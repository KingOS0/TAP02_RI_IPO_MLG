import numpy as np
import rclpy
from rclpy.node import Node
from moveit_msgs.srv import GetCartesianPath
from geometry_msgs.msg import Pose
from moveit_msgs.action import ExecuteTrajectory
from rclpy.action import ActionClient
from moveit_msgs.srv import ApplyPlanningScene
from moveit_msgs.msg import PlanningScene, AttachedCollisionObject, CollisionObject
from shape_msgs.msg import SolidPrimitive

prepick = np.array([0.942, 0.457, 1.116])
pick = np.array([0.966, 0.961, 0.430])



delta = pick - prepick
L = np.linalg.norm(delta)
direccion = delta / L

vmax = 0.100
amax = 0.020

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

print("\n--- PUNTO MEDIO 4D ---")
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

future_result = goal_handle.get_result_async()
rclpy.spin_until_future_complete(node, future_result)

print("Trayectoria quintica ejecutada")

cliente_scene = node.create_client(ApplyPlanningScene, "/apply_planning_scene")
cliente_scene.wait_for_service()

scene = PlanningScene()
scene.is_diff = True
scene.robot_state.is_diff = True

attached = AttachedCollisionObject()
attached.link_name = "tool0"
attached.object.id = "Pieza_manipulada"
attached.object.operation = CollisionObject.REMOVE

scene.robot_state.attached_collision_objects.append(attached)

pieza = CollisionObject()
pieza.header.frame_id = "base_link"
pieza.id = "Pieza_manipulada"
pieza.operation = CollisionObject.ADD

pieza.pose.position.x = 0.966
pieza.pose.position.y = 0.961
pieza.pose.position.z = 0.430
pieza.pose.orientation.w = 1.0

primitiva = SolidPrimitive()
primitiva.type = SolidPrimitive.BOX
primitiva.dimensions = [0.2, 0.2, 0.2]
pieza.primitives.append(primitiva)

req_scene = ApplyPlanningScene.Request()
req_scene.scene = scene

future_scene = cliente_scene.call_async(req_scene)
rclpy.spin_until_future_complete(node, future_scene)

print("Pieza_manipulada dejada en place")

node.destroy_node()
rclpy.shutdown()