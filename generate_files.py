#!/usr/bin/env python3
"""
Generate Chapter 1 index and all 11 diagram HTML files
"""

import os

# Chapter 1 Index HTML content
chapter1_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chapter 1: Cell - The Unit of Life | Plus One Biology</title>
    <link rel="stylesheet" href="../../css/base.css">
    <link rel="stylesheet" href="../../css/study-guide.css">
</head>
<body>
    <nav style="background: linear-gradient(135deg, #4169E1 0%, #0047AB 100%); padding: 15px 30px; color: white;">
        <a href="../../index.html" style="color: white; text-decoration: none; font-weight: 600;">← Back to Home</a>
        <span style="margin: 0 15px;">|</span>
        <span>Chapter 1: Cell - The Unit of Life</span>
    </nav>

    <div class="container" style="max-width: 1200px; margin: 40px auto; padding: 20px;">
        <h1 style="color: #4169E1; text-align: center; margin-bottom: 40px;">Cell - The Unit of Life</h1>

        <div style="background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%); padding: 30px; border-radius: 12px; margin-bottom: 40px;">
            <h2 style="color: #1B5E20; margin-bottom: 20px;">🎯 11 Interactive Diagrams</h2>
            <p style="color: #2E7D32; margin-bottom: 25px;">Explore each diagram for detailed, interactive learning:</p>

            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px;">
                <a href="diagrams/fluid-mosaic-model.html" class="card" style="text-decoration: none; border: 2px solid #4CAF50;">
                    <h4 style="color: #4169E1;">1. Fluid Mosaic Model</h4>
                    <p>Plasma membrane structure</p>
                </a>
                <a href="diagrams/mitochondria.html" class="card" style="text-decoration: none; border: 2px solid #4CAF50;">
                    <h4 style="color: #4169E1;">2. Mitochondria</h4>
                    <p>Powerhouse of the cell</p>
                </a>
                <a href="diagrams/chloroplast.html" class="card" style="text-decoration: none; border: 2px solid #4CAF50;">
                    <h4 style="color: #4169E1;">3. Chloroplast</h4>
                    <p>Photosynthesis site</p>
                </a>
                <a href="diagrams/nucleus.html" class="card" style="text-decoration: none; border: 2px solid #4CAF50;">
                    <h4 style="color: #4169E1;">4. Nucleus</h4>
                    <p>Genetic control center</p>
                </a>
                <a href="diagrams/plant-animal-cells.html" class="card" style="text-decoration: none; border: 2px solid #4CAF50;">
                    <h4 style="color: #4169E1;">5. Plant vs Animal Cells</h4>
                    <p>Comparison</p>
                </a>
                <a href="diagrams/rer-ser.html" class="card" style="text-decoration: none; border: 2px solid #4CAF50;">
                    <h4 style="color: #4169E1;">6. RER vs SER</h4>
                    <p>ER types</p>
                </a>
                <a href="diagrams/golgi-er.html" class="card" style="text-decoration: none; border: 2px solid #4CAF50;">
                    <h4 style="color: #4169E1;">7. Golgi + ER</h4>
                    <p>Endomembrane system</p>
                </a>
                <a href="diagrams/prokaryotic-cell.html" class="card" style="text-decoration: none; border: 2px solid #4CAF50;">
                    <h4 style="color: #4169E1;">8. Prokaryotic Cell</h4>
                    <p>Bacterial structure</p>
                </a>
                <a href="diagrams/chromosome-types.html" class="card" style="text-decoration: none; border: 2px solid #4CAF50;">
                    <h4 style="color: #4169E1;">9. Chromosome Types</h4>
                    <p>Centromere classification</p>
                </a>
                <a href="diagrams/plastids.html" class="card" style="text-decoration: none; border: 2px solid #4CAF50;">
                    <h4 style="color: #4169E1;">10. Plastids</h4>
                    <p>Types classification</p>
                </a>
                <a href="diagrams/cell-wall.html" class="card" style="text-decoration: none; border: 2px solid #4CAF50;">
                    <h4 style="color: #4169E1;">11. Cell Wall</h4>
                    <p>Three layers</p>
                </a>
            </div>
        </div>

        <div style="text-align: center; margin-top: 40px;">
            <a href="../../index.html" class="btn">← Back to Home</a>
        </div>
    </div>

    <footer style="background: #2C3E50; color: white; text-align: center; padding: 30px; margin-top: 60px;">
        <p>Chapter 1: Cell - The Unit of Life | Plus One Biology</p>
    </footer>
