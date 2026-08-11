import numpy as np
from dataclasses import dataclass

from .environment import Environment
from .propulsion import PropulsionSystem

@dataclass
class RocketState:
    """State vector for a 3DOF point mass rocket."""
    position: np.ndarray  # [x, y, z] - North, East, Down
    velocity: np.ndarray  # [vx, vy, vz] - North, East, Down
    mass : float
    time : float = 0.0

    def __post_init__(self):
        self.position = np.asarray(self.position, dtype=float)
        self.velocity = np.asarray(self.velocity, dtype=float)

class PointMassRocket:
    """3DOF point mass rocket dynamics"""
    def __init__(self):
        self.state : RocketState = None
        self.environment : Environment = None
        self.propulsion : PropulsionSystem = None
    
    def initialize(self, initial_position : np.ndarray, initial_velocity : np.ndarray, initial_mass : float):
        self.state = RocketState(position=initial_position, velocity=initial_velocity, mass=initial_mass)
    
    def set_environment(self, environment : Environment):
        self.environment = environment

    def set_propulsion(self, propulsion : PropulsionSystem):
        self.propulsion = propulsion
    
    def derivatives(self, state :  RocketState) -> tuple[np.ndarray, float]:
        """Compute the time derivates of the state vector. Returns acceleration and mass flow rate."""
        # Get forces (gravity, thrust, drag, wind)
        gravity_force = self.environment.get_gravity(state.position) * state.mass  # F = m * g
        thrust_force = self.propulsion.get_thrust(state.time)  # F = T
        drag_force = self.environment.get_drag(state.velocity, state.position)  # F = D
        # When wind is implemented, turn the wind vector into a force
        wind_force = self.environment.get_wind(state.position)  # F = W (not implemented yet)

        # Sum forces and calculate acceleration
        total_force = gravity_force + thrust_force + drag_force + wind_force
        acceleration = total_force / state.mass  # a = F / m

        # Get mass flow rate from propulsion
        mass_flow_rate = self.propulsion.get_mass_flow_rate(state.time)

        return acceleration, mass_flow_rate

    def step(self, dt: float, method: str = "euler"):
        """Advance the simulation by one time step."""
        if method == "rk4":
            return self.step_rk4(dt)

        # Get derivatives
        acceleration, mass_flow_rate = self.derivatives(self.state)

        # Forward Euler integration
        self.state.velocity += acceleration * dt
        self.state.position += self.state.velocity * dt
        self.state.mass += mass_flow_rate * dt  # mass flow rate is negative when burning fuel
        self.state.time += dt

        self._clamp_mass()

    def step_rk4(self, dt: float):
        """Advance the simulation by one time step using RK4 integration."""
        def state_derivatives(state: RocketState):
            acceleration, mass_flow_rate = self.derivatives(state)
            return state.velocity, acceleration, mass_flow_rate

        s0 = self.state
        k1_v, k1_a, k1_m = state_derivatives(s0)

        s1 = RocketState(
            position=s0.position + 0.5 * k1_v * dt,
            velocity=s0.velocity + 0.5 * k1_a * dt,
            mass=s0.mass + 0.5 * k1_m * dt,
            time=s0.time + 0.5 * dt,
        )
        k2_v, k2_a, k2_m = state_derivatives(s1)

        s2 = RocketState(
            position=s0.position + 0.5 * k2_v * dt,
            velocity=s0.velocity + 0.5 * k2_a * dt,
            mass=s0.mass + 0.5 * k2_m * dt,
            time=s0.time + 0.5 * dt,
        )
        k3_v, k3_a, k3_m = state_derivatives(s2)

        s3 = RocketState(
            position=s0.position + k3_v * dt,
            velocity=s0.velocity + k3_a * dt,
            mass=s0.mass + k3_m * dt,
            time=s0.time + dt,
        )
        k4_v, k4_a, k4_m = state_derivatives(s3)

        self.state.position = s0.position + dt * (k1_v + 2.0 * k2_v + 2.0 * k3_v + k4_v) / 6.0
        self.state.velocity = s0.velocity + dt * (k1_a + 2.0 * k2_a + 2.0 * k3_a + k4_a) / 6.0
        self.state.mass = s0.mass + dt * (k1_m + 2.0 * k2_m + 2.0 * k3_m + k4_m) / 6.0
        self.state.time += dt

        self._clamp_mass()

    def _clamp_mass(self):
        # Prevent negative mass or mass below the dry mass
        if self.propulsion is not None and self.state.mass < self.propulsion.dry_mass:
            self.state.mass = self.propulsion.dry_mass
        elif self.state.mass < 0.1:
            self.state.mass = 0.1

    