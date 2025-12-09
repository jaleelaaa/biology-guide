"""
integrate_components.py
Integrates actual React components (JSX + CSS) into diagram HTML files
"""

import os
import re

# Base directory paths
WEB_DIR = 'd:/Plus_One_Doc/Botany/Web'
SOURCE_DIR = 'd:/Plus_One_Doc/Botany/Docs/Cell-The-Unit-of-Life/chapter-images/interactive'
DIAGRAMS_DIR = f'{WEB_DIR}/chapters/01-cell-the-unit-of-life/diagrams'

# Mapping of HTML files to their source components
DIAGRAM_MAPPING = [
    {
        'html_file': 'fluid-mosaic-model.html',
        'jsx_file': 'FluidMosaicInteractive.jsx',
        'css_file': 'FluidMosaicInteractive.css',
        'component_name': 'FluidMosaicInteractive',
        'title': 'Fluid Mosaic Model - Interactive'
    },
    {
        'html_file': 'mitochondria.html',
        'jsx_file': 'MitochondriaInteractive.jsx',
        'css_file': 'MitochondriaInteractive.css',
        'component_name': 'MitochondriaInteractive',
        'title': 'Mitochondria Structure - Interactive'
    },
    {
        'html_file': 'chloroplast.html',
        'jsx_file': 'ChloroplastInteractive.jsx',
        'css_file': 'ChloroplastInteractive.css',
        'component_name': 'ChloroplastInteractive',
        'title': 'Chloroplast Structure - Interactive'
    },
    {
        'html_file': 'nucleus.html',
        'jsx_file': 'NucleusInteractive.jsx',
        'css_file': 'NucleusInteractive.css',
        'component_name': 'NucleusInteractive',
        'title': 'Nucleus Structure - Interactive'
    },
    {
        'html_file': 'plant-animal-cells.html',
        'jsx_file': 'PlantAnimalCellInteractive.jsx',
        'css_file': 'PlantAnimalCellInteractive.css',
        'component_name': 'PlantAnimalCellInteractive',
        'title': 'Plant vs Animal Cells - Interactive'
    },
    {
        'html_file': 'rer-ser.html',
        'jsx_file': 'RERSERInteractive.jsx',
        'css_file': 'RERSERInteractive.css',
        'component_name': 'RERSERInteractive',
        'title': 'RER vs SER - Interactive'
    },
    {
        'html_file': 'golgi-er.html',
        'jsx_file': 'GolgiERInteractive.jsx',
        'css_file': 'GolgiERInteractive.css',
        'component_name': 'GolgiERInteractive',
        'title': 'Golgi Apparatus & ER - Interactive'
    },
    {
        'html_file': 'prokaryotic-cell.html',
        'jsx_file': 'ProkaryoticCellInteractive.jsx',
        'css_file': 'ProkaryoticCellInteractive.css',
        'component_name': 'ProkaryoticCellInteractive',
        'title': 'Prokaryotic Cell - Interactive'
    },
    {
        'html_file': 'chromosome-types.html',
        'jsx_file': 'ChromosomeTypesInteractive.jsx',
        'css_file': 'ChromosomeTypesInteractive.css',
        'component_name': 'ChromosomeTypesInteractive',
        'title': 'Chromosome Types - Interactive'
    },
    {
        'html_file': 'plastids.html',
        'jsx_file': 'PlastidsInteractive.jsx',
        'css_file': 'PlastidsInteractive.css',
        'component_name': 'PlastidsInteractive',
        'title': 'Plastids Types - Interactive'
    },
    {
        'html_file': 'cell-wall.html',
        'jsx_file': 'CellWallInteractive.jsx',
        'css_file': 'CellWallInteractive.css',
        'component_name': 'CellWallInteractive',
        'title': 'Cell Wall Structure - Interactive'
    }
]


def read_file(file_path):
    """Read file content with fallback encodings"""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                content = f.read()
                # Replace any placeholder characters with proper ones
                content = content.replace('�', 'μ')  # Fix micrometer symbol
                return content
        except Exception as e:
            continue

    print(f"[ERROR] Failed to read {file_path} with any encoding")
    return None


