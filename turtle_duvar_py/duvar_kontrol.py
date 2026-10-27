import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class DuvarKontrolNode(Node):
    def __init__(self):
        super().__init__('duvar_kontrol')

        # Bonus: Parametreler
        self.declare_parameter('linear_speed', 2.0)
        self.declare_parameter('angular_speed', 1.5)
        self.declare_parameter('min_limit', 1.0)
        self.declare_parameter('max_limit', 10.0)

        # Abone: /turtle1/pose
        self.pose_sub = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # Yayıncı: /turtle1/cmd_vel
        self.cmd_pub = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.current_pose = None
        self.control_timer = self.create_timer(0.1, self.move_turtle)
        self.log_timer = self.create_timer(1.0, self.log_position)

    def pose_callback(self, msg: Pose):
        self.current_pose = msg

    def move_turtle(self):
        if self.current_pose is None:
            return

        linear_spd = self.get_parameter('linear_speed').value
        angular_spd = self.get_parameter('angular_speed').value
        min_lim = self.get_parameter('min_limit').value
        max_lim = self.get_parameter('max_limit').value

        twist = Twist()

        # Duvar sınırları kontrolü (1.0 altı veya 10.0 üstü)
        if (self.current_pose.x < min_lim or self.current_pose.x > max_lim or 
            self.current_pose.y < min_lim or self.current_pose.y > max_lim):
            twist.linear.x = 0.5
            twist.angular.z = angular_spd
        else:
            twist.linear.x = linear_spd
            twist.angular.z = 0.0

        self.cmd_pub.publish(twist)

    def log_position(self):
        if self.current_pose is not None:
            self.get_logger().info(
                f"Kaplumbağa Konumu -> X: {self.current_pose.x:.2f}, Y: {self.current_pose.y:.2f}"
            )

def main(args=None):
    rclpy.init(args=args)
    node = DuvarKontrolNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
