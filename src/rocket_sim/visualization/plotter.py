import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from ..dynamics.environment import Environment


def plot_telemetry(data, *, environment = None, show = True) -> tuple[Figure, np.ndarray]:
    required_fields = ("time", "altitude", "speed", "position_x", "position_y")

    # Check for missing fields
    missing = [f for f in required_fields if f not in data]
    if missing:
        raise ValueError(f"Missing required telemetry fields: {', '.join(missing)}")

    # Convert to 1D arrays and check for error
    try:
        telemetry = {field: np.asarray(data[field]) for field in required_fields}
    except Exception as e:
        raise ValueError(f"Error converting telemetry data: {e}")

    # Check multiple data validation rules
    sample_count = telemetry["time"].size
    if sample_count == 0 or any(a.ndim != 1 or a.size != sample_count or not np.all(np.isfinite(a)) for a in telemetry.values()):
        raise ValueError("All telemetry fields must be 1D, non-empty, have equal lengths, and contain only finite values.")

    # Dynamic Pressure Calculation
    if "dynamic_pressure" in data:
        try:
            dynamic_pressure = np.asarray(data["dynamic_pressure"], dtype=float)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Error converting dynamic pressure data: {e}") from e
        if (
            dynamic_pressure.ndim != 1
            or dynamic_pressure.size != sample_count
            or not np.all(np.isfinite(dynamic_pressure))
        ):
            raise ValueError(
                "Dynamic pressure must be one-dimensional, finite, and have "
                "the same number of samples as the other telemetry fields."
            )
    else:
        atmosphere = environment if environment is not None else Environment()
        density = np.fromiter(
            (atmosphere.get_atmosphere(float(alt))[0] for alt in telemetry["altitude"]),
            dtype=float,
            count=sample_count,
        )
        dynamic_pressure = 0.5 * density * telemetry["speed"] ** 2

    # --- Plotting Setup ---
    fig, axes = plt.subplots(3, 1, figsize=(11, 12), constrained_layout=True)
    alt_ax, pres_ax, traj_ax = axes

    # 1. Ascent Profile (Dual Axis)
    vel_ax = alt_ax.twinx()
    alt_line, = alt_ax.plot(telemetry["time"], telemetry["altitude"], color="tab:blue", label="Altitude")
    vel_line, = vel_ax.plot(telemetry["time"], telemetry["speed"], color="tab:orange", label="Speed")
    
    alt_ax.set_title("Ascent Profile")
    alt_ax.set_ylabel("Altitude (m)", color="tab:blue")
    vel_ax.set_ylabel("Speed (m/s)", color="tab:orange")
    alt_ax.set_xlabel("Time (s)")
    alt_ax.legend((alt_line, vel_line), (alt_line.get_label(), vel_line.get_label()), loc="best")

    # 2. Dynamic Pressure & Max Q
    max_q_idx = int(np.argmax(dynamic_pressure))
    max_q, max_q_time = dynamic_pressure[max_q_idx], telemetry["time"][max_q_idx]
    
    pres_ax.plot(telemetry["time"], dynamic_pressure, color="tab:green", label="Dynamic pressure")
    pres_ax.scatter(max_q_time, max_q, color="tab:red", marker="*", s=120, zorder=3, label="Max Q")
    pres_ax.annotate(
        f"Max Q: {max_q:.0f} Pa at {max_q_time:.2f} s",
        xy=(max_q_time, max_q), xytext=(10, 12),
        textcoords="offset points", arrowprops={"arrowstyle": "->", "color": "tab:red"}
    )
    pres_ax.set_title("Dynamic Pressure")
    pres_ax.set_xlabel("Time (s)")
    pres_ax.set_ylabel("Dynamic pressure (Pa)")
    pres_ax.legend(loc="best")

    # 3. 2D Flight Path
    downrange = np.hypot(telemetry["position_x"], telemetry["position_y"])
    traj_ax.plot(downrange, telemetry["altitude"], color="tab:purple")
    traj_ax.set_title("2D Flight Path")
    traj_ax.set_xlabel("Downrange distance (m)")
    traj_ax.set_ylabel("Altitude (m)")

    for ax in axes:
        ax.grid(True, alpha=0.3)

    fig.suptitle("Rocket Telemetry Dashboard")
    if show:
        plt.show()

    return fig, axes