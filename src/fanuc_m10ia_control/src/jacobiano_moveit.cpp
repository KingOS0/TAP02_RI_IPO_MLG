#include <rclcpp/rclcpp.hpp>

#include <moveit/robot_model_loader/robot_model_loader.h>
#include <moveit/robot_state/robot_state.h>

#include <Eigen/Core>

#include <iostream>
#include <vector>
#include <string>

int main(int argc, char** argv)
{
    rclcpp::init(argc, argv);

    auto node = rclcpp::Node::make_shared("jacobiano_moveit");

    robot_model_loader::RobotModelLoader robot_model_loader(node);

    moveit::core::RobotModelPtr robot_model =
        robot_model_loader.getModel();

    moveit::core::RobotState robot_state(robot_model);

    const moveit::core::JointModelGroup* joint_model_group =
        robot_model->getJointModelGroup("manipulator");

    const moveit::core::LinkModel* link_model =
        robot_model->getLinkModel("tool0");

    std::vector<std::string> nombres = {
        "PREPICK",
        "PICK",
        "PRE_PLACE",
        "PLACE"
    };

    std::vector<std::vector<double>> configuraciones = {

        {
            -0.5417750759524051,
             0.46047271225080777,
             0.21579062050232245,
             3.161468027539435,
             1.3585186541827539,
            -2.604341244084763
        },

        {
            -0.7752647813785839,
             1.1105386978136833,
             0.35293130240955367,
             3.177130932257688,
             0.8401946457796163,
            -2.390328130504908
        },

        {
             0.459276904895351,
             0.4012087905023365,
             0.4160061343874975,
            -3.0560897185874842,
             1.3279077240081203,
             2.6776838930620532
        },

        {
             0.7806358636969741,
             1.1995311919885967,
             0.6899406407535894,
             3.111631027448473,
             1.088190588062431,
            -2.9764161652134185
        }
    };

    for (size_t k = 0; k < configuraciones.size(); k++)
    {
        robot_state.setJointGroupPositions(
            joint_model_group,
            configuraciones[k]
        );

        robot_state.update();

        Eigen::MatrixXd jacobian;

        robot_state.getJacobian(
            joint_model_group,
            link_model,
            Eigen::Vector3d::Zero(),
            jacobian
        );

        std::cout << "\nJacobiano MoveIt en "
                  << nombres[k]
                  << ":\n";

        std::cout << jacobian << std::endl;
    }

    rclcpp::shutdown();

    return 0;
}