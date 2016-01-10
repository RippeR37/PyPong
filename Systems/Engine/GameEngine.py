from Systems.Engine.SceneStack import SceneStack
from Systems.Utils.TimeHelper import Time
from Systems.Utils.Console import Console


class GameEngine(object):
    def __init__(self, scene_stack):
        assert isinstance(scene_stack, SceneStack), "GameEngine object must be initialized with SceneStack object!"
        self._scenes = scene_stack

    def _process_scene(self, scene, dt, scene_index):
        scene.update(dt)
        scene.render()
        scene.process_scene_stack(self._scenes, scene_index)

    def run(self):
        last_time = Time.now()

        while self._scenes.count() > 0:
            this_time = Time.now()
            dt = Time.interval_as_float(this_time - last_time)
            last_time = this_time

            top_scene = self._scenes.get_scene(-1)  # get last scene
            if top_scene.is_stackable():
                for scene_index in range(self._scenes.count()):
                    current_scene = self._scenes.get_scene(scene_index)
                    if current_scene.is_stack_usable() or current_scene == top_scene:
                        self._process_scene(current_scene, dt, scene_index)
            else:
                scene_index = self._scenes.count() - 1
                last_scene = self._scenes.get_scene(scene_index)
                self._process_scene(last_scene, dt, scene_index)

        Console.cls()
