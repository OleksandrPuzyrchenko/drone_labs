from typing import TYPE_CHECKING
from ..flight_state import FlightState
from .handler import FlightStateHandler

if TYPE_CHECKING:
    from ..flight_test_node import FlightTestNode

class WaitingForLandingHandler(FlightStateHandler):
    def handle(self, node: "FlightTestNode") -> None:
        if node.status is None:
            return
            
        if not node.status.flying:
            node.get_logger().info("Landing completed successfully!")
            
            final_alt = 0.0
            if node.odometry is not None:
                final_alt = node.odometry.pose.pose.position.z

            node.get_logger().info("=" * 60)
            node.get_logger().info("LAB WORK №2 - FLIGHT MISSION REPORT")
            node.get_logger().info("=" * 60)
            node.get_logger().info(f"Student Variant: {node.VARIANT}")
            node.get_logger().info(f"Offsets: Delta_x = {node.DELTA_X:.1f} m, Delta_y = {node.DELTA_Y:.1f} m")
            
            if node.initial_position is not None:
                x0, y0, z0 = node.initial_position
                node.get_logger().info(f"1. Initial coordinates (x0, y0, z0):")
                node.get_logger().info(f"x0 = {x0:.4f} m, y0 = {y0:.4f} m, z0 = {z0:.4f} m")
            
            if node.target_position is not None:
                xt, yt = node.target_position
                node.get_logger().info(f"2. Target coordinates (x_target, y_target):")
                node.get_logger().info(f"x_target = {xt:.4f} m, y_target = {yt:.4f} m")
            
            if node.pre_landing_position is not None:
                xa, ya, za = node.pre_landing_position
                node.get_logger().info(f"3. Actual coordinates before landing (x_actual, y_actual):")
                node.get_logger().info(f"x_actual = {xa:.4f} m, y_actual = {ya:.4f} m, z_actual = {za:.4f} m")
            
            if node.position_error is not None:
                node.get_logger().info(f"4. Positioning error e = sqrt((x_actual - x_target)^2 + (y_actual - y_target)^2):")
                node.get_logger().info(f"e = {node.position_error:.4f} m")
                if node.position_error <= 0.3:
                    node.get_logger().info(f"STATUS: PASSED (e <= 0.30 m tolerance)")
                else:
                    node.get_logger().warn(f"STATUS: Out of recommended tolerance")

            node.get_logger().info(f"5. Final touchdown altitude: {final_alt:.3f} m")
            node.get_logger().info("=" * 60)

            node.state = FlightState.FINISHED
            node.get_logger().info("Flight test completed successfully")