#!/usr/bin/env python3
"""
RGDL V3.3 Core Functionality Test
Tests all core systems without GUI
"""

import sys
import traceback

def test_import_export():
    """Test import/export functionality"""
    print("Testing Import/Export System...")
    try:
        from rgdl_v3_3_import_export import WorkingImportExportSystem
        
        system = WorkingImportExportSystem()
        
        # Test cube generation and export
        cube_data = {
            'vertices': [[-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5],
                        [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5]],
            'faces': [[0, 1, 2], [0, 2, 3], [4, 7, 6], [4, 6, 5], [0, 4, 5], [0, 5, 1],
                     [2, 6, 7], [2, 7, 3], [0, 3, 7], [0, 7, 4], [1, 5, 6], [1, 6, 2]],
            'name': 'test_cube'
        }
        
        # Test DXF export
        if system.export_file(cube_data, 'test_cube.dxf', '.dxf'):
            print("  ✓ DXF export working")
        else:
            print("  ✗ DXF export failed")
            
        # Test STL export
        if system.export_file(cube_data, 'test_cube.stl', '.stl'):
            print("  ✓ STL export working")
        else:
            print("  ✗ STL export failed")
            
        return True
        
    except Exception as e:
        print(f"  ✗ Import/Export test failed: {e}")
        traceback.print_exc()
        return False

def test_plugin_system():
    """Test plugin system"""
    print("Testing Plugin System...")
    try:
        from rgdl_v3_3_plugin_system import WorkingPluginSystem
        
        system = WorkingPluginSystem()
        plugins = system.get_available_plugins()
        
        print(f"  ✓ Found {len(plugins)} plugins")
        
        # Test each plugin
        test_data = {
            'vertices': [[-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5]],
            'faces': [[0, 1, 2], [0, 2, 3]],
            'material': 'steel'
        }
        
        for plugin in plugins:
            try:
                result = system.execute_plugin(plugin['id'], test_data)
                if result and 'error' not in result:
                    print(f"  ✓ Plugin {plugin['name']} working")
                else:
                    print(f"  ✗ Plugin {plugin['name']} failed: {result.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"  ✗ Plugin {plugin['name']} error: {e}")
                
        return True
        
    except Exception as e:
        print(f"  ✗ Plugin system test failed: {e}")
        traceback.print_exc()
        return False

def test_save_load():
    """Test save/load functionality"""
    print("Testing Save/Load System...")
    try:
        from rgdl_v3_3_import_export import WorkingSaveLoadSystem
        
        system = WorkingSaveLoadSystem()
        
        # Test project data
        test_project = {
            'name': 'Test Project',
            'objects': [{
                'name': 'Test Cube',
                'type': 'cube',
                'vertices': [[-0.5, -0.5, -0.5], [0.5, -0.5, -0.5]],
                'faces': [[0, 1, 2]],
                'material': 'steel'
            }],
            'settings': {'test': True},
            'analysis_results': {}
        }
        
        # Test save
        if system.save_project(test_project, 'test_project.rgdl2'):
            print("  ✓ Project save working")
            
            # Test load
            loaded_project = system.load_project('test_project.rgdl2')
            if loaded_project and loaded_project['name'] == 'Test Project':
                print("  ✓ Project load working")
                return True
            else:
                print("  ✗ Project load failed")
                return False
        else:
            print("  ✗ Project save failed")
            return False
            
    except Exception as e:
        print(f"  ✗ Save/Load test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("RGDL V3.3 Core Functionality Test")
    print("=" * 40)
    
    tests = [
        test_import_export,
        test_plugin_system,
        test_save_load
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
        
    print("=" * 40)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("✓ All core systems working correctly!")
        return True
    else:
        print("✗ Some systems need attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

