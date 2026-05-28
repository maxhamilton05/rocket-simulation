from simulation import RocketSimulator

def main():
    # Create simulator instance
    sim = RocketSimulator()

    # Setup simulation with default parameters
    sim.setup(
        initial_position=[0.0, 0.0, 0.0],   # Launch from ground
        initial_velocity=[0.0, 0.0, 0.0],
        initial_mass=1000.0,                # kg
        thrust=15000.0,                     # Newtons
        burn_time=35.0                      # seconds
    )

    # Run the simulation
    logger = sim.run()

    # Get recorded data for analysis
    data = logger.get_data()

    print("\n=== Simulation Results ===")
    print(f"Maximum Altitude: {data['altitude'].max():.1f} m")
    print(f"Maximum Speed: {data['speed'].max():.1f} m/s")
    print(f"Final Mass: {data['mass'][-1]:.1f} kg")
    print(f"Simulation Duration: {data['time'][-1]:.1f} seconds")

if __name__ == "__main__":
    main()