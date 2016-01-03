from Systems.Engine.GameEngine import GameEngine
from Systems.Engine.SceneStack import SceneStack
from Systems.Scenes.MenuScene import MenuScene


def main():
    scene_stack = SceneStack()
    scene_stack.push(MenuScene())

    game_engine = GameEngine(scene_stack)
    game_engine.run()


if __name__ == "__main__":
    main()
