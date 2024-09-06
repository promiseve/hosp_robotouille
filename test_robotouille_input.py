import unittest
import pygame
from utils.robotouille_input import create_action_from_control
from unittest.mock import Mock, patch

class TestRobotouilleInput(unittest.TestCase):
    def setUp(self):
        # Mock environment, observation, and renderer
        self.env = Mock()
        self.obs = Mock()
        self.renderer = Mock()

        # Mock the renderer canvas attributes
        self.renderer.canvas = Mock()
        self.renderer.canvas.pix_square_size = [85, 85]
        self.renderer.canvas.layout = [[None] * 6 for _ in range(6)]

        # Mock the action space and its method
        self.env.action_space.all_ground_literals = Mock(return_value=iter(["giverescuebreaths(player1)"]))

    def test_g_key_for_giverescuebreaths(self):
        # Mock valid actions
        action = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_g)

        # Mock get_valid_moves to return the expected action
        with patch('utils.robotouille_utils.get_valid_moves', return_value=["giverescuebreaths(player1)"]):
            result = create_action_from_control(self.env, self.obs, [action], self.renderer)
            self.assertEqual(result, "giverescuebreaths(player1)")

if __name__ == '__main__':
    unittest.main()
