from Systems.Engine.Scene import Scene
from Systems.Engine.Window import Window
from Systems.Game.PlayerState import PlayerState
from Systems.Game.BallState import BallState
from Systems.Game.GameState import GameState
from Systems.Network.PyPongClient import PyPongClient
import pygame
import threading


class GameplayScene(Scene):
    def __init__(self, client):
        assert isinstance(client, PyPongClient), "Invalid object type - client must be of PyPongClient type!"

        super().__init__(True, False)
        self._client = client
        self._client.bind_gameplay(self)
        self._end = False
        self._window = Window((600, 400), "PyPong")
        self._window.create()
        self._game_state = \
            GameState(data=(PlayerState(-1.0, 0.0), PlayerState(1.0, 0.0), BallState(0.0, 0.0, 1.0, 1.0)))
        self._speed = 0.0
        self._listen_thread = None
        self._listen_to_host()
        self._clock = pygame.time.Clock()

    def _listen_to_host(self):
        self._listen_thread = threading.Thread(target=self._client.listen, daemon=True)
        self._listen_thread.start()

    def _process_key_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self._speed = -0.5
            elif event.key == pygame.K_DOWN:
                self._speed = 0.5
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                self._speed = 0.0

    def update(self, dt):
        self._clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end = True
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self._process_key_event(event)

        frame_game_state = self._game_state  # take current game state and work with it

        # Update game state in this frame
        self._game_state.player1.y += self._speed * dt
        self._game_state.player1.y = min(1.0, frame_game_state.player1.y)
        self._game_state.player1.y = max(-1.0, frame_game_state.player1.y)

        # Send new state to server
        self._client.update_host(self._game_state.to_json())

    def render(self):
        if not self._end:
            self._render_player(self._game_state.player1)
            self._render_player(self._game_state.player2)
            self._render_ball(self._game_state.ball)

            self._window.swap()

    def process_scene_stack(self, scene_stack, scene_index):
        if self._end:
            scene_stack.clear()  # TODO: implement better scene stack processing then quiting (e.g. go to menu/lobby)

    def _render_player(self, player_data):
        player_rect = self._get_player_rect(player_data)
        self._window.get_surface().fill((255, 255, 255), player_rect)

    def _render_ball(self, ball_data):
        ball_rect = self._get_ball_rect(ball_data)
        self._window.get_surface().fill((255, 255, 255), ball_rect)

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
