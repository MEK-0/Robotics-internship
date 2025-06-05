from sympy import symbols, Matrix, cos, sin
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# DH Matrisi Hesaplama Fonksiyonu
def dh_matrix(theta, d, a, alpha):
    return Matrix([
        [cos(theta), -sin(theta)*cos(alpha),  sin(theta)*sin(alpha), a*cos(theta)],
        [sin(theta),  cos(theta)*cos(alpha), -cos(theta)*sin(alpha), a*sin(theta)],
        [0,           sin(alpha),             cos(alpha),            d],
        [0,           0,                      0,                     1]
    ])

# DH Parametrelerini kullanıcıdan al
def get_dh_parameters(n):
    dh_params = []
    for i in range(n):
        print(f"\nEklem {i+1} için DH parametreleri:")
        theta = float(input("  θ (derece): "))
        d = float(input("  d (birim): "))
        a = float(input("  a (birim): "))
        alpha = float(input("  α (derece): "))
        # Dereceden radyana çevir
        dh_params.append((math.radians(theta), d, a, math.radians(alpha)))
    return dh_params

# Pozisyonları hesapla
def compute_positions(dh_params):
    T = Matrix(np.identity(4))
    positions = [np.array([0, 0, 0])]
    for (theta, d, a, alpha) in dh_params:
        A = dh_matrix(theta, d, a, alpha)
        T = T * A
        pos = np.array(T[:3, 3]).astype(np.float64).flatten()
        positions.append(pos)
    return positions

# 3D Robot Kol Görselleştirme
def plot_robot_3d(positions):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x_vals = [p[0] for p in positions]
    y_vals = [p[1] for p in positions]
    z_vals = [p[2] for p in positions]

    ax.plot(x_vals, y_vals, z_vals, '-o', linewidth=3, markersize=8, color='royalblue')

    ax.set_title("3B N-DOF Robot Kol Simülasyonu")
    ax.set_xlabel("X ekseni")
    ax.set_ylabel("Y ekseni")
    ax.set_zlabel("Z ekseni")
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([0, 3])
    ax.view_init(elev=30, azim=45)
    plt.tight_layout()
    plt.show()

# Ana program
if __name__ == "__main__":
    print("🔧 N-DOF Robot Kol Simülasyonu (DH Parametreleri ile)")
    n = int(input("Kaç DOF'lu robot kolu istiyorsunuz? (örnek: 3): "))
    dh_params = get_dh_parameters(n)
    positions = compute_positions(dh_params)
    print("\n📍 Uç Efektör Pozisyonu (x, y, z):", positions[-1])
    plot_robot_3d(positions)
