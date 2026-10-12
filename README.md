### 1. Запуск симулятора

~/fpv_labs/start_sim.sh
```
*(Зачекайте 10–15 секунд, доки завантажиться Gazebo та автопілот)*


### 2. Запуск автономного польоту
source /opt/ros/humble/setup.bash
source ~/fpv_labs/install/setup.bash
ros2 run fpv_lab2 flight_test


### 3. Зупинка всіх процесів симулятора
~/fpv_labs/stop_sim.sh
