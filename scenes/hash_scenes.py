hash_table_scenes = {
    0: 'TestScene',
    1: 'ActionScene',
    2: 'AttackScene'
}

def create_scene(scene_id, width, height, ground_level):
    if scene_id == 0:
        from scenes.test_scene import TestScene
        return TestScene(width, height, ground_level)
    elif scene_id == 1:
        from scenes.action_test_scene import ActionScene
        return ActionScene(width, height, ground_level)
    elif scene_id == 2:
        from scenes.attack_test_scene import AttackScene
        return AttackScene(width, height, ground_level)