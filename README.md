# Parcial de Robótica - Ciclo Pick and Place con FANUC M-10iA 🤖

Este proyecto corresponde al parcial de robótica realizado con un robot **FANUC M-10iA** usando **ROS 2 Jazzy** y **MoveIt 2**.

## 📦 Estructura del Proyecto

El proyecto está dividido principalmente en tres paquetes:

*   `fanuc_m10ia_support`: Contiene el modelo del robot, incluyendo los archivos URDF/Xacro y las mallas visuales/colisiones (archivos STL).
*   `fanuc_m10ia_moveit_config`: Contiene la configuración de MoveIt generada (grupo `manipulator`, poses guardadas, configuración de planeación, límites articulares, etc.).
*   `fanuc_m10ia_control`: Contiene los códigos desarrollados para la práctica, como la configuración de la escena de colisión, el cálculo de longitud de trayectoria, la verificación del Jacobiano y los scripts para las trayectorias cartesianas.

---

## 🛠️ Instrucciones de Compilación

Para compilar el proyecto, abre una terminal en la carpeta raíz de tu *workspace* y ejecuta:

```bash
colcon build --symlink-install

source install/setup.bash

Sigue estos pasos en diferentes terminales (recuerda hacer el source en cada una) para evaluar todas las funcionalidades del proyecto:

1. Iniciar MoveIt 2 y RViz
Este comando carga el FANUC M-10iA en MoveIt, lo que permite visualizar el robot, usar las poses guardadas y planear trayectorias de forma gráfica:
ros2 launch fanuc_m10ia_moveit_config demo.launch.py

Cargar Escena de Planificación
ros2 run fanuc_m10ia_control planning_scene

Comparación de Planeadores
ros2 run fanuc_m10ia_control path_length

Acercamiento Fino (Pre-Pick a Pick)
python3 src/fanuc_m10ia_control/interpolacion.py

Acercamiento Fino (Pre-Place a Place)
python3 src/fanuc_m10ia_control/interpolacion_place.py

Validación del Jacobiano
ros2 run fanuc_m10ia_control jacobiano_moveit
