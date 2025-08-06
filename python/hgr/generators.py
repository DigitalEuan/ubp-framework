import numpy as np

def generate_sphere_points(n_vertices: int) -> np.ndarray:
    """
    Generate points for a sphere using the Fibonacci lattice.
    Returns array of xyz positions.
    """
    indices = np.arange(0, n_vertices, dtype=float) + 0.5
    phi = np.arccos(1 - 2*indices/n_vertices)
    theta = np.pi * (1 + 5**0.5) * indices

    x = np.cos(theta) * np.sin(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(phi)
    return np.vstack((x, y, z)).T

def generate_noisy_tetrahedron(n_vertices: int, noise: float=0.1) -> np.ndarray:
    """
    Generate a noisy tetrahedron point cloud.
    """
    base = np.array([
        [1, 1, 1],
        [-1, -1, 1],
        [-1, 1, -1],
        [1, -1, -1]
    ])
    pts = []
    for _ in range(n_vertices):
        v = base[np.random.choice(4)]
        pts.append(v + np.random.normal(0, noise, 3))
    return np.array(pts)

def generate_torus_points(n_vertices: int, R: float=1.0, r: float=0.3) -> np.ndarray:
    """
    Generate points for a torus.
    """
    theta = np.linspace(0, 2*np.pi, n_vertices)
    phi = np.linspace(0, 2*np.pi, n_vertices)
    x = (R + r*np.cos(phi)) * np.cos(theta)
    y = (R + r*np.cos(phi)) * np.sin(theta)
    z = r * np.sin(phi)
    return np.vstack((x, y, z)).T
