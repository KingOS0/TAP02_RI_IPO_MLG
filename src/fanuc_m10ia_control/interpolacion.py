import numpy as np
import rclpy
from rclpy.node import Node
from moveit_msgs.srv import GetCartesianPath
from geometry_msgs.msg import Pose
from moveit_msgs.action import ExecuteTrajectory
from rclpy.action import ActionClient
from moveit_msgs.srv import ApplyPlanningScene
from moveit_msgs.msg import PlanningScene, AttachedCollisionObject, CollisionObject
from moveit_msgs.srv import GetPlanningScene
from moveit_msgs.msg import AllowedCollisionEntry
import sys

prepick = np.array([0.927, -0.560, 0.927])
pick = np.array([0.918, -0.903, 0.322])

delta = pick - prepick
L = np.linalg.norm(delta)
direccion = delta / L

vmax = 0.200
amax = 0.300

Tc = max(1.5 * L / vmax, np.sqrt(6 * L / amax))
Tq = max(1.875 * L / vmax, np.sqrt((10 / np.sqrt(3)) * L / amax))

a0c = 0.0
a1c = 0.0
a2c = 3 * L / Tc**2
a3c = -2 * L / Tc**3

a0q = 0.0
a1q = 0.0
a2q = 0.0
a3q = 10 * L / Tq**3
a4q = -15 * L / Tq**4
a5q = 6 * L / Tq**5

tiempos_c = np.linspace(0, Tc, 5)
tiempos_q = np.linspace(0, Tq, 5)

waypoints_c = []
waypoints_q = []

print("\n--- CUBICA ---")

for t in tiempos_c:
    s = a0c + a1c*t + a2c*t**2 + a3c*t**3
    v = a1c + 2*a2c*t + 3*a3c*t**2
    acc = 2*a2c + 6*a3c*t
    posicion = prepick + direccion*s
    waypoints_c.append(posicion)
    print(f"t={t:.3f} XYZ={posicion} v={v:.3f} a={acc:.3f}")

print("\n--- QUINTICA ---")

for t in tiempos_q:
    s = a0q + a1q*t + a2q*t**2 + a3q*t**3 + a4q*t**4 + a5q*t**5
    v = a1q + 2*a2q*t + 3*a3q*t**2 + 4*a4q*t**3 + 5*a5q*t**4
    acc = 2*a2q + 6*a3q*t + 12*a4q*t**2 + 20*a5q*t**3
    posicion = prepick + direccion*s
    waypoints_q.append(posicion)
    print(f"t={t:.3f} XYZ={posicion} v={v:.3f} a={acc:.3f}")

rclpy.init()
node = Node("interpolacion_cartesiana")
cliente = node.create_client(GetCartesianPath, "/compute_cartesian_path")
cliente.wait_for_service()

request_c = GetCartesianPath.Request()
request_c.header.frame_id = "base_link"
request_c.group_name = "manipulator"
request_c.link_name = "tool0"
request_c.max_step = 0.01
request_c.jump_threshold = 0.0
request_c.avoid_collisions = True
request_c.max_velocity_scaling_factor = 1.0
request_c.max_acceleration_scaling_factor = 1.0

for p in waypoints_c:
    pose = Pose()
    pose.position.x = float(p[0])
    pose.position.y = float(p[1])
    pose.position.z = float(p[2])
    pose.orientation.x = 1.0
    pose.orientation.y = 0.0
    pose.orientation.z = -0.019
    pose.orientation.w = 0.0
    request_c.waypoints.append(pose)

future_c = cliente.call_async(request_c)
rclpy.spin_until_future_complete(node, future_c)
respuesta_c = future_c.result()

request_q = GetCartesianPath.Request()
request_q.header.frame_id = "base_link"
request_q.group_name = "manipulator"
request_q.link_name = "tool0"
request_q.max_step = 0.01
request_q.jump_threshold = 0.0
request_q.avoid_collisions = True
request_q.max_velocity_scaling_factor = 1.0
request_q.max_acceleration_scaling_factor = 1.0

for p in waypoints_q:
    pose = Pose()
    pose.position.x = float(p[0])
    pose.position.y = float(p[1])
    pose.position.z = float(p[2])
    pose.orientation.x = 1.0
    pose.orientation.y = 0.0
    pose.orientation.z = -0.019
    pose.orientation.w = 0.0
    request_q.waypoints.append(pose)

future_q = cliente.call_async(request_q)
rclpy.spin_until_future_complete(node, future_q)
respuesta_q = future_q.result()

