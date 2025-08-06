import numpy as np
from python.hgr.core import HGR
from python.hgr.generators import generate_sphere_points, generate_noisy_tetrahedron, generate_torus_points
from python.crv.node import CRVNode

# Example CRV catalog builder for one realm and type
def build_crv_catalog():
    catalog = []
    node_id = 1

    # Sphere (Ideal) - Quantum realm example
    sphere_points = generate_sphere_points(4)  # For Tetrahedron vertices
    for idx, pos in enumerate(sphere_points):
        crv_val = HGR.crv_from_geometry('sphere', pos)
        stability = HGR.calculate_stability(crv_val)
        freq = HGR.assign_frequency(crv_val, 'quantum')
        node = CRVNode(
            node_id=node_id,
            solid='tetrahedron',
            node_type='vertex',
            position=pos,
            crv_name='Pi',
            crv_value=math.pi,
            crv_symbol='π',
            known_constant=True,
            realm='quantum',
            frequency=freq,
            proposed_name="",
            rune_concept=""
        )
        catalog.append(node)
        node_id += 1

    # Add more nodes from other generators/types (edges, faces, other solids)
    # For demonstration, generate a noisy tetrahedron node (perturbed)
    noisy_points = generate_noisy_tetrahedron(1, noise=0.2)
    pos = noisy_points[0]
    crv_val = HGR.crv_from_geometry('tetrahedron', pos)
    freq = HGR.assign_frequency(crv_val, 'quantum')
    node = CRVNode(
        node_id=node_id,
        solid='tetrahedron',
        node_type='edge',
        position=pos,
        crv_name='Taupi',
        crv_value=321.777750,  # Example from doc
        crv_symbol='τ^π',
        known_constant=False,
        realm='quantum',
        frequency=freq,
        proposed_name="Taupi",
        rune_concept="Psi"
    )
    catalog.append(node)
    node_id += 1

    # More generators: torus, dodecahedron, icosahedron, cross-realm intersection, etc.
    # ... (expand in production)

    return catalog

def export_crv_catalog(catalog, filename="crv_catalog.json"):
    import json
    nodes_dict = [node.to_dict() for node in catalog]
    with open(filename, "w") as f:
        json.dump(nodes_dict, f, indent=2)
