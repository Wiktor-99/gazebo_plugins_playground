from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
)
from launch.substitutions import (
    Command,
    LaunchConfiguration
)
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
import os


def generate_launch_description():
    simulation_bringup_path = get_package_share_directory('simulation_bringup')
    world_arguments = DeclareLaunchArgument(
        "world",
        default_value=os.path.join(simulation_bringup_path, "worlds", "tracked_vehicle_world.sdf"),
        description="Robot controller to start.",
    )

    sdf_file = os.path.join(simulation_bringup_path, 'models', 'tracked.sdf')

    with open(sdf_file, 'r') as infp:
        robot_description = infp.read()

    gazebo = IncludeLaunchDescription(
        os.path.join(get_package_share_directory("ros_gz_sim"), 'launch', 'gz_sim.launch.py'),
         launch_arguments=[('gz_args', ["-r -v 4 ", LaunchConfiguration('world')])]
    )

    ign_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="gz_bridge",
        ros_arguments=["-p", f"config_file:={os.path.join(simulation_bringup_path, 'config', 'ign_bridge.yaml')}"],
        output="screen",
    )

    robot_localization_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[
            os.path.join(simulation_bringup_path, 'config', 'ekf.yaml'),
            {'use_sim_time' : True}
        ]
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[
            {'robot_description': robot_description},
            {'use_sim_time' : True}

        ],
    )

    gazebo_spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        name="spawn_tracked_robot",
        arguments=["-name", "tracked_robot", "-topic", "robot_description", "-x", "2"],
        output="screen",
    )

    return LaunchDescription(
        [
            world_arguments,
            ign_bridge,
            gazebo,
            robot_localization_node,
            robot_state_publisher,
            gazebo_spawn_robot
        ])