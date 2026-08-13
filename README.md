# Rocket Simulation

A Python-based 3DOF point-mass rocket trajectory simulator designed to explore rocket flight dynamics, propulsion, environmental modeling, and numerical integration.

The simulator models a rocket's motion through the atmosphere using variable mass, thrust, gravity, and aerodynamic drag. The simulation architecture separates the physical models from the simulation loop and data logging, making the system straightforward to extend with additional physics models and numerical methods.

# Features

3DOF point-mass rocket dynamics
- Position and velocity represented in a North-East-Down coordinate frame
- Variable vehicle mass throughout powered flight
- Force-based equations of motion

Propulsion modeling
- Configurable constant-thrust engine
- Finite burn duration
- Propellant mass depletion
- Dry-mass constraint

Environmental modeling
- Altitude-dependent gravity using an inverse-square model
- Exponential atmospheric density and pressure model
- Aerodynamic drag based on atmospheric density and velocity
- Extensible environment model for future wind and atmospheric improvements

Numerical integration
- Forward Euler integration
- Fourth-order Runge-Kutta (RK4) integration

Simulation and data logging
- Configurable simulation timestep and maximum duration
- Records position, velocity, speed, altitude, mass, thrust, drag, weight, and gravitational acceleration
- Outputs simulation data as NumPy arrays for analysis and visualization

# Model

The rocket is represented as a point mass with the state

$$
x =
\begin{bmatrix}
r \\
v \\
m
\end{bmatrix}
$$

where:

- $r$ is position
- $v$ is velocity
- $m$ is vehicle mass

The equations of motion are based on

$$
\frac{dr}{dt} = v
$$

$$
\frac{dv}{dt} =
\frac{F_{gravity} + F_{thrust} + F_{drag}}{m}
$$

and

$$
\frac{dm}{dt} = \dot{m}
$$

Gravity is modeled using an inverse-square relationship with altitude, while atmospheric density is approximated using an exponential atmosphere model.

# Numerical Integration

The simulator currently supports Forward Euler and RK4 integration.

RK4 evaluates the state derivatives at four points within each timestep and combines them using the weighted average

$$
x_n+
\frac{\Delta t}{6}
(k_1 + 2k_2 + 2k_3 + k_4)
$$

This provides substantially higher-order accuracy than Forward Euler for a comparable timestep and makes RK4 useful for studying the effects of numerical integration error on trajectory simulation.

# Installation

Python 3.11 or newer is required.

Clone the repository:

git clone https://github.com/maxhamilton05/rocket-simulation.git

cd rocket-simulation

Install the package:

pip install -e .

# Running the Simulation

The simulator can be run as a Python module:

python -m rocket_sim

The main simulation parameters can be configured through the simulator setup, including:

- Initial position
- Initial velocity
- Initial mass
- Thrust
- Burn duration
- Simulation timestep
- Maximum simulation time

# Current Limitations

This project is intended as an educational and engineering-focused simulation framework rather than a high-fidelity flight simulator.

Current simplifications include:

- 3DOF point-mass dynamics rather than 6DOF rigid-body dynamics
- Simplified exponential atmospheric model
- Fixed drag coefficient-area parameter
- No wind model
- Constant thrust in the current propulsion implementation
- Thrust is currently constrained to the vertical axis
- No aerodynamic lift or attitude dynamics
- No guidance, navigation, or control system

These limitations also provide opportunities for future development.

# Future Work

Potential extensions include:

- 6DOF rigid-body dynamics
- Monte Carlo simulation
- Time-varying thrust curves
- More realistic atmospheric models
- Wind modeling
- Mach-dependent aerodynamic coefficients
- Attitude and rotational dynamics
- Guidance, navigation, and control (GNC)
- Additional numerical integration methods
- Numerical accuracy and convergence studies
- Improved trajectory visualization

# License

This project is licensed under the [MIT License](LICENSE).
