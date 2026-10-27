# Duvardan Kaçan Kaplumbağa (ROS 2 Humble)

Bu ROS 2 paketi, `turtlesim` simülasyonundaki kaplumbağanın konumunu `/turtle1/pose` üzerinden dinler. Kaplumbağa sınır değerlere (x veya y < 1.0 ya da > 10.0) ulaştığında `/turtle1/cmd_vel` üzerinden açısal hız vererek duvardan kaçmasını sağlar ve saniyede bir mevcut koordinatları loglar.

## Kurulum ve Derleme

```bash
cd ~/ros2_ws
colcon build --packages-select turtle_duvar_py
source install/setup.bash