print("\nFraccion cubica =", respuesta_c.fraction)
print("Fraccion quintica =", respuesta_q.fraction)

puntos_c = respuesta_c.solution.joint_trajectory.points
puntos_q = respuesta_q.solution.joint_trajectory.points
medio = len(puntos_q)//2
p = puntos_q[medio]

print("\n--- PUNTO MEDIO 4B ---")
print("q =", list(p.positions))
print("qdot =", list(p.velocities))

max_acc_c = 0.0
max_acc_q = 0.0

for p in puntos_c:
    if len(p.accelerations) > 0:
        max_acc_c = max(max_acc_c, max(abs(x) for x in p.accelerations))

for p in puntos_q:
    if len(p.accelerations) > 0:
        max_acc_q = max(max_acc_q, max(abs(x) for x in p.accelerations))

print("\nMax aceleracion articular cubica =", max_acc_c, "rad/s2")
print("Max aceleracion articular quintica =", max_acc_q, "rad/s2")

if max_acc_q < max_acc_c:
    print("Mejor perfil: QUINTICA")
else:
    print("Mejor perfil: CUBICA")
    
ejecutor = ActionClient(node, ExecuteTrajectory, "/execute_trajectory")
ejecutor.wait_for_server()

goal = ExecuteTrajectory.Goal()
goal.trajectory = respuesta_q.solution

future_goal = ejecutor.send_goal_async(goal)
rclpy.spin_until_future_complete(node, future_goal)

goal_handle = future_goal.result()

if goal_handle is None or not goal_handle.accepted:
    print("ERROR: MoveIt rechazo la ejecucion")
    node.destroy_node()
    rclpy.shutdown()
    exit()

future_result = goal_handle.get_result_async()
rclpy.spin_until_future_complete(node, future_result)

resultado = future_result.result()

if resultado is None:
    print("ERROR: No se recibio resultado de ejecucion")
    node.destroy_node()
    rclpy.shutdown()
    exit()

if resultado.result.error_code.val != 1:
    print("ERROR DE EJECUCION:", resultado.result.error_code.val)
    node.destroy_node()
    rclpy.shutdown()
    exit()

print("Trayectoria quintica ejecutada correctamente")

cliente_scene = node.create_client(ApplyPlanningScene, "/apply_planning_scene")
cliente_scene.wait_for_service()

scene = PlanningScene()
scene.is_diff = True
scene.robot_state.is_diff = True

attached = AttachedCollisionObject()
attached.link_name = "tool0"
attached.object.id = "Pieza_manipulada"
attached.object.operation = CollisionObject.ADD
attached.touch_links = ["tool0", "flange", "link_6", "link_5"]

scene.robot_state.attached_collision_objects.append(attached)

req_scene = ApplyPlanningScene.Request()
req_scene.scene = scene

future_scene = cliente_scene.call_async(req_scene)
rclpy.spin_until_future_complete(node, future_scene)

print("Pieza_manipulada unida al robot")

cliente_get_scene = node.create_client(GetPlanningScene, "/get_planning_scene")
cliente_get_scene.wait_for_service()

req_get = GetPlanningScene.Request()
req_get.components.components = 128

future_get = cliente_get_scene.call_async(req_get)
rclpy.spin_until_future_complete(node, future_get)

acm = future_get.result().scene.allowed_collision_matrix

for nombre in ["Pieza_manipulada", "Mesa_origen"]:
    if nombre not in acm.entry_names:
        n = len(acm.entry_names)
        acm.entry_names.append(nombre)

        for fila in acm.entry_values:
            fila.enabled.append(False)

        nueva_fila = AllowedCollisionEntry()
        nueva_fila.enabled = [False] * (n + 1)
        acm.entry_values.append(nueva_fila)

i = acm.entry_names.index("Pieza_manipulada")
j = acm.entry_names.index("Mesa_origen")

acm.entry_values[i].enabled[j] = True
acm.entry_values[j].enabled[i] = True

scene_acm = PlanningScene()
scene_acm.is_diff = True
scene_acm.allowed_collision_matrix = acm

req_acm = ApplyPlanningScene.Request()
req_acm.scene = scene_acm

future_acm = cliente_scene.call_async(req_acm)
rclpy.spin_until_future_complete(node, future_acm)

print("Contacto Pieza_manipulada - Mesa_origen permitido")

node.destroy_node()
rclpy.shutdown()
