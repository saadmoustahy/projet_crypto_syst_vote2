#!/usr/bin/env python3
"""
Security Flow Diagram Generator

This script generates a clear and visually appealing flow diagram to illustrate 
the security process: Intrusion → Post-exploitation → Anomalies → SIEM → LLM.

The diagram is exported in both PNG and SVG formats for easy sharing and integration.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np
import os

def create_security_flow_diagram():
    """Create the security flow diagram with professional styling."""
    
    # Set up the figure with high DPI for quality
    fig, ax = plt.subplots(1, 1, figsize=(16, 10), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Define colors for different types of components
    colors = {
        'intrusion': '#FF6B6B',      # Red for threats
        'post_exploit': '#FF8E53',   # Orange for exploitation
        'anomalies': '#4ECDC4',      # Teal for detection
        'siem': '#45B7D1',           # Blue for analysis
        'llm': '#96CEB4',            # Green for AI/response
        'arrow': '#2C3E50',          # Dark blue for arrows
        'text': '#2C3E50'            # Dark blue for text
    }
    
    # Define the positions and sizes for each block
    blocks = [
        {'name': 'Intrusion', 'pos': (1, 3), 'color': colors['intrusion']},
        {'name': 'Post-exploitation', 'pos': (3, 3), 'color': colors['post_exploit']},
        {'name': 'Anomalies', 'pos': (5, 3), 'color': colors['anomalies']},
        {'name': 'SIEM', 'pos': (7, 3), 'color': colors['siem']},
        {'name': 'LLM', 'pos': (9, 3), 'color': colors['llm']}
    ]
    
    # Define descriptions for each block
    descriptions = {
        'Intrusion': 'Point of entry:\n• Phishing attacks\n• Vulnerabilities\n• Compromised credentials',
        'Post-exploitation': 'Malicious activities:\n• Lateral movement\n• Privilege escalation\n• Persistence mechanisms',
        'Anomalies': 'Unusual behaviors:\n• Traffic spikes\n• Unauthorized access\n• System irregularities',
        'SIEM': 'Centralized monitoring:\n• Log collection\n• Event correlation\n• Alert generation',
        'LLM': 'Advanced analysis:\n• Contextual analysis\n• Hypothesis generation\n• Automated responses'
    }
    
    # Draw the main flow blocks
    for i, block in enumerate(blocks):
        # Create rounded rectangle for each block
        rect = FancyBboxPatch(
            (block['pos'][0] - 0.4, block['pos'][1] - 0.3),
            0.8, 0.6,
            boxstyle="round,pad=0.05",
            facecolor=block['color'],
            edgecolor='white',
            linewidth=2,
            alpha=0.9
        )
        ax.add_patch(rect)
        
        # Add block title
        ax.text(block['pos'][0], block['pos'][1] + 0.1, block['name'],
                ha='center', va='center', fontsize=12, fontweight='bold',
                color='white', family='sans-serif')
        
        # Add description below each block
        ax.text(block['pos'][0], block['pos'][1] - 0.8, descriptions[block['name']],
                ha='center', va='top', fontsize=9,
                color=colors['text'], family='sans-serif',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8, edgecolor='lightgray'))
    
    # Draw arrows between blocks
    arrow_style = dict(arrowstyle='->', lw=3, color=colors['arrow'])
    
    for i in range(len(blocks) - 1):
        start_x = blocks[i]['pos'][0] + 0.4
        end_x = blocks[i + 1]['pos'][0] - 0.4
        y = blocks[i]['pos'][1]
        
        # Create arrow
        arrow = ConnectionPatch(
            (start_x, y), (end_x, y),
            "data", "data",
            **arrow_style
        )
        ax.add_patch(arrow)
    
    # Add title
    ax.text(5, 5.5, 'Security Incident Response Flow', 
            ha='center', va='center', fontsize=20, fontweight='bold',
            color=colors['text'], family='sans-serif')
    
    # Add subtitle
    ax.text(5, 5.1, 'From Initial Intrusion to AI-Powered Response', 
            ha='center', va='center', fontsize=14, style='italic',
            color=colors['text'], family='sans-serif')
    
    # Add flow direction indicator
    ax.text(5, 0.3, '← Flow Direction →', 
            ha='center', va='center', fontsize=12, fontweight='bold',
            color=colors['arrow'], family='sans-serif')
    
    plt.tight_layout()
    return fig

def save_diagram_formats(fig, base_filename='security_flow_diagram'):
    """Save the diagram in both PNG and SVG formats."""
    
    # Create diagrams directory if it doesn't exist
    diagrams_dir = os.path.join(os.path.dirname(__file__), 'diagrams')
    os.makedirs(diagrams_dir, exist_ok=True)
    
    # Save as PNG (high quality)
    png_path = os.path.join(diagrams_dir, f'{base_filename}.png')
    fig.savefig(png_path, format='png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print(f"PNG diagram saved to: {png_path}")
    
    # Save as SVG (vector format)
    svg_path = os.path.join(diagrams_dir, f'{base_filename}.svg')
    fig.savefig(svg_path, format='svg', bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print(f"SVG diagram saved to: {svg_path}")
    
    return png_path, svg_path

def main():
    """Main function to generate and save the security flow diagram."""
    print("Generating Security Flow Diagram...")
    
    # Create the diagram
    fig = create_security_flow_diagram()
    
    # Save in both formats
    png_path, svg_path = save_diagram_formats(fig)
    
    print("\nDiagram generation completed successfully!")
    print(f"Files created:")
    print(f"  - PNG: {png_path}")
    print(f"  - SVG: {svg_path}")
    print("\nThe diagram illustrates the security incident response flow:")
    print("1. Intrusion: Initial attack vectors")
    print("2. Post-exploitation: Attacker activities")
    print("3. Anomalies: Detection of unusual behaviors")
    print("4. SIEM: Centralized monitoring and correlation")
    print("5. LLM: AI-powered analysis and response")
    
    # Close the figure to free memory
    plt.close(fig)

if __name__ == "__main__":
    main()