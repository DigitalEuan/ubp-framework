"""
RGDL V3.3 - Fixed Import/Export System
Restores working DXF/STL functionality from V2
"""

import numpy as np
import struct
import os
import json
from pathlib import Path
import trimesh

class WorkingImportExportSystem:
    """
    Restored import/export system with working DXF/STL support
    """
    
    def __init__(self):
        self.supported_formats = {
            'import': ['.dxf', '.stl', '.rgdl2'],
            'export': ['.dxf', '.stl', '.rgdl2', '.json']
        }
        
    def import_file(self, file_path):
        """Import file with proper format detection"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        extension = file_path.suffix.lower()
        
        if extension == '.dxf':
            return self.import_dxf(file_path)
        elif extension == '.stl':
            return self.import_stl(file_path)
        elif extension == '.rgdl2':
            return self.import_rgdl2(file_path)
        else:
            raise ValueError(f"Unsupported import format: {extension}")
            
    def export_file(self, geometry_data, file_path, format_type=None):
        """Export geometry with proper format handling"""
        file_path = Path(file_path)
        
        if format_type is None:
            extension = file_path.suffix.lower()
        else:
            extension = format_type.lower()
            if not extension.startswith('.'):
                extension = '.' + extension
                
        if extension == '.dxf':
            return self.export_dxf(geometry_data, file_path)
        elif extension == '.stl':
            return self.export_stl(geometry_data, file_path)
        elif extension == '.rgdl2':
            return self.export_rgdl2(geometry_data, file_path)
        elif extension == '.json':
            return self.export_json(geometry_data, file_path)
        else:
            raise ValueError(f"Unsupported export format: {extension}")
            
    def import_dxf(self, file_path):
        """Import DXF file with proper entity parsing"""
        print(f"Importing DXF file: {file_path}")
        
        try:
            entities = []
            current_entity = {}
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                # DXF group codes
                if line.isdigit():
                    group_code = int(line)
                    if i + 1 < len(lines):
                        value = lines[i + 1].strip()
                        
                        # Entity type
                        if group_code == 0:
                            if current_entity:
                                entities.append(current_entity)
                            current_entity = {'type': value}
                            
                        # Coordinates
                        elif group_code == 10:  # X coordinate
                            current_entity['x'] = float(value)
                        elif group_code == 20:  # Y coordinate
                            current_entity['y'] = float(value)
                        elif group_code == 30:  # Z coordinate
                            current_entity['z'] = float(value)
                            
                        # Line endpoints
                        elif group_code == 11:  # X2 coordinate
                            current_entity['x2'] = float(value)
                        elif group_code == 21:  # Y2 coordinate
                            current_entity['y2'] = float(value)
                        elif group_code == 31:  # Z2 coordinate
                            current_entity['z2'] = float(value)
                            
                        # Circle/Arc properties
                        elif group_code == 40:  # Radius
                            current_entity['radius'] = float(value)
                        elif group_code == 50:  # Start angle
                            current_entity['start_angle'] = float(value)
                        elif group_code == 51:  # End angle
                            current_entity['end_angle'] = float(value)
                            
                        # Layer
                        elif group_code == 8:
                            current_entity['layer'] = value
                            
                    i += 2
                else:
                    i += 1
                    
            # Add last entity
            if current_entity:
                entities.append(current_entity)
                
            # Filter out non-geometric entities
            geometric_entities = []
            for entity in entities:
                if entity.get('type') in ['LINE', 'CIRCLE', 'ARC', 'POLYLINE', 'LWPOLYLINE', 'POINT']:
                    geometric_entities.append(entity)
                    
            print(f"DXF imported successfully: {len(geometric_entities)} entities")
            
            if geometric_entities:
                return self.convert_dxf_to_geometry(geometric_entities)
            else:
                print("No geometric entities found in DXF")
                return None
                
        except Exception as e:
            print(f"Error importing DXF: {e}")
            return None
            
    def convert_dxf_to_geometry(self, entities):
        """Convert DXF entities to 3D geometry"""
        vertices = []
        faces = []
        
        for entity in entities:
            entity_type = entity.get('type', '').upper()
            
            if entity_type == 'LINE':
                # Convert line to vertices
                x1, y1 = entity.get('x', 0), entity.get('y', 0)
                z1 = entity.get('z', 0)
                x2, y2 = entity.get('x2', 0), entity.get('y2', 0)
                z2 = entity.get('z2', 0)
                
                vertices.extend([[x1, y1, z1], [x2, y2, z2]])
                
            elif entity_type == 'CIRCLE':
                # Convert circle to polygon approximation
                x, y = entity.get('x', 0), entity.get('y', 0)
                z = entity.get('z', 0)
                radius = entity.get('radius', 1)
                
                # Create circle as polygon with 16 sides
                num_sides = 16
                circle_vertices = []
                for i in range(num_sides):
                    angle = 2 * np.pi * i / num_sides
                    cx = x + radius * np.cos(angle)
                    cy = y + radius * np.sin(angle)
                    circle_vertices.append([cx, cy, z])
                    
                vertices.extend(circle_vertices)
                
                # Create faces for circle
                center_idx = len(vertices)
                vertices.append([x, y, z])  # Center point
                
                for i in range(num_sides):
                    next_i = (i + 1) % num_sides
                    face = [center_idx, center_idx - num_sides + i, center_idx - num_sides + next_i]
                    faces.append(face)
                    
        if vertices:
            return {
                'vertices': np.array(vertices),
                'faces': np.array(faces) if faces else None,
                'type': 'imported_dxf',
                'entity_count': len(entities)
            }
        else:
            return None
            
    def import_stl(self, file_path):
        """Import STL file with proper binary/ASCII detection"""
        print(f"Importing STL file: {file_path}")
        
        try:
            # Try to determine if file is binary or ASCII
            with open(file_path, 'rb') as f:
                header = f.read(80)
                
            # Check if it's ASCII STL
            try:
                header_text = header.decode('utf-8', errors='strict')
                if 'solid' in header_text.lower():
                    # Might be ASCII, try to read as text
                    return self.import_stl_ascii(file_path)
            except UnicodeDecodeError:
                pass
                
            # Try binary STL
            return self.import_stl_binary(file_path)
            
        except Exception as e:
            print(f"Error importing STL: {e}")
            return None
            
    def import_stl_ascii(self, file_path):
        """Import ASCII STL file"""
        vertices = []
        faces = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            current_vertices = []
            
            for line in lines:
                line = line.strip().lower()
                
                if line.startswith('vertex'):
                    parts = line.split()
                    if len(parts) >= 4:
                        x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                        current_vertices.append([x, y, z])
                        
                elif line.startswith('endfacet'):
                    if len(current_vertices) == 3:
                        # Add vertices and create face
                        start_idx = len(vertices)
                        vertices.extend(current_vertices)
                        faces.append([start_idx, start_idx + 1, start_idx + 2])
                    current_vertices = []
                    
            if vertices:
                return {
                    'vertices': np.array(vertices),
                    'faces': np.array(faces),
                    'type': 'imported_stl_ascii',
                    'triangle_count': len(faces)
                }
            else:
                return None
                
        except Exception as e:
            print(f"Error reading ASCII STL: {e}")
            return None
            
    def import_stl_binary(self, file_path):
        """Import binary STL file"""
        try:
            with open(file_path, 'rb') as f:
                # Skip 80-byte header
                f.read(80)
                
                # Read number of triangles
                triangle_count = struct.unpack('<I', f.read(4))[0]
                
                vertices = []
                faces = []
                
                for i in range(triangle_count):
                    # Skip normal vector (12 bytes)
                    f.read(12)
                    
                    # Read 3 vertices (9 floats, 36 bytes)
                    triangle_vertices = []
                    for j in range(3):
                        x, y, z = struct.unpack('<fff', f.read(12))
                        triangle_vertices.append([x, y, z])
                        
                    # Skip attribute byte count (2 bytes)
                    f.read(2)
                    
                    # Add vertices and face
                    start_idx = len(vertices)
                    vertices.extend(triangle_vertices)
                    faces.append([start_idx, start_idx + 1, start_idx + 2])
                    
            if vertices:
                return {
                    'vertices': np.array(vertices),
                    'faces': np.array(faces),
                    'type': 'imported_stl_binary',
                    'triangle_count': len(faces)
                }
            else:
                return None
                
        except Exception as e:
            print(f"Error reading binary STL: {e}")
            return None
            
    def export_dxf(self, geometry_data, file_path):
        """Export geometry to DXF R2000 ASCII format"""
        print(f"Exporting DXF file: {file_path}")
        
        try:
            vertices = geometry_data.get('vertices', [])
            faces = geometry_data.get('faces', [])
            
            with open(file_path, 'w') as f:
                # DXF header
                f.write("0\\nSECTION\\n2\\nHEADER\\n")
                f.write("9\\n$ACADVER\\n1\\nAC1015\\n")  # AutoCAD 2000
                f.write("0\\nENDSEC\\n")
                
                # Tables section
                f.write("0\\nSECTION\\n2\\nTABLES\\n")
                f.write("0\\nTABLE\\n2\\nLAYER\\n70\\n1\\n")
                f.write("0\\nLAYER\\n2\\n0\\n70\\n0\\n62\\n7\\n6\\nCONTINUOUS\\n")
                f.write("0\\nENDTAB\\n0\\nENDSEC\\n")
                
                # Entities section
                f.write("0\\nSECTION\\n2\\nENTITIES\\n")
                
                if faces is not None and len(faces) > 0:
                    # Export as 3DFACE entities
                    for face in faces:
                        if len(face) >= 3:
                            v1, v2, v3 = vertices[face[0]], vertices[face[1]], vertices[face[2]]
                            
                            f.write("0\\n3DFACE\\n8\\n0\\n")
                            f.write(f"10\\n{v1[0]:.6f}\\n20\\n{v1[1]:.6f}\\n30\\n{v1[2]:.6f}\\n")
                            f.write(f"11\\n{v2[0]:.6f}\\n21\\n{v2[1]:.6f}\\n31\\n{v2[2]:.6f}\\n")
                            f.write(f"12\\n{v3[0]:.6f}\\n22\\n{v3[1]:.6f}\\n32\\n{v3[2]:.6f}\\n")
                            f.write(f"13\\n{v3[0]:.6f}\\n23\\n{v3[1]:.6f}\\n33\\n{v3[2]:.6f}\\n")
                else:
                    # Export vertices as points
                    for vertex in vertices:
                        f.write("0\\nPOINT\\n8\\n0\\n")
                        f.write(f"10\\n{vertex[0]:.6f}\\n20\\n{vertex[1]:.6f}\\n30\\n{vertex[2]:.6f}\\n")
                        
                f.write("0\\nENDSEC\\n0\\nEOF\\n")
                
            print(f"DXF exported successfully: {len(vertices)} vertices")
            return True
            
        except Exception as e:
            print(f"Error exporting DXF: {e}")
            return False
            
    def export_stl(self, geometry_data, file_path):
        """Export geometry to STL format"""
        print(f"Exporting STL file: {file_path}")
        
        try:
            vertices = geometry_data.get('vertices', [])
            faces = geometry_data.get('faces', [])
            
            if faces is None or len(faces) == 0:
                print("No faces to export to STL")
                return False
                
            # Export as binary STL
            with open(file_path, 'wb') as f:
                # 80-byte header
                header = b"RGDL V3.3 Generated STL" + b"\\0" * (80 - 23)
                f.write(header)
                
                # Number of triangles
                f.write(struct.pack('<I', len(faces)))
                
                for face in faces:
                    if len(face) >= 3:
                        v1, v2, v3 = vertices[face[0]], vertices[face[1]], vertices[face[2]]
                        
                        # Calculate normal vector
                        edge1 = v2 - v1
                        edge2 = v3 - v1
                        normal = np.cross(edge1, edge2)
                        normal = normal / (np.linalg.norm(normal) + 1e-10)
                        
                        # Write normal vector
                        f.write(struct.pack('<fff', normal[0], normal[1], normal[2]))
                        
                        # Write vertices
                        f.write(struct.pack('<fff', v1[0], v1[1], v1[2]))
                        f.write(struct.pack('<fff', v2[0], v2[1], v2[2]))
                        f.write(struct.pack('<fff', v3[0], v3[1], v3[2]))
                        
                        # Attribute byte count (unused)
                        f.write(struct.pack('<H', 0))
                        
            print(f"STL exported successfully: {len(faces)} triangles")
            return True
            
        except Exception as e:
            print(f"Error exporting STL: {e}")
            return False
            
    def import_rgdl2(self, file_path):
        """Import RGDL2 project file"""
        try:
            with open(file_path, 'r') as f:
                project_data = json.load(f)
                
            print(f"RGDL2 project loaded: {project_data.get('name', 'Unnamed')}")
            return project_data
            
        except Exception as e:
            print(f"Error importing RGDL2: {e}")
            return None
            
    def export_rgdl2(self, project_data, file_path):
        """Export RGDL2 project file"""
        try:
            with open(file_path, 'w') as f:
                json.dump(project_data, f, indent=2)
                
            print(f"RGDL2 project saved: {file_path}")
            return True
            
        except Exception as e:
            print(f"Error exporting RGDL2: {e}")
            return False
            
    def export_json(self, geometry_data, file_path):
        """Export geometry data as JSON"""
        try:
            # Convert numpy arrays to lists for JSON serialization
            export_data = {}
            for key, value in geometry_data.items():
                if isinstance(value, np.ndarray):
                    export_data[key] = value.tolist()
                else:
                    export_data[key] = value
                    
            with open(file_path, 'w') as f:
                json.dump(export_data, f, indent=2)
                
            print(f"JSON exported successfully: {file_path}")
            return True
            
        except Exception as e:
            print(f"Error exporting JSON: {e}")
            return False


class WorkingSaveLoadSystem:
    """
    Restored save/load functionality for projects
    """
    
    def __init__(self):
        self.current_project = None
        self.project_history = []
        
    def save_project(self, project_data, file_path):
        """Save complete project state"""
        try:
            # Ensure all numpy arrays are converted to lists
            serializable_data = self.make_serializable(project_data)
            
            with open(file_path, 'w') as f:
                json.dump(serializable_data, f, indent=2)
                
            print(f"Project saved: {file_path}")
            self.current_project = file_path
            return True
            
        except Exception as e:
            print(f"Error saving project: {e}")
            return False
            
    def load_project(self, file_path):
        """Load complete project state"""
        try:
            with open(file_path, 'r') as f:
                project_data = json.load(f)
                
            # Convert lists back to numpy arrays where appropriate
            restored_data = self.restore_numpy_arrays(project_data)
            
            print(f"Project loaded: {file_path}")
            self.current_project = file_path
            return restored_data
            
        except Exception as e:
            print(f"Error loading project: {e}")
            return None
            
    def make_serializable(self, data):
        """Convert numpy arrays and other non-serializable objects to JSON-compatible format"""
        if isinstance(data, dict):
            return {key: self.make_serializable(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.make_serializable(item) for item in data]
        elif isinstance(data, np.ndarray):
            return {
                '_numpy_array': True,
                'data': data.tolist(),
                'dtype': str(data.dtype),
                'shape': data.shape
            }
        elif isinstance(data, (np.integer, np.floating)):
            return float(data)
        else:
            return data
            
    def restore_numpy_arrays(self, data):
        """Restore numpy arrays from JSON-compatible format"""
        if isinstance(data, dict):
            if data.get('_numpy_array'):
                return np.array(data['data'], dtype=data['dtype']).reshape(data['shape'])
            else:
                return {key: self.restore_numpy_arrays(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.restore_numpy_arrays(item) for item in data]
        else:
            return data
            
    def auto_save(self, project_data, auto_save_dir="auto_saves"):
        """Automatic project backup"""
        try:
            os.makedirs(auto_save_dir, exist_ok=True)
            
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            auto_save_path = os.path.join(auto_save_dir, f"auto_save_{timestamp}.rgdl2")
            
            return self.save_project(project_data, auto_save_path)
            
        except Exception as e:
            print(f"Auto-save failed: {e}")
            return False


# Test the import/export system
if __name__ == "__main__":
    import_export = WorkingImportExportSystem()
    save_load = WorkingSaveLoadSystem()
    
    print("RGDL V3.3 Import/Export System Test")
    print("===================================")
    
    # Test DXF export
    test_geometry = {
        'vertices': np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]),
        'faces': np.array([[0, 1, 2], [0, 2, 3]]),
        'type': 'test_geometry'
    }
    
    print("Testing DXF export...")
    if import_export.export_dxf(test_geometry, "test_export.dxf"):
        print("✓ DXF export working")
    else:
        print("✗ DXF export failed")
        
    print("Testing STL export...")
    if import_export.export_stl(test_geometry, "test_export.stl"):
        print("✓ STL export working")
    else:
        print("✗ STL export failed")
        
    print("Testing project save...")
    test_project = {
        'name': 'Test Project',
        'geometry': test_geometry,
        'settings': {'material': 'steel', 'analysis_type': 'static'}
    }
    
    if save_load.save_project(test_project, "test_project.rgdl2"):
        print("✓ Project save working")
    else:
        print("✗ Project save failed")
        
    print("Testing project load...")
    loaded_project = save_load.load_project("test_project.rgdl2")
    if loaded_project:
        print("✓ Project load working")
    else:
        print("✗ Project load failed")
        
    print("\\nImport/Export system validation complete!")

