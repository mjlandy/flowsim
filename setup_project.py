#!/usr/bin/env python3
"""
Setup script for Agile Flow Metrics Simulation.
Run this after extracting the zip file to organize the project correctly.
"""

import os
import shutil

def setup_project():
    """Set up the project with correct file names."""
    print("Setting up Agile Flow Metrics Simulation...")
    
    # File mappings: source -> destination
    file_mappings = {
        'clean_models.py': 'models.py',
        'clean_visualization.py': 'visualization.py',
        'ui_components_fixed.py': 'ui_components.py',
        'callbacks_fixed.py': 'callbacks.py'
    }
    
    # Rename files
    for source, dest in file_mappings.items():
        if os.path.exists(source):
            print(f"Renaming {source} -> {dest}")
            if os.path.exists(dest):
                os.remove(dest)  # Remove existing file
            shutil.move(source, dest)
        else:
            print(f"Warning: {source} not found")
    
    # Update imports in files
    update_imports()
    
    print("\n✅ Project setup complete!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run the application: python app.py")
    print("3. Open browser to: http://127.0.0.1:8050")

def update_imports():
    """Update import statements in files."""
    print("Updating import statements...")
    
    # Update visualization.py imports
    if os.path.exists('visualization.py'):
        with open('visualization.py', 'r') as f:
            content = f.read()
        
        content = content.replace('from clean_models import FlowMetrics', 'from models import FlowMetrics')
        
        with open('visualization.py', 'w') as f:
            f.write(content)
        print("Updated imports in visualization.py")
    
    # Update callbacks.py imports
    if os.path.exists('callbacks.py'):
        with open('callbacks.py', 'r') as f:
            content = f.read()
        
        content = content.replace(
            'from clean_models import (',
            'from models import ('
        )
        content = content.replace(
            'from clean_visualization import FlowMetricsVisualizer, ParameterImpactDescriptor',
            'from visualization import FlowMetricsVisualizer, ParameterImpactDescriptor'
        )
        
        with open('callbacks.py', 'w') as f:
            f.write(content)
        print("Updated imports in callbacks.py")

if __name__ == "__main__":
    setup_project()