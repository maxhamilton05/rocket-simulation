import unittest

import numpy as np

from rocket_sim.dynamics.propulsion import PropulsionSystem


class TestPropulsionSystem(unittest.TestCase):
    def test_constant_thrust_mass_flow_rate(self):
        propulsion = PropulsionSystem()
        propulsion.set_constant_thrust(
            thrust=1000.0,
            burn_time=10.0,
            dry_mass=100.0,
            initial_mass=200.0,
        )

        self.assertEqual(propulsion.fuel_mass, 100.0)
        self.assertEqual(propulsion.dry_mass, 100.0)
        self.assertTrue(np.isclose(propulsion.mass_flow_rate, -10.0))
        self.assertTrue(np.isclose(propulsion.get_mass_flow_rate(0.0), propulsion.mass_flow_rate))
        self.assertEqual(propulsion.get_mass_flow_rate(10.0), 0.0)
        np.testing.assert_array_equal(propulsion.get_thrust(0.0), np.array([0.0, 0.0, -1000.0]))
        np.testing.assert_array_equal(propulsion.get_thrust(11.0), np.zeros(3))
