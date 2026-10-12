import math
import time
from typing import TYPE_CHECKING
from geometry_msgs.msg import TwistStamped
from ..flight_state import FlightState
from .handler import FlightStateHandler

if TYPE_CHECKING:
    from ..flight_test_node import FlightTestNode

class FlyingToTargetHandler(FlightStateHandler):

    def __init__(self):
        self.last_log_time = 0.0
        self.kp_horizontal = 0.6 
        self.max_speed = 0.8
        self.min_speed = 0.15
        self.kp_altitude = 0.5
        self.max_climb_rate = 0.3

    def handle(self, node: "FlightTestNode") -> None:
        if node.status is None or not node.status.armed:
            node.fail("Drone disarmed unexpectedly during flight to target")
            return

        if node.odometry is None or node.target_position is None:
            return

        current_x = node.odometry.pose.pose.position.x
        current_y = node.odometry.pose.pose.position.y
        current_z = node.odometry.pose.pose.position.z

        target_x, target_y = node.target_position
        target_z = node.TAKEOFF_ALTITUDE

        dx = target_x - current_x
        dy = target_y - current_y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist <= node.TARGET_TOLERANCE:
            stop_msg = TwistStamped()
            stop_msg.header.stamp = node.get_clock().now().to_msg()
            stop_msg.header.frame_id = "base_link"
            stop_msg.twist.linear.x = 0.0
            stop_msg.twist.linear.y = 0.0
            stop_msg.twist.linear.z = 0.0
            node.cmd_vel_publisher.publish(stop_msg)

            node.pre_landing_position = (current_x, current_y, current_z)
            node.position_error = dist

            node.get_logger().info("=" * 60)
            node.get_logger().info(f"TARGET REACHED within tolerance! Distance: {dist:.3f} m <= {node.TARGET_TOLERANCE:.2f} m")
            node.get_logger().info(f"Actual coordinates before landing:")
            node.get_logger().info(f"  x_actual = {current_x:.3f} m, y_actual = {current_y:.3f} m, z_actual = {current_z:.3f} m")
            node.get_logger().info(f"Target coordinates:")
            node.get_logger().info(f"  x_target = {target_x:.3f} m, y_target = {target_y:.3f} m")
            node.get_logger().info(f"Positioning error e = {dist:.3f} m (allowed: <= 0.3 m)")
            node.get_logger().info("Stopping horizontal motion and switching to LAND mode...")
            node.get_logger().info("=" * 60)

            node.state = FlightState.LANDING
            return

        speed = self.kp_horizontal * dist
        speed = max(self.min_speed, min(self.max_speed, speed))

        vx = speed * (dx / dist)
        vy = -speed * (dy / dist)

        dz = target_z - current_z
        vz = max(-self.max_climb_rate, min(self.max_climb_rate, self.kp_altitude * dz))

        cmd_msg = TwistStamped()
        cmd_msg.header.stamp = node.get_clock().now().to_msg()
        cmd_msg.header.frame_id = "base_link"
        cmd_msg.twist.linear.x = vx
        cmd_msg.twist.linear.y = vy
        cmd_msg.twist.linear.z = vz
        cmd_msg.twist.angular.z = 0.0

        node.cmd_vel_publisher.publish(cmd_msg)

        now = time.monotonic()
        if now - self.last_log_time >= 1.0:
            self.last_log_time = now
            node.get_logger().info(
                f"Navigating: Pos=({current_x:.2f}, {current_y:.2f}, {current_z:.2f}) -> "
                f"Dist={dist:.2f} m | Vel=({vx:.2f}, {vy:.2f}) m/s"
            )
