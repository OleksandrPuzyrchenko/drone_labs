import time
from typing import TYPE_CHECKING
from ..flight_state import FlightState
from .handler import FlightStateHandler

if TYPE_CHECKING:
    from ..flight_test_node import FlightTestNode

class HoveringHandler(FlightStateHandler):
    def handle(self, node: "FlightTestNode") -> None:
        if node.status is None or not node.status.armed:
            node.fail("Drone disarmed unexpectedly during flight")
            return

        if node.odometry is not None:
            altitude = node.odometry.pose.pose.position.z
            node.get_logger().debug(
                f"Gazebo altitude: {altitude:.2f} m"
            )

        elapsed = time.monotonic() - node.hover_started_at
        if elapsed >= node.HOVER_DURATION:
            if node.odometry is None:
                return

            x0 = node.odometry.pose.pose.position.x
            y0 = node.odometry.pose.pose.position.y
            z0 = node.odometry.pose.pose.position.z

            if z0 < 1.5:
                node.get_logger().info(
                    f"Waiting for drone to reach target altitude (current: {z0:.2f} m)..."
                )
                return

            node.initial_position = (x0, y0, z0)

            x_target = x0 - node.DELTA_X
            y_target = y0 - node.DELTA_Y
            node.target_position = (x_target, y_target)

            node.get_logger().info(
                f"Hover stabilization completed."
            )
            node.get_logger().info(
                f"Initial position (x0, y0): ({x0:.3f}, {y0:.3f}), altitude: {z0:.2f} m"
            )
            node.get_logger().info(
                f"Variant {node.VARIANT}: Delta_x = {node.DELTA_X:.1f} m, Delta_y = {node.DELTA_Y:.1f} m"
            )
            node.get_logger().info(
                f"Calculated target (x_target, y_target): ({x_target:.3f}, {y_target:.3f})"
            )
            node.get_logger().info(
                f"Starting autonomous flight to target (tolerance: {node.TARGET_TOLERANCE:.2f} m)..."
            )
            node.state = FlightState.FLYING_TO_TARGET