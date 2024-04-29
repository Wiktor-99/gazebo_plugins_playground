from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
)
from launch.substitutions import (
    LaunchConfiguration,
)
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
import os


def generate_launch_description():
    simulation_bringup_path = get_package_share_directory('simulation_bringup')
    declared_arguments = [
        DeclareLaunchArgument(
            "world",
            default_value=os.path.join(simulation_bringup_path, "worlds", "default_world.sdf"),
            description="Robot controller to start.",
        )
    ]

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

    return LaunchDescription(
        declared_arguments +
        [
            ign_bridge,
            gazebo
        ])