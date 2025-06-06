import pybullet as p
import pybullet_data
import time

# PyBullet GUI başlat
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # URDF dosyaları için yol
p.setGravity(0, 0, -9.81)

# Zemin ve robot kolunu yükle
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("kuka_iiwa/model.urdf", useFixedBase=True)

# KUKA IIWA'da 7 hareketli eklem var
num_joints = p.getNumJoints(robotId)
print(f"Bu robot kolunda {num_joints} eklem var.")

# Kullanıcıdan açıları al (radyan cinsinden)
angles = []
for i in range(num_joints):
    deg = float(input(f"Eklem {i} için açı gir (°): "))
    rad = deg * 3.14159 / 180
    angles.append(rad)

# Eklemlere açıları uygula
for joint_index in range(num_joints):
    p.setJointMotorControl2(
        bodyIndex=robotId,
        jointIndex=joint_index,
        controlMode=p.POSITION_CONTROL,
        targetPosition=angles[joint_index],
        force=500
    )

# Simülasyonu çalıştır (pozisyona geçmesini gözlemlemek için)
for _ in range(240):
    p.stepSimulation()
    time.sleep(1./240.)

# Uç efektör pozisyonunu al ve göster
end_effector_state = p.getLinkState(robotId, num_joints - 1)
pos = end_effector_state[4]  # Pozisyon bilgisi
print(f"\nUç efektör pozisyonu: x={pos[0]:.3f}, y={pos[1]:.3f}, z={pos[2]:.3f}")

# Simülasyonu açık bırak (istersen kapatmak için Enter'a bas)
input("\nSimülasyonu kapatmak için Enter'a bas...")
p.disconnect()
