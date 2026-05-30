import numpy as np
from collections import defaultdict


class SimulationLogger:
    """Records simulation data for plotting and analysis."""

    def __init__(self):
        self.data : dict[str, list[float]] = defaultdict(list)

    def record(self, state, environment, propulsion):
        """Record relevant data from the current state, environment, and propulsion."""
        self.data['time'].append(state.time)
        self.data['position_x'].append(state.position[0])
        self.data['position_y'].append(state.position[1])
        self.data['position_z'].append(state.position[2])
        self.data['velocity_x'].append(state.velocity[0])
        self.data['velocity_y'].append(state.velocity[1])
        self.data['velocity_z'].append(state.velocity[2])
        self.data['speed'].append(np.linalg.norm(state.velocity))
        self.data['mass'].append(state.mass)
        self.data['altitude'].append(-state.position[2])  # z is positive down, so altitude is negative of z

        # Record gravity and forces for logging
        gravity_accel = environment.get_gravity(state.position)  # m/s^2
        weight_force = gravity_accel * state.mass  # W = m * g
        drag_force = environment.get_drag(state.velocity, state.position)
        thrust_force = propulsion.get_thrust(state.time)

        self.data['gravity_accel'].append(np.linalg.norm(gravity_accel))
        self.data['weight'].append(np.linalg.norm(weight_force))
        self.data['drag'].append(np.linalg.norm(drag_force))
        self.data['thrust'].append(np.linalg.norm(thrust_force))

    def get_data(self) -> dict[str, np.ndarray]:
        """Return the recorded data as numpy arrays."""
        return {key: np.array(value) for key, value in self.data.items()}