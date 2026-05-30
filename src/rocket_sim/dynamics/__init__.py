"""
Dynamics module for rocket trajectory simulation (3DOF point mass model).
"""

from .point_mass import RocketState, PointMassRocket
from .environment import Environment
from .propulsion import PropulsionSystem