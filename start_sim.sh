#!/bin/bash

export DISPLAY="${DISPLAY:-:0}"

$HOME/fpv_labs/stop_sim.sh >/dev/null 2>&1
sleep 1

echo " 1. Запуск Micro-XRCE-DDS-Agent..."
MicroXRCEAgent udp4 -p 2019 > /tmp/micro_xrce_agent.log 2>&1 &

echo " 2. Запуск Gazebo Sim..."
ign gazebo -v4 -r $HOME/ardupilot_gazebo/worlds/iris_arducopter_runway.world > /tmp/gazebo.log 2>&1 &
sleep 5

echo " 3. Запуск ros_gz_bridge для /odometry..."
source /opt/ros/humble/setup.bash
ros2 run ros_gz_bridge parameter_bridge '/model/iris/odometry@nav_msgs/msg/Odometry[ignition.msgs.Odometry' --ros-args -r /model/iris/odometry:=/odometry > /tmp/ros_gz_bridge.log 2>&1 &

echo " 4. Запуск ArduPilot SITL..."
cd $HOME/ardupilot/ArduCopter
sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON -N --enable-DDS --add-param-file=$HOME/ardupilot/Tools/autotest/default_params/gazebo-iris.parm --add-param-file=$HOME/ardupilot/Tools/ros2/ardupilot_sitl/config/default_params/dds_use_ns.parm --console
