#!/usr/bin/env python3
"""
Example script showing how to integrate the security flow diagram generator
into other applications or workflows.
"""

import os
import sys

# Add the current directory to Python path to import the generator
sys.path.append(os.path.dirname(__file__))

try:
    from generate_security_flow_diagram import create_security_flow_diagram, save_diagram_formats
    import matplotlib.pyplot as plt
    
    def example_usage():
        """Example showing different ways to use the diagram generator."""
        
        print("Security Flow Diagram - Usage Examples")
        print("=" * 50)
        
        # Example 1: Generate with custom filename
        print("\n1. Generating diagram with custom filename...")
        fig = create_security_flow_diagram()
        png_path, svg_path = save_diagram_formats(fig, 'custom_security_flow')
        print(f"   Created: {os.path.basename(png_path)}")
        print(f"   Created: {os.path.basename(svg_path)}")
        plt.close(fig)
        
        # Example 2: Generate and show (if in interactive environment)
        print("\n2. Integration example - get figure object...")
        fig = create_security_flow_diagram()
        print("   Figure object created successfully")
        print("   Can be used for:")
        print("   - Embedding in larger reports")
        print("   - Custom modifications")
        print("   - Integration with other visualization tools")
        plt.close(fig)
        
        # Example 3: Batch generation
        print("\n3. Batch generation example...")
        formats = ['security_flow_v1', 'security_flow_v2']
        for fmt in formats:
            fig = create_security_flow_diagram()
            save_diagram_formats(fig, fmt)
            plt.close(fig)
        print(f"   Generated {len(formats)} diagram versions")
        
        print("\n" + "=" * 50)
        print("Examples completed successfully!")
        print("\nGenerated files are available in the 'diagrams' directory.")
        
    if __name__ == "__main__":
        example_usage()
        
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please ensure matplotlib and other dependencies are installed:")
    print("pip install matplotlib pillow")
except Exception as e:
    print(f"Error running examples: {e}")