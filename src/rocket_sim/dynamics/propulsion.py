import numpy as np
from typing import Callable
from ..config import GRAVITY

class PropulsionSystem:
    """Model for rocket propulsion, including thrust and mass flow rate."""
    def __init__(self):
        self.burn_time = 0.0  # seconds
        self.thrust_profile : Callable[[float], float] = None  # Function of time returning thrust (N)
        self.initial_mass = 0.0  # kg
        self.dry_mass = 0.0  # kg (mass after fuel is burned)
        self.fuel_mass = 0.0  # kg of propellant
        self.mass_flow_rate = 0.0  # kg/s (negative = fuel burning)
        self.isp = 250.0  # seconds (specific impulse)

    def set_constant_thrust(self, thrust: float, burn_time: float, dry_mass: float, initial_mass: float):
        """Simple constant thrust engine"""
        self.burn_time = burn_time
        self.dry_mass = max(0.0, dry_mass)
        self.initial_mass = initial_mass
        self.fuel_mass = max(0.0, self.initial_mass - self.dry_mass)
        self.mass_flow_rate = -self.fuel_mass / burn_time if burn_time > 0 and self.fuel_mass > 0 else 0.0
        self.thrust_profile = (
            lambda t: thrust if t < burn_time and self.fuel_mass > 0 else 0.0
        )

    def get_thrust(self, t: float) -> np.ndarray:
        """Calculate thrust at a given time."""
        thrust_mag = self.thrust_profile(t) if self.thrust_profile is not None else 0.0
        """Assume thrust is always in the upward direction (negative z) for simplicity."""
        return np.array([0, 0, -thrust_mag])  # Thrust vector pointing upward
    
    def get_mass_flow_rate(self, t: float) -> float:
        """Calculate mass flow rate at a given time.
        kg/s (negative = mass decreasing)"""
        if t >= self.burn_time or self.fuel_mass <= 0.0:
            return 0.0
        return self.mass_flow_rate
    