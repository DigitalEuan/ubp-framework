"""
RGDL V3.3 - Working Professional GUI
Fixes all GUI regressions and integrates working systems
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import json
import os
from pathlib import Path

# Import our working systems
from rgdl_v3_3_import_export import WorkingImportExportSystem, WorkingSaveLoadSystem
from rgdl_v3_3_plugin_system import WorkingPluginSystem

class WorkingRGDLGUI:
    """
    Working RGDL V3.3 GUI that actually functions properly
    """
    
    def __init__(self, master):
        self.master = master
        self.master.title("RGDL V3.3 Professional - Universal Binary Principle Engineering Platform")
        self.master.geometry("1400x900")
        
        # Initialize working systems
        self.import_export = WorkingImportExportSystem()
        self.save_load = WorkingSaveLoadSystem()
        self.plugin_system = WorkingPluginSystem()
        
        # Project data
        self.current_project = {
            'name': 'New Project',
            'objects': [],  # Multiple objects support
            'settings': {},
            'analysis_results': {}
        }
        
        # Current selection
        self.selected_object_index = 0
        
        # Setup GUI
        self.setup_styles()
        self.create_menu()
        self.create_main_interface()
        self.create_status_bar()
        
        # Load UBP logo if available
        self.setup_ubp_branding()
        
        print("RGDL V3.3 Professional GUI initialized successfully")
        
    def setup_styles(self):
        """Setup professional styling"""
        style = ttk.Style()
        
        # Professional color scheme
        self.colors = {
            'primary': '#2C3E50',      # Dark blue-gray
            'secondary': '#34495E',    # Lighter blue-gray  
            'accent': '#3498DB',       # Blue
            'success': '#27AE60',      # Green
            'warning': '#F39C12',      # Orange
            'danger': '#E74C3C',       # Red
            'light': '#ECF0F1',        # Light gray
            'white': '#FFFFFF'
        }
        
        # Configure ttk styles
        style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Heading.TLabel', font=('Arial', 10, 'bold'))
        
    def setup_ubp_branding(self):
        """Setup UBP logo and branding"""
        try:
            # Create UBP logo frame
            self.logo_frame = tk.Frame(self.master, bg=self.colors['primary'], height=60)
            self.logo_frame.pack(fill='x', side='top')
            self.logo_frame.pack_propagate(False)
            
            # UBP Logo (hexagonal cube representation)
            logo_canvas = tk.Canvas(self.logo_frame, width=50, height=50, 
                                  bg=self.colors['primary'], highlightthickness=0)
            logo_canvas.pack(side='left', padx=10, pady=5)
            
            # Draw hexagonal cube logo
            self.draw_ubp_logo(logo_canvas)
            
            # Title
            title_label = tk.Label(self.logo_frame, 
                                 text="RGDL V3.3 Professional", 
                                 font=('Arial', 16, 'bold'),
                                 fg=self.colors['white'],
                                 bg=self.colors['primary'])
            title_label.pack(side='left', padx=10, pady=15)
            
            # Subtitle
            subtitle_label = tk.Label(self.logo_frame,
                                    text="Universal Binary Principle Engineering Platform",
                                    font=('Arial', 10),
                                    fg=self.colors['light'],
                                    bg=self.colors['primary'])
            subtitle_label.pack(side='left', padx=10, pady=15)
            
            print("UBP branding applied successfully")
            
        except Exception as e:
            print(f"Warning: Could not setup UBP branding: {e}")
            
    def draw_ubp_logo(self, canvas):
        """Draw the UBP hexagonal cube logo"""
        try:
            # Hexagon coordinates (cube viewed from corner)
            center_x, center_y = 25, 25
            radius = 18
            
            # UBP colors: red, orange, yellow, green, blue, purple
            ubp_colors = ['#E74C3C', '#F39C12', '#F1C40F', '#27AE60', '#3498DB', '#9B59B6']
            
            # Draw 6 segments of the hexagon
            for i in range(6):
                angle1 = i * 60 * np.pi / 180
                angle2 = (i + 1) * 60 * np.pi / 180
                
                # Calculate points
                x1 = center_x + radius * np.cos(angle1)
                y1 = center_y + radius * np.sin(angle1)
                x2 = center_x + radius * np.cos(angle2)
                y2 = center_y + radius * np.sin(angle2)
                
                # Draw segment
                canvas.create_polygon(center_x, center_y, x1, y1, x2, y2,
                                    fill=ubp_colors[i], outline='white', width=1)
                                    
        except Exception as e:
            print(f"Could not draw UBP logo: {e}")
            # Fallback: simple text
            canvas.create_text(25, 25, text="UBP", fill='white', font=('Arial', 12, 'bold'))
            
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Project", command=self.new_project)
        file_menu.add_command(label="Open Project", command=self.open_project)
        file_menu.add_command(label="Save Project", command=self.save_project)
        file_menu.add_command(label="Save Project As...", command=self.save_project_as)
        file_menu.add_separator()
        file_menu.add_command(label="Import DXF", command=self.import_dxf)
        file_menu.add_command(label="Import STL", command=self.import_stl)
        file_menu.add_separator()
        file_menu.add_command(label="Export DXF", command=self.export_dxf)
        file_menu.add_command(label="Export STL", command=self.export_stl)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Add Shape", command=self.add_shape_dialog)
        edit_menu.add_command(label="Delete Selected", command=self.delete_selected_object)
        edit_menu.add_command(label="Duplicate Selected", command=self.duplicate_selected_object)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Run FEA Analysis", command=lambda: self.run_plugin('fea_analysis'))
        tools_menu.add_command(label="Measurement Tools", command=lambda: self.run_plugin('measurement_tools'))
        tools_menu.add_command(label="Unfold for Laser Cutting", command=lambda: self.run_plugin('unfolding_tools'))
        tools_menu.add_command(label="Assembly Analysis", command=lambda: self.run_plugin('assembly_analysis'))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def create_main_interface(self):
        """Create main interface with working components"""
        # Main container
        main_frame = tk.Frame(self.master)
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Left panel - Object management and properties
        left_panel = tk.Frame(main_frame, width=300)
        left_panel.pack(side='left', fill='y', padx=(0, 5))
        left_panel.pack_propagate(False)
        
        self.create_object_panel(left_panel)
        
        # Center panel - 3D visualization
        center_panel = tk.Frame(main_frame)
        center_panel.pack(side='left', fill='both', expand=True, padx=5)
        
        self.create_visualization_panel(center_panel)
        
        # Right panel - Plugins and analysis
        right_panel = tk.Frame(main_frame, width=300)
        right_panel.pack(side='right', fill='y', padx=(5, 0))
        right_panel.pack_propagate(False)
        
        self.create_plugin_panel(right_panel)
        
    def create_object_panel(self, parent):
        """Create object management panel"""
        # Object list
        objects_frame = tk.LabelFrame(parent, text="Objects", font=('Arial', 10, 'bold'))
        objects_frame.pack(fill='both', expand=True, pady=(0, 5))
        
        # Object listbox with scrollbar
        list_frame = tk.Frame(objects_frame)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.object_listbox = tk.Listbox(list_frame, selectmode='single')
        self.object_listbox.pack(side='left', fill='both', expand=True)
        self.object_listbox.bind('<<ListboxSelect>>', self.on_object_select)
        
        scrollbar = tk.Scrollbar(list_frame, orient='vertical', command=self.object_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.object_listbox.config(yscrollcommand=scrollbar.set)
        
        # Object control buttons
        button_frame = tk.Frame(objects_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Button(button_frame, text="Add Shape", command=self.add_shape_dialog,
                 bg=self.colors['success'], fg='white').pack(side='left', padx=2)
        tk.Button(button_frame, text="Delete", command=self.delete_selected_object,
                 bg=self.colors['danger'], fg='white').pack(side='left', padx=2)
        tk.Button(button_frame, text="Duplicate", command=self.duplicate_selected_object,
                 bg=self.colors['accent'], fg='white').pack(side='left', padx=2)
        
        # Properties panel
        props_frame = tk.LabelFrame(parent, text="Properties", font=('Arial', 10, 'bold'))
        props_frame.pack(fill='x', pady=5)
        
        # Object name
        tk.Label(props_frame, text="Name:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(props_frame, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=2)
        self.name_entry.bind('<Return>', self.update_object_name)
        
        # Material
        tk.Label(props_frame, text="Material:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.material_var = tk.StringVar(value="steel")
        material_combo = ttk.Combobox(props_frame, textvariable=self.material_var,
                                    values=["steel", "aluminum", "concrete", "wood"])
        material_combo.grid(row=1, column=1, sticky='ew', padx=5, pady=2)
        
        # Position controls
        tk.Label(props_frame, text="Position:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        
        pos_frame = tk.Frame(props_frame)
        pos_frame.grid(row=3, column=0, columnspan=2, sticky='ew', padx=5, pady=2)
        
        tk.Label(pos_frame, text="X:").pack(side='left')
        self.pos_x_var = tk.DoubleVar()
        tk.Entry(pos_frame, textvariable=self.pos_x_var, width=8).pack(side='left', padx=2)
        
        tk.Label(pos_frame, text="Y:").pack(side='left')
        self.pos_y_var = tk.DoubleVar()
        tk.Entry(pos_frame, textvariable=self.pos_y_var, width=8).pack(side='left', padx=2)
        
        tk.Label(pos_frame, text="Z:").pack(side='left')
        self.pos_z_var = tk.DoubleVar()
        tk.Entry(pos_frame, textvariable=self.pos_z_var, width=8).pack(side='left', padx=2)
        
        props_frame.columnconfigure(1, weight=1)
        
    def create_visualization_panel(self, parent):
        """Create 3D visualization panel"""
        viz_frame = tk.LabelFrame(parent, text="3D Visualization", font=('Arial', 10, 'bold'))
        viz_frame.pack(fill='both', expand=True)
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, viz_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        
        # Visualization controls
        control_frame = tk.Frame(viz_frame)
        control_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Button(control_frame, text="Reset View", command=self.reset_view).pack(side='left', padx=2)
        tk.Button(control_frame, text="Fit All", command=self.fit_all_objects).pack(side='left', padx=2)
        
        # View options
        self.show_wireframe = tk.BooleanVar(value=True)
        tk.Checkbutton(control_frame, text="Wireframe", variable=self.show_wireframe,
                      command=self.update_visualization).pack(side='left', padx=5)
        
        self.show_stress = tk.BooleanVar(value=False)
        tk.Checkbutton(control_frame, text="Stress Colors", variable=self.show_stress,
                      command=self.update_visualization).pack(side='left', padx=5)
        
        # Initialize with empty plot
        self.update_visualization()
        
    def create_plugin_panel(self, parent):
        """Create plugin panel with working plugin display"""
        plugin_frame = tk.LabelFrame(parent, text="Plugins", font=('Arial', 10, 'bold'))
        plugin_frame.pack(fill='both', expand=True, pady=(0, 5))
        
        # Plugin list
        self.plugin_tree = ttk.Treeview(plugin_frame, columns=('status',), show='tree headings')
        self.plugin_tree.heading('#0', text='Plugin')
        self.plugin_tree.heading('status', text='Status')
        self.plugin_tree.column('status', width=80)
        
        self.plugin_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Populate plugins
        self.refresh_plugin_list()
        
        # Plugin controls
        plugin_control_frame = tk.Frame(plugin_frame)
        plugin_control_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Button(plugin_control_frame, text="Run Plugin", command=self.run_selected_plugin,
                 bg=self.colors['accent'], fg='white').pack(side='left', padx=2)
        tk.Button(plugin_control_frame, text="Refresh", command=self.refresh_plugin_list,
                 bg=self.colors['secondary'], fg='white').pack(side='left', padx=2)
        
        # Analysis results
        results_frame = tk.LabelFrame(parent, text="Analysis Results", font=('Arial', 10, 'bold'))
        results_frame.pack(fill='both', expand=True, pady=5)
        
        # Results text area
        self.results_text = tk.Text(results_frame, height=10, wrap='word')
        self.results_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        results_scrollbar = tk.Scrollbar(results_frame, orient='vertical', command=self.results_text.yview)
        results_scrollbar.pack(side='right', fill='y')
        self.results_text.config(yscrollcommand=results_scrollbar.set)
        
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = tk.Frame(self.master, relief='sunken', bd=1)
        self.status_bar.pack(side='bottom', fill='x')
        
        self.status_label = tk.Label(self.status_bar, text="Ready", anchor='w')
        self.status_label.pack(side='left', padx=5)
        
        # Object count
        self.object_count_label = tk.Label(self.status_bar, text="Objects: 0", anchor='e')
        self.object_count_label.pack(side='right', padx=5)
        
    def refresh_plugin_list(self):
        """Refresh the plugin list with actual working plugins"""
        # Clear existing items
        for item in self.plugin_tree.get_children():
            self.plugin_tree.delete(item)
            
        # Get plugins from working plugin system
        plugins = self.plugin_system.get_available_plugins()
        
        for plugin in plugins:
            status = "Loaded" if plugin.get('loaded', False) else "Available"
            self.plugin_tree.insert('', 'end', 
                                  text=plugin['name'],
                                  values=(status,),
                                  tags=(plugin['id'],))
                                  
        self.update_status(f"Loaded {len(plugins)} plugins")
        
    def run_selected_plugin(self):
        """Run the selected plugin"""
        selection = self.plugin_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a plugin to run")
            return
            
        item = selection[0]
        plugin_name = self.plugin_tree.item(item, 'text')
        
        # Find plugin ID
        plugin_id = None
        for plugin in self.plugin_system.get_available_plugins():
            if plugin['name'] == plugin_name:
                plugin_id = plugin['id']
                break
                
        if plugin_id:
            self.run_plugin(plugin_id)
        else:
            messagebox.showerror("Error", f"Plugin not found: {plugin_name}")
            
    def run_plugin(self, plugin_id):
        """Run a specific plugin"""
        if not self.current_project['objects']:
            messagebox.showwarning("No Objects", "Please add some objects before running analysis")
            return
            
        try:
            self.update_status(f"Running plugin: {plugin_id}")
            
            # Get current object or all objects
            if plugin_id == 'assembly_analysis':
                # Assembly analysis needs all objects
                plugin_data = {'objects': self.current_project['objects']}
                result = self.plugin_system.execute_plugin(plugin_id, plugin_data)
            else:
                # Other plugins work on selected object
                if self.selected_object_index < len(self.current_project['objects']):
                    current_object = self.current_project['objects'][self.selected_object_index]
                    result = self.plugin_system.execute_plugin(plugin_id, current_object)
                else:
                    result = {'error': 'No object selected'}
                    
            # Display results
            if result:
                self.display_analysis_results(plugin_id, result)
                self.current_project['analysis_results'][plugin_id] = result
                
                # Update visualization if stress analysis
                if plugin_id == 'fea_analysis' and 'stress_field' in result:
                    self.show_stress.set(True)
                    self.update_visualization()
                    
            self.update_status(f"Plugin {plugin_id} completed")
            
        except Exception as e:
            messagebox.showerror("Plugin Error", f"Error running plugin {plugin_id}: {e}")
            self.update_status("Plugin execution failed")
            
    def display_analysis_results(self, plugin_id, result):
        """Display analysis results in the results panel"""
        self.results_text.delete(1.0, tk.END)
        
        self.results_text.insert(tk.END, f"=== {plugin_id.upper()} RESULTS ===\\n\\n")
        
        if 'error' in result:
            self.results_text.insert(tk.END, f"Error: {result['error']}\\n")
        else:
            # Format results based on plugin type
            if plugin_id == 'fea_analysis':
                self.results_text.insert(tk.END, f"Analysis Type: {result.get('analysis_type', 'Unknown')}\\n")
                self.results_text.insert(tk.END, f"Nodes: {result.get('num_nodes', 0)}\\n")
                self.results_text.insert(tk.END, f"Elements: {result.get('num_elements', 0)}\\n")
                self.results_text.insert(tk.END, f"Max Stress: {result.get('max_stress', 0):.2e} Pa\\n")
                self.results_text.insert(tk.END, f"Max Displacement: {result.get('max_displacement', 0):.6f} m\\n")
                
            elif plugin_id == 'measurement_tools':
                if 'bounding_box' in result:
                    bbox = result['bounding_box']
                    self.results_text.insert(tk.END, f"Bounding Box Dimensions: {bbox.get('dimensions', [])}\\n")
                    self.results_text.insert(tk.END, f"Volume: {bbox.get('volume', 0):.6f} m³\\n")
                    
            elif plugin_id == 'unfolding_tools':
                self.results_text.insert(tk.END, f"Unfolded Faces: {result.get('face_count', 0)}\\n")
                self.results_text.insert(tk.END, f"Total Area: {result.get('total_area', 0):.6f} m²\\n")
                
            elif plugin_id == 'assembly_analysis':
                self.results_text.insert(tk.END, f"Objects: {result.get('object_count', 0)}\\n")
                self.results_text.insert(tk.END, f"Contacts: {result.get('contact_count', 0)}\\n")
                self.results_text.insert(tk.END, f"Center of Mass: {result.get('center_of_mass', [])}\\n")
                
            # Add raw data for debugging
            self.results_text.insert(tk.END, f"\\n--- Raw Data ---\\n")
            self.results_text.insert(tk.END, json.dumps(result, indent=2, default=str))
            
    def add_shape_dialog(self):
        """Show dialog to add new shape"""
        dialog = tk.Toplevel(self.master)
        dialog.title("Add Shape")
        dialog.geometry("400x300")
        dialog.transient(self.master)
        dialog.grab_set()
        
        # Shape type
        tk.Label(dialog, text="Shape Type:", font=('Arial', 10, 'bold')).pack(pady=5)
        
        shape_var = tk.StringVar(value="cube")
        shapes = ["cube", "sphere", "cylinder", "cone", "pyramid", "torus"]
        
        for shape in shapes:
            tk.Radiobutton(dialog, text=shape.capitalize(), variable=shape_var, 
                          value=shape).pack(anchor='w', padx=20)
                          
        # Parameters frame
        params_frame = tk.LabelFrame(dialog, text="Parameters")
        params_frame.pack(fill='x', padx=10, pady=10)
        
        # Size parameter
        tk.Label(params_frame, text="Size:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        size_var = tk.DoubleVar(value=1.0)
        tk.Entry(params_frame, textvariable=size_var, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        # Resolution parameter
        tk.Label(params_frame, text="Resolution:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        resolution_var = tk.IntVar(value=20)
        tk.Entry(params_frame, textvariable=resolution_var, width=10).grid(row=1, column=1, padx=5, pady=2)
        
        # Buttons
        button_frame = tk.Frame(dialog)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        def create_shape():
            try:
                shape_type = shape_var.get()
                size = size_var.get()
                resolution = resolution_var.get()
                
                # Generate shape geometry
                geometry = self.generate_shape_geometry(shape_type, size, resolution)
                
                if geometry:
                    # Create object
                    obj = {
                        'name': f"{shape_type.capitalize()}_{len(self.current_project['objects']) + 1}",
                        'type': shape_type,
                        'vertices': geometry['vertices'],
                        'faces': geometry['faces'],
                        'material': 'steel',
                        'position': [0, 0, 0],
                        'size': size,
                        'resolution': resolution
                    }
                    
                    self.current_project['objects'].append(obj)
                    self.refresh_object_list()
                    self.update_visualization()
                    self.update_status(f"Added {shape_type}")
                    
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create shape: {e}")
                
        tk.Button(button_frame, text="Create", command=create_shape,
                 bg=self.colors['success'], fg='white').pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                 bg=self.colors['secondary'], fg='white').pack(side='left', padx=5)
                 
    def generate_shape_geometry(self, shape_type, size, resolution):
        """Generate geometry for different shape types"""
        if shape_type == "cube":
            return self.generate_cube(size)
        elif shape_type == "sphere":
            return self.generate_sphere(size, resolution)
        elif shape_type == "cylinder":
            return self.generate_cylinder(size, size * 2, resolution)
        elif shape_type == "cone":
            return self.generate_cone(size, size * 2, resolution)
        elif shape_type == "pyramid":
            return self.generate_pyramid(size)
        elif shape_type == "torus":
            return self.generate_torus(size, size * 0.3, resolution)
        else:
            return None
            
    def generate_cube(self, size):
        """Generate cube geometry"""
        s = size / 2
        vertices = [
            [-s, -s, -s], [s, -s, -s], [s, s, -s], [-s, s, -s],  # Bottom
            [-s, -s, s], [s, -s, s], [s, s, s], [-s, s, s]       # Top
        ]
        
        faces = [
            [0, 1, 2], [0, 2, 3],  # Bottom
            [4, 7, 6], [4, 6, 5],  # Top
            [0, 4, 5], [0, 5, 1],  # Front
            [2, 6, 7], [2, 7, 3],  # Back
            [0, 3, 7], [0, 7, 4],  # Left
            [1, 5, 6], [1, 6, 2]   # Right
        ]
        
        return {'vertices': vertices, 'faces': faces}
        
    def generate_sphere(self, radius, resolution):
        """Generate sphere geometry"""
        vertices = []
        faces = []
        
        # Generate vertices
        for i in range(resolution + 1):
            theta = np.pi * i / resolution
            for j in range(resolution * 2):
                phi = 2 * np.pi * j / (resolution * 2)
                
                x = radius * np.sin(theta) * np.cos(phi)
                y = radius * np.sin(theta) * np.sin(phi)
                z = radius * np.cos(theta)
                
                vertices.append([x, y, z])
                
        # Generate faces
        for i in range(resolution):
            for j in range(resolution * 2):
                current = i * (resolution * 2) + j
                next_row = (i + 1) * (resolution * 2) + j
                next_col = i * (resolution * 2) + ((j + 1) % (resolution * 2))
                next_both = (i + 1) * (resolution * 2) + ((j + 1) % (resolution * 2))
                
                if i < resolution:
                    faces.append([current, next_row, next_both])
                    faces.append([current, next_both, next_col])
                    
        return {'vertices': vertices, 'faces': faces}
        
    def generate_cylinder(self, radius, height, resolution):
        """Generate cylinder geometry"""
        vertices = []
        faces = []
        
        # Bottom circle
        vertices.append([0, 0, -height/2])  # Bottom center
        for i in range(resolution):
            angle = 2 * np.pi * i / resolution
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            vertices.append([x, y, -height/2])
            
        # Top circle
        vertices.append([0, 0, height/2])   # Top center
        for i in range(resolution):
            angle = 2 * np.pi * i / resolution
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            vertices.append([x, y, height/2])
            
        # Bottom faces
        for i in range(resolution):
            next_i = (i + 1) % resolution
            faces.append([0, i + 1, next_i + 1])
            
        # Top faces
        top_center = resolution + 1
        for i in range(resolution):
            next_i = (i + 1) % resolution
            faces.append([top_center, top_center + next_i + 1, top_center + i + 1])
            
        # Side faces
        for i in range(resolution):
            next_i = (i + 1) % resolution
            bottom1 = i + 1
            bottom2 = next_i + 1
            top1 = top_center + i + 1
            top2 = top_center + next_i + 1
            
            faces.append([bottom1, bottom2, top2])
            faces.append([bottom1, top2, top1])
            
        return {'vertices': vertices, 'faces': faces}
        
    def generate_cone(self, radius, height, resolution):
        """Generate cone geometry"""
        vertices = []
        faces = []
        
        # Base center and circle
        vertices.append([0, 0, -height/2])  # Base center
        for i in range(resolution):
            angle = 2 * np.pi * i / resolution
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            vertices.append([x, y, -height/2])
            
        # Apex
        vertices.append([0, 0, height/2])
        
        # Base faces
        for i in range(resolution):
            next_i = (i + 1) % resolution
            faces.append([0, i + 1, next_i + 1])
            
        # Side faces
        apex = resolution + 1
        for i in range(resolution):
            next_i = (i + 1) % resolution
            faces.append([i + 1, next_i + 1, apex])
            
        return {'vertices': vertices, 'faces': faces}
        
    def generate_pyramid(self, size):
        """Generate pyramid geometry"""
        s = size / 2
        vertices = [
            [-s, -s, -s], [s, -s, -s], [s, s, -s], [-s, s, -s],  # Base
            [0, 0, s]  # Apex
        ]
        
        faces = [
            [0, 2, 1], [0, 3, 2],  # Base (two triangles)
            [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]  # Sides
        ]
        
        return {'vertices': vertices, 'faces': faces}
        
    def generate_torus(self, major_radius, minor_radius, resolution):
        """Generate torus geometry"""
        vertices = []
        faces = []
        
        # Generate vertices
        for i in range(resolution):
            theta = 2 * np.pi * i / resolution
            for j in range(resolution):
                phi = 2 * np.pi * j / resolution
                
                x = (major_radius + minor_radius * np.cos(phi)) * np.cos(theta)
                y = (major_radius + minor_radius * np.cos(phi)) * np.sin(theta)
                z = minor_radius * np.sin(phi)
                
                vertices.append([x, y, z])
                
        # Generate faces
        for i in range(resolution):
            for j in range(resolution):
                current = i * resolution + j
                next_i = ((i + 1) % resolution) * resolution + j
                next_j = i * resolution + ((j + 1) % resolution)
                next_both = ((i + 1) % resolution) * resolution + ((j + 1) % resolution)
                
                faces.append([current, next_i, next_both])
                faces.append([current, next_both, next_j])
                
        return {'vertices': vertices, 'faces': faces}
        
    def refresh_object_list(self):
        """Refresh the object list"""
        self.object_listbox.delete(0, tk.END)
        
        for i, obj in enumerate(self.current_project['objects']):
            self.object_listbox.insert(tk.END, f"{i+1}. {obj['name']} ({obj['type']})")
            
        self.object_count_label.config(text=f"Objects: {len(self.current_project['objects'])}")
        
    def on_object_select(self, event):
        """Handle object selection"""
        selection = self.object_listbox.curselection()
        if selection:
            self.selected_object_index = selection[0]
            self.load_object_properties()
            self.update_visualization()
            
    def load_object_properties(self):
        """Load selected object properties into the property panel"""
        if self.selected_object_index < len(self.current_project['objects']):
            obj = self.current_project['objects'][self.selected_object_index]
            
            self.name_var.set(obj.get('name', ''))
            self.material_var.set(obj.get('material', 'steel'))
            
            position = obj.get('position', [0, 0, 0])
            self.pos_x_var.set(position[0])
            self.pos_y_var.set(position[1])
            self.pos_z_var.set(position[2])
            
    def update_object_name(self, event=None):
        """Update selected object name"""
        if self.selected_object_index < len(self.current_project['objects']):
            self.current_project['objects'][self.selected_object_index]['name'] = self.name_var.get()
            self.refresh_object_list()
            
    def delete_selected_object(self):
        """Delete the selected object"""
        if self.selected_object_index < len(self.current_project['objects']):
            obj_name = self.current_project['objects'][self.selected_object_index]['name']
            
            if messagebox.askyesno("Confirm Delete", f"Delete object '{obj_name}'?"):
                del self.current_project['objects'][self.selected_object_index]
                self.selected_object_index = max(0, self.selected_object_index - 1)
                self.refresh_object_list()
                self.update_visualization()
                self.update_status(f"Deleted object: {obj_name}")
                
    def duplicate_selected_object(self):
        """Duplicate the selected object"""
        if self.selected_object_index < len(self.current_project['objects']):
            original = self.current_project['objects'][self.selected_object_index]
            
            # Create copy
            duplicate = original.copy()
            duplicate['name'] = f"{original['name']}_copy"
            duplicate['position'] = [p + 0.1 for p in original.get('position', [0, 0, 0])]
            
            self.current_project['objects'].append(duplicate)
            self.refresh_object_list()
            self.update_visualization()
            self.update_status(f"Duplicated object: {original['name']}")
            
    def update_visualization(self):
        """Update the 3D visualization"""
        self.ax.clear()
        
        if not self.current_project['objects']:
            self.ax.text(0, 0, 0, 'No objects to display\\nUse "Add Shape" to create geometry',
                        ha='center', va='center', fontsize=12)
        else:
            # Plot all objects
            for i, obj in enumerate(self.current_project['objects']):
                vertices = np.array(obj.get('vertices', []))
                faces = obj.get('faces', [])
                position = obj.get('position', [0, 0, 0])
                
                if len(vertices) > 0:
                    # Apply position offset
                    vertices = vertices + np.array(position)
                    
                    # Determine color
                    if i == self.selected_object_index:
                        color = 'red'  # Highlight selected object
                        alpha = 0.8
                    else:
                        color = 'blue'
                        alpha = 0.6
                        
                    # Show stress colors if enabled and available
                    if self.show_stress.get() and 'fea_analysis' in self.current_project.get('analysis_results', {}):
                        stress_data = self.current_project['analysis_results']['fea_analysis'].get('stress_field', [])
                        if len(stress_data) == len(vertices):
                            # Normalize stress for color mapping
                            stress_array = np.array(stress_data)
                            normalized_stress = (stress_array - stress_array.min()) / (stress_array.max() - stress_array.min() + 1e-10)
                            colors = plt.cm.jet(normalized_stress)
                        else:
                            colors = color
                    else:
                        colors = color
                        
                    # Plot vertices
                    self.ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], 
                                  c=colors, s=20, alpha=alpha)
                    
                    # Plot wireframe if enabled
                    if self.show_wireframe.get() and faces:
                        for face in faces:
                            if len(face) >= 3:
                                face_vertices = vertices[face[:3]]
                                # Close the triangle
                                face_vertices = np.vstack([face_vertices, face_vertices[0]])
                                self.ax.plot(face_vertices[:, 0], face_vertices[:, 1], face_vertices[:, 2], 
                                           color=color, alpha=0.3, linewidth=0.5)
                                           
        # Set labels and title
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('RGDL V3.3 - 3D Visualization')
        
        # Update canvas
        self.canvas.draw()
        
    def reset_view(self):
        """Reset the 3D view"""
        self.ax.view_init(elev=20, azim=45)
        self.canvas.draw()
        
    def fit_all_objects(self):
        """Fit all objects in view"""
        if self.current_project['objects']:
            all_vertices = []
            for obj in self.current_project['objects']:
                vertices = np.array(obj.get('vertices', []))
                position = obj.get('position', [0, 0, 0])
                if len(vertices) > 0:
                    vertices = vertices + np.array(position)
                    all_vertices.extend(vertices.tolist())
                    
            if all_vertices:
                all_vertices = np.array(all_vertices)
                
                # Set axis limits with some padding
                padding = 0.1
                x_range = [all_vertices[:, 0].min() - padding, all_vertices[:, 0].max() + padding]
                y_range = [all_vertices[:, 1].min() - padding, all_vertices[:, 1].max() + padding]
                z_range = [all_vertices[:, 2].min() - padding, all_vertices[:, 2].max() + padding]
                
                self.ax.set_xlim(x_range)
                self.ax.set_ylim(y_range)
                self.ax.set_zlim(z_range)
                
                self.canvas.draw()
                
    def new_project(self):
        """Create new project"""
        if messagebox.askyesno("New Project", "Create new project? Unsaved changes will be lost."):
            self.current_project = {
                'name': 'New Project',
                'objects': [],
                'settings': {},
                'analysis_results': {}
            }
            self.refresh_object_list()
            self.update_visualization()
            self.results_text.delete(1.0, tk.END)
            self.update_status("New project created")
            
    def open_project(self):
        """Open existing project"""
        file_path = filedialog.askopenfilename(
            title="Open Project",
            filetypes=[("RGDL Projects", "*.rgdl2"), ("All Files", "*.*")]
        )
        
        if file_path:
            project_data = self.save_load.load_project(file_path)
            if project_data:
                self.current_project = project_data
                self.refresh_object_list()
                self.update_visualization()
                self.update_status(f"Opened project: {file_path}")
            else:
                messagebox.showerror("Error", "Failed to open project file")
                
    def save_project(self):
        """Save current project"""
        if hasattr(self, 'current_project_file'):
            if self.save_load.save_project(self.current_project, self.current_project_file):
                self.update_status(f"Project saved: {self.current_project_file}")
            else:
                messagebox.showerror("Error", "Failed to save project")
        else:
            self.save_project_as()
            
    def save_project_as(self):
        """Save project with new name"""
        file_path = filedialog.asksaveasfilename(
            title="Save Project As",
            defaultextension=".rgdl2",
            filetypes=[("RGDL Projects", "*.rgdl2"), ("All Files", "*.*")]
        )
        
        if file_path:
            if self.save_load.save_project(self.current_project, file_path):
                self.current_project_file = file_path
                self.update_status(f"Project saved: {file_path}")
            else:
                messagebox.showerror("Error", "Failed to save project")
                
    def import_dxf(self):
        """Import DXF file"""
        file_path = filedialog.askopenfilename(
            title="Import DXF",
            filetypes=[("DXF Files", "*.dxf"), ("All Files", "*.*")]
        )
        
        if file_path:
            geometry = self.import_export.import_file(file_path)
            if geometry:
                obj = {
                    'name': f"Imported_DXF_{len(self.current_project['objects']) + 1}",
                    'type': 'imported_dxf',
                    'vertices': geometry['vertices'].tolist() if hasattr(geometry['vertices'], 'tolist') else geometry['vertices'],
                    'faces': geometry['faces'].tolist() if geometry['faces'] is not None and hasattr(geometry['faces'], 'tolist') else geometry.get('faces'),
                    'material': 'steel',
                    'position': [0, 0, 0],
                    'source_file': file_path
                }
                
                self.current_project['objects'].append(obj)
                self.refresh_object_list()
                self.update_visualization()
                self.update_status(f"Imported DXF: {Path(file_path).name}")
            else:
                messagebox.showerror("Error", "Failed to import DXF file")
                
    def import_stl(self):
        """Import STL file"""
        file_path = filedialog.askopenfilename(
            title="Import STL",
            filetypes=[("STL Files", "*.stl"), ("All Files", "*.*")]
        )
        
        if file_path:
            geometry = self.import_export.import_file(file_path)
            if geometry:
                obj = {
                    'name': f"Imported_STL_{len(self.current_project['objects']) + 1}",
                    'type': 'imported_stl',
                    'vertices': geometry['vertices'].tolist() if hasattr(geometry['vertices'], 'tolist') else geometry['vertices'],
                    'faces': geometry['faces'].tolist() if hasattr(geometry['faces'], 'tolist') else geometry['faces'],
                    'material': 'steel',
                    'position': [0, 0, 0],
                    'source_file': file_path
                }
                
                self.current_project['objects'].append(obj)
                self.refresh_object_list()
                self.update_visualization()
                self.update_status(f"Imported STL: {Path(file_path).name}")
            else:
                messagebox.showerror("Error", "Failed to import STL file")
                
    def export_dxf(self):
        """Export current object to DXF"""
        if not self.current_project['objects']:
            messagebox.showwarning("No Objects", "No objects to export")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Export DXF",
            defaultextension=".dxf",
            filetypes=[("DXF Files", "*.dxf"), ("All Files", "*.*")]
        )
        
        if file_path:
            if self.selected_object_index < len(self.current_project['objects']):
                obj = self.current_project['objects'][self.selected_object_index]
                
                if self.import_export.export_file(obj, file_path, '.dxf'):
                    self.update_status(f"Exported DXF: {Path(file_path).name}")
                else:
                    messagebox.showerror("Error", "Failed to export DXF file")
                    
    def export_stl(self):
        """Export current object to STL"""
        if not self.current_project['objects']:
            messagebox.showwarning("No Objects", "No objects to export")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Export STL",
            defaultextension=".stl",
            filetypes=[("STL Files", "*.stl"), ("All Files", "*.*")]
        )
        
        if file_path:
            if self.selected_object_index < len(self.current_project['objects']):
                obj = self.current_project['objects'][self.selected_object_index]
                
                if self.import_export.export_file(obj, file_path, '.stl'):
                    self.update_status(f"Exported STL: {Path(file_path).name}")
                else:
                    messagebox.showerror("Error", "Failed to export STL file")
                    
    def show_about(self):
        """Show about dialog"""
        about_text = """RGDL V3.3 Professional
