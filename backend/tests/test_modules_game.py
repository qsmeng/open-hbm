import unittest
from backend.modules.game.core import GameCore

class TestGameCore(unittest.TestCase):
    def setUp(self):
        self.game_core = GameCore()

    def test_start_game(self):
        result = self.game_core.start_game()
        self.assertEqual(result["message"], "游戏已启动")
        self.assertEqual(self.game_core.game_state, "running")

    def test_add_and_use_treasure(self):
        # 添加宝物
        add_result = self.game_core.add_treasure(1, "Treasure A", 10)
        self.assertEqual(add_result["message"], "宝物已添加")
        # 创建空间
        self.game_core.create_space(1, initial_stability=50)
        # 使用宝物
        use_result = self.game_core.use_treasure(1, 1)
        self.assertIn("space", use_result)
        self.assertGreater(use_result["space"]["stability"], 50)

    def test_explore_space(self):
        # 创建空间
        self.game_core.create_space(1, initial_stability=20)
        # 探索空间
        explore_result = self.game_core.explore_space(1, user_id=1)
        self.assertEqual(explore_result["message"], "探索成功")
        self.assertEqual(explore_result["space"]["remaining_rounds"], 18)

    def test_team_explore(self):
        # 创建空间
        self.game_core.create_space(1, initial_stability=100)
        # 团队探索
        team_result = self.game_core.team_explore(1, user_ids=[1, 2, 3])
        self.assertEqual(team_result["message"], "团队探索成功")
        self.assertLess(team_result["space"]["stability"], 100)

    def test_solidify_space_invalid_stability(self):
        # 创建一个稳定性不足的空间
        self.game_core.create_space(1, initial_stability=40)
        result = self.game_core.solidify_space(1)
        self.assertEqual(result["message"], "空间稳定性不足，无法固化")

    def test_solidify_space_success(self):
        # 创建一个足够稳定的空间
        self.game_core.create_space(1, initial_stability=60)
        result = self.game_core.solidify_space(1)
        self.assertEqual(result["message"], "空间已固化为公共安全区域")
        self.assertEqual(result["space"]["type"], "public")
        self.assertEqual(result["space"]["stability"], 100)

if __name__ == "__main__":
    unittest.main()