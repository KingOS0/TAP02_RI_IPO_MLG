#include <rclcpp/rclcpp.hpp>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit_msgs/msg/collision_object.hpp>
#include <shape_msgs/msg/solid_primitive.hpp>
#include <geometry_msgs/msg/pose.hpp>
#include <thread>
#include <chrono>

int main(int argc, char ** argv)
{
    rclcpp::init(argc, argv);

    auto node = rclcpp::Node::make_shared("fanuc_planning_scene");

    moveit::planning_interface::PlanningSceneInterface planning_scene_interface;

    std::this_thread::sleep_for(std::chrono::seconds(2));

    moveit_msgs::msg::CollisionObject piece;

    piece.header.frame_id = "base_link";
    piece.id = "Pieza_manipulada";

    shape_msgs::msg::SolidPrimitive primitive;
    primitive.type = shape_msgs::msg::SolidPrimitive::BOX;

    primitive.dimensions.resize(3);
    primitive.dimensions[shape_msgs::msg::SolidPrimitive::BOX_X] = 0.20;
    primitive.dimensions[shape_msgs::msg::SolidPrimitive::BOX_Y] = 0.20;
    primitive.dimensions[shape_msgs::msg::SolidPrimitive::BOX_Z] = 0.20;

    geometry_msgs::msg::Pose piece_pose;

    piece_pose.position.x = 0.92;
    piece_pose.position.y = -0.90;
    piece_pose.position.z = 0.21;

    piece_pose.orientation.x = 0.0;
    piece_pose.orientation.y = 0.0;
    piece_pose.orientation.z = 0.0;
    piece_pose.orientation.w = 1.0;

    piece.primitives.push_back(primitive);
    piece.primitive_poses.push_back(piece_pose);

    piece.operation = moveit_msgs::msg::CollisionObject::ADD;

    planning_scene_interface.applyCollisionObject(piece);

    RCLCPP_INFO(node->get_logger(), "Collision object 'piece' added.");

    moveit_msgs::msg::CollisionObject table;

    table.header.frame_id = "base_link";
    table.id = "Mesa_final";

    shape_msgs::msg::SolidPrimitive table_primitive;
    table_primitive.type = shape_msgs::msg::SolidPrimitive::BOX;

    table_primitive.dimensions.resize(3);
    table_primitive.dimensions[shape_msgs::msg::SolidPrimitive::BOX_X] = 0.20;
    table_primitive.dimensions[shape_msgs::msg::SolidPrimitive::BOX_Y] = 0.50;
    table_primitive.dimensions[shape_msgs::msg::SolidPrimitive::BOX_Z] = 0.20;

    geometry_msgs::msg::Pose table_pose;

    table_pose.position.x = 0.95;
    table_pose.position.y = 0.95;
    table_pose.position.z = 0.11;

    table_pose.orientation.x = 0.0;
    table_pose.orientation.y = 0.0;
    table_pose.orientation.z = 0.0;
    table_pose.orientation.w = 1.0;

    table.primitives.push_back(table_primitive);
    table.primitive_poses.push_back(table_pose);

    table.operation = moveit_msgs::msg::CollisionObject::ADD;

    planning_scene_interface.applyCollisionObject(table);

    RCLCPP_INFO(node->get_logger(), "Collision object 'table' added.");
    moveit_msgs::msg::CollisionObject table2;

    table2.header.frame_id = "base_link";
    table2.id = "Mesa_origen";

    shape_msgs::msg::SolidPrimitive table2_primitive;
    table2_primitive.type = shape_msgs::msg::SolidPrimitive::CYLINDER;

    table2_primitive.dimensions.resize(2);
    table2_primitive.dimensions[shape_msgs::msg::SolidPrimitive::CYLINDER_HEIGHT] = 0.20;
    table2_primitive.dimensions[shape_msgs::msg::SolidPrimitive::CYLINDER_RADIUS] = 0.25;

    geometry_msgs::msg::Pose table2_pose;

    table2_pose.position.x = 0.91;
    table2_pose.position.y = -0.90;
    table2_pose.position.z = 0.01;

    table2_pose.orientation.x = 0.0;
    table2_pose.orientation.y = 0.0;
    table2_pose.orientation.z = 0.0;
    table2_pose.orientation.w = 1.0;

    table2.primitives.push_back(table2_primitive);
    table2.primitive_poses.push_back(table2_pose);

    table2.operation = moveit_msgs::msg::CollisionObject::ADD;

    planning_scene_interface.applyCollisionObject(table2);

    RCLCPP_INFO(node->get_logger(), "Collision object 'Mesa_origen' added.");

    moveit_msgs::msg::CollisionObject obstacle;

    obstacle.header.frame_id = "base_link";
    obstacle.id = "obstaculo";

    shape_msgs::msg::SolidPrimitive obstacle_primitive;
    obstacle_primitive.type = shape_msgs::msg::SolidPrimitive::CYLINDER;

    obstacle_primitive.dimensions.resize(2);
    obstacle_primitive.dimensions[shape_msgs::msg::SolidPrimitive::CYLINDER_HEIGHT] = 0.80;
    obstacle_primitive.dimensions[shape_msgs::msg::SolidPrimitive::CYLINDER_RADIUS] = 0.05;

    geometry_msgs::msg::Pose obstacle_pose;

    obstacle_pose.position.x = 0.97;
    obstacle_pose.position.y = 0.10;
    obstacle_pose.position.z = 0.31;

    obstacle_pose.orientation.x = 0.0;
    obstacle_pose.orientation.y = 0.0;
    obstacle_pose.orientation.z = 0.0;
    obstacle_pose.orientation.w = 1.0;

    obstacle.primitives.push_back(obstacle_primitive);
    obstacle.primitive_poses.push_back(obstacle_pose);

    obstacle.operation = moveit_msgs::msg::CollisionObject::ADD;

    planning_scene_interface.applyCollisionObject(obstacle);

    RCLCPP_INFO(node->get_logger(), "Collision object 'obstacle' added.");

    moveit_msgs::msg::CollisionObject obstacle2;

    obstacle2.header.frame_id = "base_link";
    obstacle2.id = "obstaculo_2";

    shape_msgs::msg::SolidPrimitive obstacle2_primitive;
    obstacle2_primitive.type = shape_msgs::msg::SolidPrimitive::CYLINDER;

    obstacle2_primitive.dimensions.resize(2);
    obstacle2_primitive.dimensions[shape_msgs::msg::SolidPrimitive::CYLINDER_HEIGHT] = 1.50;
    obstacle2_primitive.dimensions[shape_msgs::msg::SolidPrimitive::CYLINDER_RADIUS] = 0.025;

    geometry_msgs::msg::Pose obstacle2_pose;

    obstacle2_pose.position.x = 0.58;
    obstacle2_pose.position.y = -0.21;
    obstacle2_pose.position.z = 0.65;

    obstacle2_pose.orientation.x = 0.0;
    obstacle2_pose.orientation.y = 0.0;
    obstacle2_pose.orientation.z = 0.0;
    obstacle2_pose.orientation.w = 1.0;

    obstacle2.primitives.push_back(obstacle2_primitive);
    obstacle2.primitive_poses.push_back(obstacle2_pose);

    obstacle2.operation = moveit_msgs::msg::CollisionObject::ADD;

    planning_scene_interface.applyCollisionObject(obstacle2);

    RCLCPP_INFO(node->get_logger(), "Collision object 'obstaculo_2' added.");
    rclcpp::shutdown();

    return 0;
}