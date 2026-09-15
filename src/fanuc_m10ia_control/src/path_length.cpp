#include <rclcpp/rclcpp.hpp>
#include <moveit_msgs/msg/display_trajectory.hpp>
#include <cmath>

class PathLengthNode : public rclcpp::Node
{
public:
    PathLengthNode() : Node("path_length_node")
    {
        sub_ = create_subscription<moveit_msgs::msg::DisplayTrajectory>(
            "/display_planned_path",
            10,
            [this](const moveit_msgs::msg::DisplayTrajectory::SharedPtr msg)
            {
                if (msg->trajectory.empty())
                    return;

                const auto& points =
                    msg->trajectory[0].joint_trajectory.points;

                double length = 0.0;

                for (size_t i = 1; i < points.size(); i++)
                {
                    double segment = 0.0;

                    for (size_t j = 0; j < points[i].positions.size(); j++)
                    {
                        double dq =
                            points[i].positions[j] -
                            points[i - 1].positions[j];

                        segment += dq * dq;
                    }

                    length += std::sqrt(segment);
                }

                RCLCPP_INFO(
                    get_logger(),
                    "Path length = %.6f rad",
                    length);
            });
    }

private:
    rclcpp::Subscription<
        moveit_msgs::msg::DisplayTrajectory>::SharedPtr sub_;
};

int main(int argc, char** argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<PathLengthNode>());
    rclcpp::shutdown();
    return 0;
}