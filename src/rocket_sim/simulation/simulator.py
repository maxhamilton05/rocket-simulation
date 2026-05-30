from ..dynamics import PointMassRocket, PropulsionSystem, Environment
from .logger import SimulationLogger
from ..config import DT, MAX_SIM_TIME

class RocketSimulator:
    """Main class to run a full rocket simulation."""

    def __init__(self):
        self.rocket = PointMassRocket()
        self.environment = Environment()
        self.propulsion = PropulsionSystem()
        self.logger = SimulationLogger()
        self.dt = DT  # time step for simulation
        self.max_time = MAX_SIM_TIME  # maximum simulation time

    def setup(self,
              initial_position=None,
              initial_velocity=None,
              initial_mass=1000.0,
              thrust=15000.0,
              burn_time=10.0):
        """Initialize the rocket, environment, and propulsion system."""

        # Set initial conditions
        if initial_position is None:
            initial_position = [0.0, 0.0, 0.0]
        
        if initial_velocity is None:
            initial_velocity = [0.0, 0.0, 0.0]

        # Configure components
        self.rocket.set_environment(self.environment)
        self.rocket.set_propulsion(self.propulsion)

        self.propulsion.set_constant_thrust(
            thrust=thrust,
            burn_time=burn_time,
            dry_mass=initial_mass * 0.3,
            initial_mass=initial_mass,
        )

        # Initialize rocket state
        self.rocket.initialize(initial_position, initial_velocity, initial_mass)
    
    def run(self):
        """Run the simulation loop."""
        """Runs the simulation until burnout + some coasting time."""
        print("Starting simulation...")

        while self.rocket.state.time < self.max_time:
            self.rocket.step(self.dt)
            self.logger.record(self.rocket.state, self.environment, self.propulsion)

        print("Simulation complete.")
        return self.logger
    