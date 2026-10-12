#!/bin/bash
echo "Зупинка всіх процесів симуляції..."

pkill -9 -f "sim_vehicle.py" 2>/dev/null
pkill -9 -f "mavproxy.py" 2>/dev/null
pkill -9 -f "arducopter" 2>/dev/null
killall -9 xterm 2>/dev/null

pkill -9 -f "ign gazebo" 2>/dev/null
killall -9 ruby 2>/dev/null

pkill -9 -f "parameter_bridge" 2>/dev/null
pkill -9 -f "MicroXRCEAgent" 2>/dev/null
pkill -9 -f "flight_test" 2>/dev/null
echo "Симуляцію успішно зупинено."