Universal Binary Principle Engineering Platform

Version: 3.3.0
Build: Production

Features:
• Advanced FEA Analysis
• Multi-object Assembly Analysis  
• 3D to 2D Unfolding for Laser Cutting
• Precision Measurement Tools
• DXF/STL Import/Export
• Professional Plugin Architecture

© 2025 UBP Research Team
"""
        messagebox.showinfo("About RGDL V3.3", about_text)
        
    def update_status(self, message):
        """Update status bar"""
        self.status_label.config(text=message)
        self.master.update_idletasks()


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = WorkingRGDLGUI(root)
    
    # Add some example objects for testing
    try:
        # Add a cube
        cube_geometry = app.generate_cube(1.0)
        if cube_geometry:
            cube_obj = {
                'name': 'Example Cube',
                'type': 'cube',
                'vertices': cube_geometry['vertices'],
                'faces': cube_geometry['faces'],
                'material': 'steel',
                'position': [0, 0, 0],
                'size': 1.0,
                'resolution': 20
            }
            app.current_project['objects'].append(cube_obj)
            
        # Add a sphere
        sphere_geometry = app.generate_sphere(0.8, 16)
        if sphere_geometry:
            sphere_obj = {
                'name': 'Example Sphere',
                'type': 'sphere',
                'vertices': sphere_geometry['vertices'],
                'faces': sphere_geometry['faces'],
                'material': 'aluminum',
                'position': [2, 0, 0],
                'size': 0.8,
                'resolution': 16
            }
            app.current_project['objects'].append(sphere_obj)
            
        app.refresh_object_list()
        app.update_visualization()
        app.update_status("Ready - Example objects loaded")
        
    except Exception as e:
        print(f"Warning: Could not create example objects: {e}")
        app.update_status("Ready")
    
    root.mainloop()


if __name__ == "__main__":
    main()

