# Security Flow Diagram

This directory contains a comprehensive security incident response flow diagram that illustrates the process from initial intrusion to AI-powered response.

## Overview

The diagram shows the sequential flow through five key stages of security incident handling:

**Intrusion → Post-exploitation → Anomalies → SIEM → LLM**

## Diagram Components

### 1. **Intrusion** (Entry Point)
- **Color**: Red
- **Description**: Point of entry for security threats
- **Examples**:
  - Phishing attacks
  - System vulnerabilities exploitation
  - Compromised credentials usage

### 2. **Post-exploitation** (Malicious Activities)
- **Color**: Orange
- **Description**: Activities performed by attackers after initial access
- **Examples**:
  - Lateral movement within the network
  - Privilege escalation attempts
  - Persistence mechanisms installation

### 3. **Anomalies** (Detection Phase)
- **Color**: Teal
- **Description**: Unusual behaviors or events detected in the system
- **Examples**:
  - Sudden spikes in network traffic
  - Unauthorized file access attempts
  - System irregularities and suspicious patterns

### 4. **SIEM** (Analysis & Correlation)
- **Color**: Blue
- **Description**: Security Information and Event Management system
- **Functions**:
  - Centralized log collection
  - Event correlation and analysis
  - Alert generation and prioritization

### 5. **LLM** (AI-Powered Response)
- **Color**: Green
- **Description**: Large Language Model for advanced security analysis
- **Capabilities**:
  - Advanced contextual analysis
  - Intelligent hypothesis generation
  - Automated response recommendations

## Files

- `security_flow_diagram.png` - High-quality raster image (300 DPI)
- `security_flow_diagram.svg` - Scalable vector graphics format
- `README.md` - This documentation file

## Usage

### PNG Format
- Best for: Presentations, documents, web display
- High resolution (300 DPI) suitable for printing
- File size: ~293 KB

### SVG Format  
- Best for: Web applications, scalable displays
- Vector format that scales without quality loss
- Smaller file size: ~84 KB
- Can be embedded directly in HTML or modified programmatically

## Generation

The diagram was generated using the `generate_security_flow_diagram.py` script located in the project root. To regenerate or modify the diagram:

```bash
python3 generate_security_flow_diagram.py
```

## Integration

These diagrams can be easily integrated into:
- Security documentation
- Training materials
- Incident response procedures
- Presentation slides
- Web applications and dashboards

## Technical Details

- **Generated with**: Python 3.12 + Matplotlib
- **Image dimensions**: 4770 x 2970 pixels (PNG)
- **Color scheme**: Professional security-themed palette
- **Font**: Sans-serif for readability
- **Style**: Modern, clean design with rounded corners and professional spacing