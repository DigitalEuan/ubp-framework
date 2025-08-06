import pandas as pd

class CRVCatalog:
    """
    Loads and manages the CRV catalog from a CSV file.
    Allows access, editing, and expansion.
    """
    def __init__(self, csv_path="data/crv_catalog.csv"):
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)
    
    def get_node(self, node_id):
        """Return node as dict given Node_ID."""
        node = self.df[self.df["Node_ID"] == node_id]
        if node.empty:
            return None
        return node.to_dict(orient="records")[0]
    
    def get_by_column(self, column, value):
        """Return all nodes matching a column value."""
        return self.df[self.df[column] == value].to_dict(orient="records")
    
    def add_column(self, column_name, default=None):
        """Add a new column (keeps data compatible)."""
        if column_name not in self.df.columns:
            self.df[column_name] = default
    
    def set_value(self, node_id, column, value):
        """Edit a value for a node."""
        idx = self.df.index[self.df["Node_ID"] == node_id]
        if len(idx) == 0:
            return False
        self.df.at[idx[0], column] = value
        return True
    
    def save(self, path=None):
        """Save changes to CSV."""
        self.df.to_csv(path or self.csv_path, index=False)
    
    def all_nodes(self):
        """Return all nodes as dicts."""
        return self.df.to_dict(orient="records")
