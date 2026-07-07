import unittest

import numpy as np

from rocket_sim.dynamics.environment import Environment


class TestEnvironment(unittest.TestCase):
    def test_gravity_is_downward_and_clamped_at_ground(self):
        env = Environment()

        gravity = env.get_gravity(np.array([0.0, 0.0, -1000.0]))
        np.testing.assert_allclose(gravity[:2], np.zeros(2))
        self.assertGreater(gravity[2], 0)

        gravity_ground = env.get_gravity(np.array([0.0, 0.0, 100.0]))
        self.assertTrue(np.isclose(gravity_ground[2], env.gravity))

    def test_drag_is_zero_at_zero_speed(self):
        env = Environment()
        drag = env.get_drag(np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 0.0]))
        np.testing.assert_allclose(drag, np.zeros(3))