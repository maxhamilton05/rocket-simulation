import numpy as np
from ..config import GRAVITY

class Environment:
    """Model for gravity, atmosphere, and wind.
    Coordinate system:
        x = north
        y = east
        z = down

    Altitude = -z
    Gravity points in +z direction.
    """
    def __init__(self):
        self.gravity = GRAVITY  # m/s^2
        self.earth_radius = 6371000.0  # meters

    def get_gravity(self, position : np.ndarray) -> np.ndarray:
        """Calculate gravity vector based on position."""
        """Returns a vector pointing downward with magnitude based on altitude."""
        altitude = -position[2]  # z is positive down, so altitude is negative of z
        altitude = max(0.0, altitude)  # Don't allow below ground level

        # Inverse square law for gravity magnitude
        g_mag = self.gravity * (self.earth_radius / (self.earth_radius + altitude))**2
        return np.array([0.0, 0.0, g_mag])  # downward gravity vector
    
    def get_atmosphere(self, altitude : float) -> tuple[float, float]:
        """Calculate density and pressure based on altitude."""
        """Returns a tuple of (density, pressure)."""
        """Simple exponential atmosphere model for density and pressure."""
        altitude = max(0.0, altitude)
        density = 1.225 * np.exp(-altitude / 8500.0)  # kg/m^3
        pressure = 101325.0 * np.exp(-altitude / 8500.0)  # Pa
        return density, pressure
    
    def get_drag(self, velocity : np.ndarray, position : np.ndarray) -> np.ndarray:
        """Calculate drag force based on velocity and altitude."""
        """Returns a vector representing the drag force."""
        # Once wind is implemented, calculate relative velocity to the air and use that for drag
        speed = np.linalg.norm(velocity)
        if speed < 1e-6:
            return np.zeros(3)  # No drag if velocity is negligible
        
        # Get atmospheric density from position
        rho, _ = self.get_atmosphere(-position[2])  # Use altitude (z) to get density
        
        # Temporarily using: Cd * A (improve later)
        drag_coeff_area = 0.5  # m²
        drag_magnitude = 0.5 * rho * speed**2 * drag_coeff_area
        drag_force = -drag_magnitude * (velocity / speed)
        return drag_force
    
    def get_wind(self, position: np.ndarray) -> np.ndarray:
        """Wind velocity vector"""
        return np.zeros(3)  # No wind for now