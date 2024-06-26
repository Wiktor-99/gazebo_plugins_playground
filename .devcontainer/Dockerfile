FROM osrf/ros:iron-desktop
ARG ROS_DISTRO=iron
ARG USERNAME=ros
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV DEBIAN_FRONTEND=noninteractive
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3-pip
ENV DEBIAN_FRONTEND=dialog
ENV SHELL /bin/bash

RUN apt-get update && \
    sudo apt-get install -y lsb-release wget gnupg

ENV DEBIAN_FRONTEND=noninteractive
RUN sudo wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null && \
    sudo apt-get update -y && \
    sudo apt-get install -y \
    gz-harmonic git-core \
    bash-completion \
    ros-$ROS_DISTRO-xacro \
    ros-$ROS_DISTRO-teleop-twist-keyboard \
    ros-$ROS_DISTRO-gz-ros2-control \
    ros-$ROS_DISTRO-ros-gzharmonic-sim \
    ros-$ROS_DISTRO-ros-gzharmonic-bridge  \
    ros-$ROS_DISTRO-robot-localization \
    && rm -rf /var/lib/apt/lists/*

RUN . /opt/ros/${ROS_DISTRO}/setup.sh && \
    mkdir -p /sdformat_urdf/src && \
    cd /sdformat_urdf/src && \
    git clone --branch iron https://github.com/ros/sdformat_urdf.git && \
    cd /sdformat_urdf && \
    colcon build
ENV DEBIAN_FRONTEND=dialog

RUN echo "if [ -f /opt/ros/${ROS_DISTRO}/setup.bash ]; then source /opt/ros/${ROS_DISTRO}/setup.bash; fi" >> /home/$USERNAME/.bashrc \
    && echo "if [ -f /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash ]; then source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash; fi" >> /home/$USERNAME/.bashrc \
    && echo "if [ -f ${WORKSPACE}/install/setup.bash ]; then source ${WORKSPACE}/install/setup.bash; fi" >> /home/ros/.bashrc \
    && echo "if [ -f /sdformat_urdf/install/setup.bash ]; then source /sdformat_urdf/install/setup.bash; fi" >> /home/ros/.bashrc

USER $USERNAME
CMD ["/bin/bash"]