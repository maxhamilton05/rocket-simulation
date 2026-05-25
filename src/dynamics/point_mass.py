import numpy as np
from dataclasses import dataclass

from dynamics.environment import Environment
from dynamics.propulsion import Propulsion

@dataclass
class RocketState:
    """State vector for a 3DOF point mass rocket."""
    position: np.ndarray  # [x, y, z] - North, East, Down
    velocity: np.ndarray  # [vx, vy, vz] - North, East, Down
    mass : float
    time : float = 0.0

    def __post_init__(self):
        self.position = np.asarray(self.position, dtype=np.float)
        self.velocity = np.asarray(self.velocity, dtype=np.float)

class PointMassRocket:
    """3DOF point mass rocket dynamics"""
    def __init__(self):
        self.state : RocketState = None
        self.environment : Environment = None
        self.propulsion : Propulsion = None
    
    def initialize(self, initial_position : np.ndarray, initial_velocity : np.ndarray, initial_mass : float):
        self.state = RocketState(position=initial_position, velocity=initial_velocity, mass=initial_mass)
    
    def set_environment(self, environment : Environment):
        self.environment = environment

    def set_propulsion(self, propulsion : Propulsion):
        self.propulsion = propulsion
    
    def derivatives(self, state :  RocketState) -> tuple[np.ndarray, float]:
        """Compute the time derivates of the state vector. Returns acceleration and mass flow rate."""
        # Get forces (gravity, thrust, drag, wind)
        gravity_force = self.environment.get_gravity(state.position) * state.mass  # F = m * g
        thrust_force = self.propulsion.get_thrust(state.time)  # F = T
        drag_force = self.environment.get_drag(state.velocity, state.position)  # F = D
        wind_force = self.environment.get_wind(state.position)  # F = W (not implemented yet)

        # Sum forces and calculate acceleration
        total_force = gravity_force + thrust_force + drag_force + wind_force
        acceleration = total_force / state.mass  # a = F / m

        # Get mass flow rate from propulsion
        mass_flow_rate = self.propulsion.get_mass_flow_rate(state.time)

        return acceleration, mass_flow_rate

    def step(self, dt: float):
        """Advance the simulation by one time step."""
        # Get derivatives
        acceleration, mass_flow_rate = self.derivatives(self.state)

        # Forward Euler integration (improve later, likely RK4)
        self.state.velocity += acceleration * dt
        self.state.position += self.state.velocity * dt
        self.state.mass += mass_flow_rate * dt  # mass flow rate is negative when burning fuel
        self.state.time += dt

        # Prevent negative mass
        if self.state.mass < 0.1:
            self.state.mass = 0.1