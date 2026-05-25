import numpy as np
from typing import Callable
from config import GRAVITY

class Propulsion:
    """Model for rocket propulsion, including thrust and mass flow rate."""
    def __init__(self):
        self.burn_time = 0.0  # seconds
        self.thrust_profile : Callable[[float], float] = None  # Function of time returning thrust (N)
        self.initial_mass = 0.0  # kg
        self.dry_mass = 0.0  # kg (mass after fuel is burned)
        self.isp = 250.0  # seconds (specific impulse)

    def set_constant_thrust(self, thrust: float, burn_time: float, dry_mass: float):
        """Simple constant thrust engine"""
        self.burn_time = burn_time
        self.dry_mass = dry_mass
        self.thrust_profile = lambda t: thrust if t < burn_time else 0.0  # Create a function and store it in thrust_profile

    def get_thrust(self, t: float) -> np.ndarray:
        """Calculate thrust at a given time."""
        thrust_mag = self.thrust_profile(t) if self.thrust_profile is not None else 0.0
        """Assume thrust is always in the upward direction (negative z) for simplicity."""
        return np.array([0, 0, -thrust_mag])  # Thrust vector pointing upward
    
    def get_mass_flow_rate(self, t: float) -> float:
        """Calculate mass flow rate at a given time."""
        """kg/s (negative = mass decreasing)"""
        if t >= self.burn_time:
            return 0.0  # No mass flow after engines cut off
        thrust = self.thrust_profile(t) if self.thrust_profile is not None else 0.0
        mass_flow_rate = -thrust / (self.isp * GRAVITY)  # m_dot = -T / (Isp * g0)
        return mass_flow_rate
    