</body>
</html>'''

# Diagram HTML template
def create_diagram_html(title, description, component_name):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Interactive | Plus One Biology</title>
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <link rel="stylesheet" href="../../../css/base.css">
    <style>
        body {{ margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
        .back-button {{ position: fixed; top: 20px; left: 20px; background: white; color: #4169E1; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 1000; transition: all 0.3s; }}
        .back-button:hover {{ transform: translateY(-2px); box-shadow: 0 6px 16px rgba(0,0,0,0.2); text-decoration: none; }}
        #root {{ max-width: 1600px; margin: 0 auto; }}
    </style>
</head>
<body>
    <a href="../index.html" class="back-button">← Back to Chapter</a>
    <div id="root"></div>

    <script type="text/babel">
        const PlaceholderComponent = () => {{
            return (
                <div style={{{{
                    maxWidth: '800px',
                    margin: '60px auto',
                    padding: '40px',
                    background: 'white',
                    borderRadius: '12px',
                    boxShadow: '0 8px 32px rgba(0,0,0,0.15)',
                    textAlign: 'center'
                }}}}>
                    <h1 style={{{{ color: '#4169E1', marginBottom: '20px' }}}}>
                        {title}
                    </h1>
                    <p style={{{{ fontSize: '1.1rem', color: '#666', lineHeight: '1.8' }}}}>
                        {description}
                    </p>
                    <div style={{{{
                        background: '#FFF9E6',
                        borderLeft: '4px solid #FFC107',
                        padding: '20px',
                        borderRadius: '8px',
                        marginTop: '30px',
                        textAlign: 'left'
                    }}}}>
                        <h3 style={{{{ color: '#FF6F00', marginBottom: '15px' }}}}>📝 To Complete This Diagram:</h3>
                        <ol style={{{{ lineHeight: '2' }}}}>
                            <li>Copy JSX code from: <code>Docs/Cell-The-Unit-of-Life/chapter-images/interactive/{component_name}.jsx</code></li>
                            <li>Copy CSS from: <code>Docs/Cell-The-Unit-of-Life/chapter-images/interactive/{component_name}.css</code></li>
                            <li>Paste into this file replacing the PlaceholderComponent</li>
                            <li>Update React.useState to useState after adding: <code>const {{{{ useState, useRef }}}} = React;</code></li>
                        </ol>
                    </div>
                    <a href="../index.html" style={{{{
                        display: 'inline-block',
                        marginTop: '30px',
                        padding: '12px 32px',
                        background: '#4169E1',
                        color: 'white',
                        borderRadius: '8px',
                        textDecoration: 'none',
                        fontWeight: '600'
                    }}}}>Return to Chapter</a>
                </div>
            );
        }};

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<PlaceholderComponent />);
    </script>
</body>
</html>'''

# Diagram configurations
diagrams = [
    ('fluid-mosaic-model.html', 'Fluid Mosaic Model', 'Interactive plasma membrane structure showing phospholipid bilayer, proteins, and cholesterol', 'FluidMosaicInteractive'),
    ('mitochondria.html', 'Mitochondria', 'Powerhouse of the cell with cristae, matrix, and ATP synthesis sites', 'MitochondriaInteractive'),
    ('chloroplast.html', 'Chloroplast', 'Photosynthesis site showing grana, stroma, and thylakoids', 'ChloroplastInteractive'),
    ('nucleus.html', 'Nucleus', 'Genetic control center with nuclear envelope, chromatin, and nucleolus', 'NucleusInteractive'),
    ('plant-animal-cells.html', 'Plant vs Animal Cells', 'Side-by-side comparison highlighting unique and common features', 'PlantAnimalCellInteractive'),
    ('rer-ser.html', 'RER vs SER', 'Rough and Smooth Endoplasmic Reticulum comparison', 'RERSERInteractive'),
    ('golgi-er.html', 'Golgi + ER System', 'Endomembrane system with protein transport pathway', 'GolgiERInteractive'),
    ('prokaryotic-cell.html', 'Prokaryotic Cell', 'Bacterial cell structure with nucleoid, 70S ribosomes, and plasmids', 'ProkaryoticCellInteractive'),
    ('chromosome-types.html', 'Chromosome Types', 'Classification based on centromere position (4 types)', 'ChromosomeTypesInteractive'),
    ('plastids.html', 'Plastids Types', 'Chloroplasts, chromoplasts, and leucoplasts classification', 'PlastidsInteractive'),
    ('cell-wall.html', 'Cell Wall Structure', 'Three-layer system: middle lamella, primary, and secondary walls', 'CellWallInteractive'),
]

def main():
    base_dir = 'd:/Plus_One_Doc/Botany/Web/chapters/01-cell-the-unit-of-life'

    # Create Chapter 1 index
    print("Creating Chapter 1 index...")
    with open(f'{base_dir}/index.html', 'w', encoding='utf-8') as f:
        f.write(chapter1_html)
    print("[OK] Chapter 1 index created")

    # Create diagram directory if not exists
    diagrams_dir = f'{base_dir}/diagrams'
    os.makedirs(diagrams_dir, exist_ok=True)

    # Create all diagram HTMLs
    print(f"\nCreating {len(diagrams)} diagram files...")
    for filename, title, desc, component in diagrams:
        with open(f'{diagrams_dir}/{filename}', 'w', encoding='utf-8') as f:
            f.write(create_diagram_html(title, desc, component))
        print(f"[OK] Created {filename}")

    print(f"\n[SUCCESS] All files created successfully!")
    print(f"\nAccess your website at: http://localhost:8080/")

if __name__ == '__main__':
    main()
