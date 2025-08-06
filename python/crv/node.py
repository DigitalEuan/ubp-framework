import numpy as np

class CRVNode:
    """
    Represents a Core Resonance Value (CRV) node in the UBP system.
    Contains geometric, mathematical, and physical attributes.
    """
    def __init__(
        self,
        node_id: int,
        solid: str,
        node_type: str,
        position: np.ndarray,
        crv_name: str,
        crv_value: float,
        crv_symbol: str,
        known_constant: bool,
        realm: str,
        frequency: float,
        proposed_name: str = "",
        rune_concept: str = ""
    ):
        self.node_id = node_id
        self.solid = solid
        self.node_type = node_type
        self.position = position
        self.crv_name = crv_name
        self.crv_value = crv_value
        self.crv_symbol = crv_symbol
        self.known_constant = known_constant
        self.realm = realm
        self.frequency = frequency
        self.proposed_name = proposed_name
        self.rune_concept = rune_concept

    def to_dict(self):
        return {
            "Node_ID": self.node_id,
            "Solid": self.solid,
            "Node_Type": self.node_type,
            "Position": self.position.tolist(),
            "CRV_Name": self.crv_name,
            "CRV_Value": self.crv_value,
            "CRV_Symbol": self.crv_symbol,
            "Known_Constant": self.known_constant,
            "Realm": self.realm,
            "Frequency": self.frequency,
            "Proposed_Name": self.proposed_name,
            "Rune_Concept": self.rune_concept
        }
