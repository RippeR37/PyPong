from Systems.Engine.Scene import Scene
from Systems.Game.PlayerState import PlayerState
from Systems.Game.BallState import BallState
from Systems.Game.GameState import GameState
from Systems.Network.Messages.GamestateUpdateProc import GameStateUpdateProc
from Systems.Network.PyPongClient import PyPongClient
import pygame


class GameplayScene(Scene):
    def __init__(self, client, client_listener, window, index):
        assert isinstance(client, PyPongClient), "Invalid object type - client must be of PyPongClient type!"

        super().__init__(True, False)
        self._client = client
        self._client_listener = client_listener
        self._index = index
        self._window = window
        self._end = False
        self._lobby = False
        self._game_state = \
            GameState(data=(PlayerState(-1.0, 0.0), PlayerState(1.0, 0.0), BallState(0.0, 0.0, 1.0, 1.0)))
        self._speed = 0.0
        self._speed_factor = 2.5
        self._clock = pygame.time.Clock()
        self._window.set_title("PyPong - Gameplay | {}:{}".format(0, 0))
        self._client.bind_proc_callback(self._process_json_proc)
        self._ball_img = pygame.image.load("Assets/ball.jpg")
        self._new_window_title = ""

    def _process_key_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self._speed += -1.0 * self._speed_factor
            elif event.key == pygame.K_DOWN:
                self._speed += 1.0 * self._speed_factor
            elif event.key == pygame.K_SPACE:
                self._send_round_start()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self._speed -= -1.0 * self._speed_factor
            elif event.key == pygame.K_DOWN:
                self._speed -= 1.0 * self._speed_factor

    def _send_round_start(self):
        self._client.signal_round_start()

    def _update_title_pts(self, game_state):
        def cmp_pts(gs1, gs2):
            return gs1.player1.pts == gs2.player1.pts and gs1.player2.pts == gs2.player2.pts

        if not cmp_pts(self._game_state, game_state):
            self._new_window_title = "PyPong - Gameplay | {}:{}".format(game_state.player1.pts, game_state.player2.pts)

    def _process_json_proc(self, json_proc):
        try:
            if json_proc['proc'] == 'index_assignment':
                print("[CLIENT] Other player has disconnected!")
                print("[CLIENT] Waiting for new player to connect...")
                self._lobby = True
                self._index = json_proc['data']['index']
                self._client.set_default_proc_callback()
                return False  # consume message as it was processed
        except:
            pass

        try:
            if json_proc['proc'] == 'game_state_update':
                server_gs = GameStateUpdateProc(None).from_json(json_proc)
                self._update_title_pts(server_gs.data['game_state'])
                self._game_state.ball = server_gs.data['game_state'].ball
                if self._index == 0:
                    self._game_state.player2 = server_gs.data['game_state'].player2
                if self._index == 1:
                    self._game_state.player1 = server_gs.data['game_state'].player1
                return False  # consume message as it was processed
        except:
            pass

        return True  # consume this message to avoid piling

    def update(self, dt):
        if self._lobby:
            return

        self._clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end = True
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self._process_key_event(event)

        if not self._end:
            if self._new_window_title != "":
                self._window.set_title(self._new_window_title)
                self._new_window_title = ""

        frame_game_state = self._game_state  # take current game state and work with it

        # Update game state in this frame
        if self._index == 0:
            self._game_state.player1.y += self._speed * dt
            self._game_state.player1.y = min(1.0, frame_game_state.player1.y)
            self._game_state.player1.y = max(-1.0, frame_game_state.player1.y)
        elif self._index == 1:
            self._game_state.player2.y += self._speed * dt
            self._game_state.player2.y = min(1.0, frame_game_state.player2.y)
            self._game_state.player2.y = max(-1.0, frame_game_state.player2.y)

        # Send new state to server
        self._client.update_host_game_state(self._game_state)

    def render(self):
        if not self._end and not self._lobby:
            self._render_player(self._game_state.player1)
            self._render_player(self._game_state.player2)
            self._render_ball(self._game_state.ball)

            self._window.swap()

    def process_scene_stack(self, scene_stack, scene_index):
        if self._end:
            scene_stack.clear()
        if self._lobby:
            scene_stack.get_scene(scene_index-1).set_index(self._index)
            scene_stack.cut_from(self)

    def _render_player(self, player_data):
        player_rect = self._get_player_rect(player_data)
        self._window.get_surface().fill((255, 255, 255), player_rect)

    def _render_ball(self, ball_data):
        ball_rect = self._get_ball_rect(ball_data)
        self._window.get_surface().blit(self._ball_img, ball_rect)

    def _get_player_rect(self, player_data):
        width = self._window.get_size()[0] / 30
        height = self._window.get_size()[1] / 5

        pos_x = (player_data.x + 1.0) * 0.5 * (self._window.get_size()[0] - width)
        pos_y = (player_data.y + 1.0) * 0.5 * (self._window.get_size()[1] - height)

        return pos_x, pos_y, width, height

    def _get_ball_rect(self, ball_data):
        width = self._window.get_size()[0] / 30
        height = self._window.get_size()[1] / 20

        pos_x = (ball_data.x + 1.0) * 0.5 * (self._window.get_size()[0] - width)
        pos_y = (ball_data.y + 1.0) * 0.5 * (self._window.get_size()[1] - height)

        return pos_x, pos_y, width, height
