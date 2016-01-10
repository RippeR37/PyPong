from Systems.Engine.Scene import Scene
from Systems.Network.PyPongClient import PyPongClient
import pygame


class GameOverScene(Scene):
    def __init__(self, client, client_listener, window, index, stats, game_over_result, gameplay_ctor):
        assert isinstance(client, PyPongClient), "Invalid object type - client must be of PyPongClient type!"

        super().__init__(True, False)
        self._client = client
        self._client_listener = client_listener
        self._window = window
        self._index = index
        self._stats = stats
        self._end = False
        self._lobby = False
        self._play_again = False
        self._signal_play_again_sent = False
        self._result = game_over_result
        self._gameplay_ctor = gameplay_ctor
        self._font = pygame.font.SysFont("arial", 18)

        self._process_stats()  # Set window's title and increment value in players stats
        self._client.bind_proc_callback(self._process_json_proc)  # Bind this scene proc callback

    def _process_stats(self):
        # Set new window title
        title = "PyPong - You have {}".format("won!" if self._result == "win" else "lost.")
        self._window.set_title(title)

        # Update statistics
        if self._stats is not None:
            if self._result == "win":
                self._stats.increment_wins()
            else:
                self._stats.increment_loses()
            self._stats.save()

    def _process_json_proc(self, json_proc):
        if json_proc['proc'] == 'index_assignment':
            print("[CLIENT] Other player has disconnected!")
            print("[CLIENT] Waiting for new player to connect...")
            self._lobby = True
            self._index = json_proc['data']['index']
            self._client.set_default_proc_callback()
            return False  # consume message as it was processed

        elif json_proc['proc'] == "game_state_update":
            return False  # ignore it and consume

        elif json_proc['proc'] == "server_ready":
            print("[CLIENT] Starting new game...")
            self._play_again = True
            self._client.set_default_proc_callback()
            return False  # consume message as it was processed

        # print("[CLIENT][GAME_OVER] Unhandled json procedure: {}".format(json_proc)  # DEBUG
        return False  # consume other messages not to pile up (and they 'should' be at most game_state_update)

    def _signal_play_again(self):
        if not self._signal_play_again_sent:  # Send it only once
            self._client.signal_play_again()
            self._signal_play_again_sent = True

    def update(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._signal_play_again()
                elif event.key == pygame.K_ESCAPE:
                    self._end = True

    def render(self):
        if not self._end:
            self._window.swap()

        if not self._signal_play_again_sent:
            self._render_options()
        else:
            self._render_wait()

    def _render_options(self):
        window_size = self._window.get_size()
        white_color = (255, 255, 255)

        text1 = "You have {} the game!".format("won" if self._result == "win" else "lost")
        text2 = "Press [SPACE] to play again or [ESC] to quit."

        size1 = self._font.size(text1)
        size2 = self._font.size(text2)

        label1 = self._font.render(text1, True, white_color)
        label2 = self._font.render(text2, True, white_color)

        offset1 = ((window_size[0] - size1[0]) / 2, 150)  # center of screen
        offset2 = ((window_size[0] - size2[0]) / 2, 200)  # center of screen

        self._window.get_surface().blit(label1, offset1)
        self._window.get_surface().blit(label2, offset2)

    def _render_wait(self):
        window_size = self._window.get_size()
        white_color = (255, 255, 255)

        text = "Waiting for other player to signal he's ready..."
        size = self._font.size(text)

        label = self._font.render(text, True, white_color)
        offset = ((window_size[0] - size[0]) / 2, 150)  # center of screen

        self._window.get_surface().blit(label, offset)

    def process_scene_stack(self, scene_stack, scene_index):
        if self._end:
            scene_stack.clear()
        elif self._lobby:
            scene_stack.get_scene(scene_index-1).set_index(self._index)
            scene_stack.cut_from(self)
        elif self._play_again:
            scene_stack.cut_from(self)
            scene_stack.push(self._gameplay_ctor(
                self._client,
                self._client_listener,
                self._window,
                self._index,
                self._stats
            ))
