import unittest

import numpy as np

from rocket_sim.dynamics.environment import Environment
from rocket_sim.dynamics.point_mass import PointMassRocket
from rocket_sim.dynamics.propulsion import PropulsionSystem
from rocket_sim.simulation.logger import SimulationLogger
from rocket_sim import RocketSimulator


class TestPointMassRocket(unittest.TestCase):
    def test_step_updates_time_and_position(self):
        env = Environment()
        propulsion = PropulsionSystem()
        propulsion.set_constant_thrust(
            thrust=1000.0,
            burn_time=1.0,
            dry_mass=80.0,
            initial_mass=100.0,
        )

        rocket = PointMassRocket()
        rocket.set_environment(env)
        rocket.set_propulsion(propulsion)
        rocket.initialize([0.0, 0.0, 0.0], [0.0, 0.0, 0.0], 100.0)

        rocket.step(0.1)

        self.assertEqual(rocket.state.time, 0.1)
        self.assertNotEqual(rocket.state.position[2], 0.0)
        self.assertTrue(rocket.state.mass < 100.0)

    def test_step_clamps_mass_at_dry_mass(self):
        env = Environment()
        propulsion = PropulsionSystem()
        propulsion.set_constant_thrust(
            thrust=1000.0,
            burn_time=1.0,
            dry_mass=50.0,
            initial_mass=100.0,
        )

        rocket = PointMassRocket()
        rocket.set_environment(env)
        rocket.set_propulsion(propulsion)
        rocket.initialize([0.0, 0.0, 0.0], [0.0, 0.0, 0.0], 100.0)
        rocket.state.mass = 40.0

        rocket.step(0.1)

        self.assertEqual(rocket.state.mass, 50.0)


class TestSimulationLogger(unittest.TestCase):
    def test_record_populates_all_fields(self):
        env = Environment()
        propulsion = PropulsionSystem()
        propulsion.set_constant_thrust(
            thrust=500.0,
            burn_time=0.5,
            dry_mass=90.0,
            initial_mass=100.0,
        )

        from rocket_sim.dynamics.point_mass import RocketState

        state = RocketState(
            position=np.array([0.0, 0.0, 0.0]),
            velocity=np.array([1.0, 1.0, 0.0]),
            mass=100.0,
            time=0.0,
        )

        logger = SimulationLogger()
        logger.record(state, env, propulsion)
        data = logger.get_data()

        expected_keys = {
            'time', 'position_x', 'position_y', 'position_z',
            'velocity_x', 'velocity_y', 'velocity_z', 'speed',
            'mass', 'altitude', 'gravity_accel', 'weight', 'drag', 'thrust'
        }
        self.assertEqual(set(data.keys()), expected_keys)
        self.assertEqual(data['time'].tolist(), [0.0])
        self.assertEqual(data['mass'].tolist(), [100.0])
        self.assertEqual(data['altitude'].tolist(), [0.0])
        self.assertTrue(np.isclose(data['speed'][0], np.sqrt(2.0)))
        self.assertTrue(data['gravity_accel'][0] > 0.0)
        self.assertTrue(data['thrust'][0] > 0.0)


class TestRocketSimulator(unittest.TestCase):
    def test_setup_wires_components_and_initializes_state(self):
        sim = RocketSimulator()
        sim.setup(
            initial_position=[0.0, 0.0, 0.0],
            initial_velocity=[0.0, 0.0, 0.0],
            initial_mass=100.0,
            thrust=500.0,
            burn_time=0.5,
        )

        self.assertIsNotNone(sim.rocket.state)
        self.assertIsNotNone(sim.rocket.environment)
        self.assertIsNotNone(sim.rocket.propulsion)
        self.assertEqual(sim.rocket.state.mass, 100.0)
        self.assertEqual(sim.rocket.state.time, 0.0)

    def test_run_returns_logger_with_data(self):
        sim = RocketSimulator()
        sim.setup(
            initial_position=[0.0, 0.0, 0.0],
            initial_velocity=[0.0, 0.0, 0.0],
            initial_mass=100.0,
            thrust=500.0,
            burn_time=0.5,
        )
        sim.max_time = 0.05
        sim.dt = 0.01

        logger = sim.run()
        data = logger.get_data()

        self.assertGreater(len(data['time']), 0)
        self.assertIn('altitude', data)
        self.assertIn('mass', data)
        self.assertEqual(data['time'][-1], 0.05)