def process_jsx_content(jsx_content):
    """
    Process JSX content to work in browser:
    - Remove import statements
    - Convert React.useState to useState with destructuring at top
    """
    # Remove import statements
    jsx_content = re.sub(r"^import\s+.*?;\s*$", "", jsx_content, flags=re.MULTILINE)

    # Add React hooks destructuring at the top
    hooks_declaration = "const { useState, useRef, useEffect } = React;\n\n"

    # Find where the component starts (after imports)
    lines = jsx_content.split('\n')
    component_start = 0
    for i, line in enumerate(lines):
        if line.strip() and not line.strip().startswith('/*') and not line.strip().startswith('*') and not line.strip().startswith('//') and not line.strip() == '*/':
            if 'const' in line or 'function' in line or 'class' in line:
                component_start = i
                break

    # Insert hooks declaration
    processed_lines = lines[:component_start] + [hooks_declaration] + lines[component_start:]

    return '\n'.join(processed_lines)


def create_integrated_html(diagram_info):
    """Create complete HTML file with integrated JSX and CSS"""

    jsx_path = f"{SOURCE_DIR}/{diagram_info['jsx_file']}"
    css_path = f"{SOURCE_DIR}/{diagram_info['css_file']}"

    # Read source files
    jsx_content = read_file(jsx_path)
    css_content = read_file(css_path)

    if not jsx_content or not css_content:
        print(f"[ERROR] Missing source files for {diagram_info['html_file']}")
        return None

    # Process JSX content
    jsx_content = process_jsx_content(jsx_content)

    # Create HTML template
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{diagram_info['title']} | Plus One Biology</title>
    <meta name="description" content="Interactive {diagram_info['title']} for Kerala Board Plus One Biology">

    <!-- React and Babel from CDN -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

    <!-- Base Styles -->
    <link rel="stylesheet" href="../../../css/base.css">

    <style>
        /* ============================================
           Back Button Styling
           ============================================ */
        body {{
            margin: 0;
            padding: 0;
        }}

        .back-button {{
            position: fixed;
            top: 20px;
            left: 20px;
            background: white;
            color: #4169E1;
            padding: 12px 24px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10000;
            transition: all 0.3s ease;
            border: 2px solid #4169E1;
        }}

        .back-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.2);
            background: #4169E1;
            color: white;
        }}

        /* ============================================
           Component Specific Styles
           ============================================ */
{css_content}
    </style>
</head>
<body>
    <!-- Back Navigation -->
    <a href="../index.html" class="back-button">← Back to Chapter</a>

    <!-- React Root -->
    <div id="root"></div>

    <!-- Component Code -->
    <script type="text/babel">
{jsx_content}

        // Render the component
        const container = document.getElementById('root');
        const root = ReactDOM.createRoot(container);
        root.render(<{diagram_info['component_name']} />);
    </script>
</body>
</html>'''

    return html_content


def main():
    print("=" * 60)
    print("INTEGRATING INTERACTIVE COMPONENTS")
    print("=" * 60)
    print(f"\nSource Directory: {SOURCE_DIR}")
    print(f"Target Directory: {DIAGRAMS_DIR}\n")

    success_count = 0
    failed_count = 0

    for diagram_info in DIAGRAM_MAPPING:
        print(f"Processing: {diagram_info['html_file']}...")

        html_content = create_integrated_html(diagram_info)

        if html_content:
            output_path = f"{DIAGRAMS_DIR}/{diagram_info['html_file']}"
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"  [OK] Created {diagram_info['html_file']}")
                success_count += 1
            except Exception as e:
                print(f"  [ERROR] Failed to write {diagram_info['html_file']}: {e}")
                failed_count += 1
        else:
            failed_count += 1

    print("\n" + "=" * 60)
    print("INTEGRATION COMPLETE")
    print("=" * 60)
    print(f"\n[SUCCESS] {success_count} files integrated successfully")
    if failed_count > 0:
        print(f"[FAILED] {failed_count} files failed")
    print(f"\nAll interactive diagrams are now live!")
    print(f"Access them at: http://localhost:8080/chapters/01-cell-the-unit-of-life/\n")


if __name__ == '__main__':
    main()
