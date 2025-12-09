"""
Convert Cell Study Guide Markdown to Complete HTML Study Notes
Uses markdown2 library for proper conversion
"""

import markdown2
import os

def read_study_guide(file_path):
    """Read the study guide markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def remove_interactive_resources(content):
    """Remove interactive learning resource blockquotes but preserve Static Diagram links"""
    import re

    # Pattern to match blockquotes containing "INTERACTIVE LEARNING RESOURCE"
    pattern = r'> ### 🎯 \*\*INTERACTIVE LEARNING RESOURCE\*\*.*?(?=\n(?!>)\n|---|\Z)'

    # Find all interactive resource blockquotes
    matches = list(re.finditer(pattern, content, flags=re.DOTALL))

    # Process each match from end to beginning (to preserve positions)
    for match in reversed(matches):
        blockquote_text = match.group(0)

        # Check if this blockquote contains a Static Diagram reference
        diagram_pattern = r'> \*\*📊 Static Diagram\*\*: (\[[^\]]+\]\([^)]+\))'
        diagram_match = re.search(diagram_pattern, blockquote_text)

        if diagram_match:
            # Extract the diagram link and place it after the blockquote as a standalone line
            diagram_link = diagram_match.group(1)
            replacement = f'\n**🎯 Interactive Diagram**: {diagram_link}\n'
        else:
            replacement = ''

        # Replace the blockquote with the diagram link (or empty string)
        content = content[:match.start()] + replacement + content[match.end():]

    # Clean up multiple consecutive blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content

def remove_neet_questions(content):
    """Remove NEET PREVIOUS YEAR QUESTIONS section (available on separate exam questions page)"""
    import re

    # Pattern to match the specific "NEET PREVIOUS YEAR QUESTIONS" section
    # Matches from "## ... NEET PREVIOUS YEAR QUESTIONS" until next ## section or end
    pattern = r'## [^\n]*NEET PREVIOUS YEAR QUESTIONS[^\n]*\n.*?(?=\n## |\Z)'

    content = re.sub(pattern, '', content, flags=re.DOTALL)

    # Clean up multiple consecutive blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content

def convert_diagram_references(content):
    """Convert static DrawIO diagram references to interactive HTML diagram links"""
    import re

    # Mapping of DrawIO diagram files to interactive HTML diagrams
    # NOTE: Reference diagrams 03 & 04 cover prokaryotic cells (Figure 5.1 removed to avoid duplication)
    diagram_mapping = {
        # Reference Diagrams (numbered)
        '03_prokaryotic_cell_structure.drawio': ('diagrams/prokaryotic-cell.html', 'Prokaryotic Cell Structure (Interactive)'),
        '04_bacterial_cell_envelope.drawio': ('diagrams/prokaryotic-cell.html', 'Bacterial Cell Envelope (Interactive)'),
        '05_plant_vs_animal_cell_comparison.drawio': ('diagrams/plant-animal-cells.html', 'Plant vs Animal Cells (Interactive Comparison)'),
        '09_nucleus_structure.drawio': ('diagrams/nucleus.html', 'Nucleus Structure (Interactive)'),
        '10_endoplasmic_reticulum.drawio': ('diagrams/rer-ser.html', 'Endoplasmic Reticulum (Interactive)'),
        '11_golgi_apparatus.drawio': ('diagrams/golgi-er.html', 'Golgi Apparatus & ER Connection (Interactive)'),

        # Figure Diagrams (static versions → interactive)
        # Figure_5.1 removed - covered by reference diagrams 03 & 04 above
        'Figure_5.2_Plant_Cell.drawio': ('diagrams/plant-animal-cells.html', 'Plant Cell (Interactive)'),
        'Figure_5.12_Animal_Cell.drawio': ('diagrams/plant-animal-cells.html', 'Animal Cell (Interactive)'),
        'Figure_5.3_Fluid_Mosaic_Model.drawio': ('diagrams/fluid-mosaic-model.html', 'Fluid Mosaic Model (Interactive)'),
        'Figure_5.4_Cell_Wall.drawio': ('diagrams/cell-wall.html', 'Cell Wall Structure (Interactive)'),
        'Figure_5.5_RER_SER_Detailed.drawio': ('diagrams/rer-ser.html', 'RER vs SER (Interactive Comparison)'),
        'Figure_5.6_Golgi_ER.drawio': ('diagrams/golgi-er.html', 'Golgi & ER Connection (Interactive)'),
        'Figure_5.7_Mitochondria.drawio': ('diagrams/mitochondria.html', 'Mitochondria - The Powerhouse (Interactive)'),
        'Figure_5.8_Chloroplast.drawio': ('diagrams/chloroplast.html', 'Chloroplast Structure (Interactive)'),
        'Figure_5.9_Plastids.drawio': ('diagrams/plastids.html', 'Types of Plastids (Interactive)'),
        'Figure_5.10_Nucleus.drawio': ('diagrams/nucleus.html', 'Nucleus Structure (Interactive)'),
        'Figure_5.11_Chromosome_Types.drawio': ('diagrams/chromosome-types.html', 'Chromosome Types (Interactive)'),
    }

    # Pattern 1: **Reference Diagram**: See [text](path.drawio)
    # Pattern 2: - [text](path.drawio) (list items)
    # Pattern 3: > **📊 Static Diagram**: [text](path.drawio) (blockquotes)

    for drawio_file, (html_link, display_text) in diagram_mapping.items():
        # Replace all references to this DrawIO file with interactive HTML link
        # Pattern: [any text](../chapter-images/FILENAME.drawio)
        pattern = r'\[([^\]]+)\]\([^)]*' + re.escape(drawio_file) + r'\)'
        replacement = f'<a href="{html_link}" target="_blank">🎯 **{display_text}** - Click to Explore</a>'
        content = re.sub(pattern, replacement, content)

    # Remove "Static Diagram" labels since they're now interactive
    content = re.sub(r'> \*\*📊 Static Diagram\*\*:', '> **🎯 Interactive Diagram**:', content)
    content = re.sub(r'> \*\*📊 Static Diagrams\*\*:', '> **🎯 Interactive Diagrams**:', content)
    content = re.sub(r'- 📊 \*\*Static\*\*:', '- 🎯 **Interactive**:', content)
    content = re.sub(r'\*\*Reference Diagram\*\*:', '**🎯 Interactive Diagram**:', content)
    content = re.sub(r'\*\*Reference Diagrams\*\*:', '**🎯 Interactive Diagrams**:', content)

    # Convert plain text Figure references to interactive links
    figure_text_mapping = {
        # Figure 5.1 removed - covered by reference diagrams in main list
        'Figure 5.2 - Eukaryotic Plant Cell': 'diagrams/plant-animal-cells.html',
        'Figure 5.3 - Fluid Mosaic Model': 'diagrams/fluid-mosaic-model.html',
        'Figure 5.4 - Plant Cell Wall Structure': 'diagrams/cell-wall.html',
        'Figure 5.5 - Rough and Smooth Endoplasmic Reticulum': 'diagrams/rer-ser.html',
        'Figure 5.6 - Golgi Apparatus': 'diagrams/golgi-er.html',
        'Figure 5.7 - Mitochondria Structure': 'diagrams/mitochondria.html',
        'Figure 5.8 - Chloroplast Structure': 'diagrams/chloroplast.html',
        'Figure 5.9 - Types of Plastids': 'diagrams/plastids.html',
        'Figure 5.10 - Nucleus Structure': 'diagrams/nucleus.html',
        'Figure 5.11 - Chromosome Types': 'diagrams/chromosome-types.html',
        'Figure 5.12 - Eukaryotic Animal Cell': 'diagrams/plant-animal-cells.html',
    }

    for figure_text, diagram_link in figure_text_mapping.items():
        # Convert: *[Diagram reference: See Figure X.X - Name]* → **<a href="link" target="_blank">🎯 View Interactive Diagram</a>**
        pattern = r'\*\[Diagram reference: See ' + re.escape(figure_text) + r'\]\*'
        replacement = f'**<a href="{diagram_link}" target="_blank">🎯 View Interactive {figure_text}</a>**'
        content = re.sub(pattern, replacement, content)

    # Remove remaining non-essential DrawIO references that don't have interactive equivalents
    # Pattern: **🎯 Interactive Diagram**: See [text](../chapter-images/*.drawio)
    content = re.sub(r'\*\*🎯 Interactive Diagram\*\*: See \[[^\]]+\]\([^)]*\.drawio\)',
                     '', content)

    # Also remove standalone DrawIO links in paragraphs
    content = re.sub(r'\[[^\]]*\]\([^)]*chapter-images/[^)]*\.drawio\)',
                     '', content)

    # Remove empty "Interactive Diagram:" labels (labels without links after them)
    content = re.sub(r'\*\*🎯 Interactive Diagram\*\*:\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'> \*\*🎯 Interactive Diagram\*\*:\s*$', '', content, flags=re.MULTILINE)

    # Remove old FluidMosaicDemo.html references (duplicate interactive diagram)
    content = re.sub(r'- 🎮 \*\*Interactive\*\*: \[Fluid Mosaic Model Interactive Diagram\]\([^)]*FluidMosaicDemo\.html\)[^\n]*\n?', '', content)

    # Remove "Print-friendly version" suffix from diagram links
    content = re.sub(r' - Print-friendly version', '', content)

    # Clean up empty lines and extra whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content

def create_html_page(content):
    """Create complete HTML page with enhanced interactive styling"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Study Notes - Cell: The Unit of Life | Plus One Biology</title>
    <link rel="stylesheet" href="../../css/base.css">
    <!-- Distinctive Typography from Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Crimson+Text:wght@400;600;700&family=Space+Grotesk:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            /* Educational Science Theme - Organic & Professional */
            --color-primary: #2E7D32;
            --color-primary-light: #4CAF50;
            --color-secondary: #1565C0;
            --color-secondary-light: #42A5F5;
            --color-accent: #F57C00;
            --color-background: #FAFAF8;
            --color-surface: #FFFFFF;
            --color-text: #1A1A1A;
            --color-text-light: #4A4A4A;

            /* Typography */
            --font-display: 'Playfair Display', Georgia, serif;
            --font-body: 'Crimson Text', 'Times New Roman', serif;
            --font-heading: 'Space Grotesk', 'Segoe UI', sans-serif;

            /* Shadows & Effects */
            --shadow-sm: 0 2px 8px rgba(46, 125, 50, 0.1);
            --shadow-md: 0 4px 16px rgba(46, 125, 50, 0.15);
            --shadow-lg: 0 8px 32px rgba(46, 125, 50, 0.2);
            --glow-green: 0 0 20px rgba(76, 175, 80, 0.3);
            --glow-blue: 0 0 20px rgba(66, 165, 245, 0.3);
        }}

        * {{
            scroll-behavior: smooth;
        }}

        body {{
            font-family: var(--font-body);
            font-size: 18px;
            line-height: 1.9;
            color: var(--color-text);
            position: relative;
            /* Organic gradient mesh background */
            background:
                radial-gradient(circle at 10% 20%, rgba(76, 175, 80, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 90% 80%, rgba(66, 165, 245, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 50% 50%, rgba(245, 124, 0, 0.05) 0%, transparent 50%),
                linear-gradient(135deg, #FAFAF8 0%, #F5F3EF 100%);
            background-attachment: fixed;
        }}

        /* Subtle texture overlay */
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image:
                repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(46, 125, 50, 0.02) 2px, rgba(46, 125, 50, 0.02) 4px);
            pointer-events: none;
            z-index: 1;
        }}

        /* Reading Progress Bar */
        #progress-bar {{
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 4px;
            background: linear-gradient(90deg, #4CAF50 0%, #4169E1 100%);
            z-index: 10000;
            transition: width 0.1s ease;
        }}

        nav {{
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
            padding: 18px 40px;
            color: white;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: var(--shadow-lg);
            transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
            backdrop-filter: blur(10px);
            font-family: var(--font-heading);
        }}
        nav.scrolled {{
            padding: 12px 40px;
            box-shadow: 0 12px 36px rgba(46, 125, 50, 0.25);
            background: linear-gradient(135deg, rgba(46, 125, 50, 0.95) 0%, rgba(21, 101, 192, 0.95) 100%);
        }}
        nav a {{
            color: white;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.05rem;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            padding: 8px 16px;
            border-radius: 6px;
            letter-spacing: 0.3px;
        }}
        nav a:hover {{
            background: rgba(255,255,255,0.25);
            transform: translateY(-3px);
            box-shadow: 0 4px 12px rgba(255,255,255,0.2);
        }}

        /* Back to Top Button */
        #back-to-top {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #4169E1 0%, #0047AB 100%);
            color: white;
            border: none;
            border-radius: 50%;
            font-size: 24px;
            cursor: pointer;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            z-index: 999;
        }}
        #back-to-top.visible {{
            opacity: 1;
            visibility: visible;
        }}
        #back-to-top:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        }}

        /* Floating Table of Contents */
        #toc-toggle {{
            position: fixed;
            top: 80px;
            right: 20px;
            background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            z-index: 998;
            transition: all 0.3s ease;
        }}
        #toc-toggle:hover {{
            transform: scale(1.05);
            box-shadow: 0 6px 16px rgba(0,0,0,0.3);
        }}
        #toc-panel {{
            position: fixed;
            top: 130px;
            right: 20px;
            width: 280px;
            max-height: 70vh;
            background: white;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.15);
            padding: 20px;
            overflow-y: auto;
            opacity: 0;
            visibility: hidden;
            transform: translateX(20px);
            transition: all 0.3s ease;
            z-index: 997;
        }}
        #toc-panel.visible {{
            opacity: 1;
            visibility: visible;
            transform: translateX(0);
        }}
        #toc-panel h3 {{
            margin-top: 0;
            color: #4169E1;
            font-size: 1.2rem;
            border-bottom: 2px solid #4169E1;
            padding-bottom: 10px;
        }}
        #toc-panel ul {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        #toc-panel li {{
            margin: 8px 0;
        }}
        #toc-panel a {{
            color: #2C3E50;
            text-decoration: none;
            display: block;
            padding: 8px 12px;
            border-radius: 6px;
            transition: all 0.2s ease;
            font-size: 0.9rem;
        }}
        #toc-panel a:hover {{
            background: #E3F2FD;
            transform: translateX(5px);
        }}
        #toc-panel a.active {{
            background: linear-gradient(135deg, #4169E1 0%, #0047AB 100%);
            color: white;
        }}

        .container {{
            max-width: 1100px;
            margin: 50px auto;
            padding: 60px;
            background: var(--color-surface);
            border-radius: 24px;
            box-shadow: var(--shadow-lg);
            animation: fadeInUp 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
            position: relative;
            z-index: 2;
            border: 1px solid rgba(76, 175, 80, 0.1);
        }}
        .container::before {{
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(135deg, var(--color-primary-light), var(--color-secondary-light), var(--color-accent));
            border-radius: 24px;
            opacity: 0;
            z-index: -1;
            transition: opacity 0.6s ease;
        }}
        .container:hover::before {{
            opacity: 0.05;
        }}

        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        h1 {{
            font-family: var(--font-display);
            color: var(--color-primary);
            font-size: 3rem;
            font-weight: 700;
            letter-spacing: -0.5px;
            border-bottom: 5px solid var(--color-primary-light);
            padding-bottom: 20px;
            margin-bottom: 40px;
            animation: slideInLeft 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
            text-shadow: 2px 2px 0px rgba(76, 175, 80, 0.1);
        }}

        @keyframes slideInLeft {{
            from {{
                opacity: 0;
                transform: translateX(-80px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}

        h2 {{
            font-family: var(--font-heading);
            color: var(--color-secondary);
            font-size: 2.2rem;
            font-weight: 600;
            letter-spacing: -0.3px;
            margin-top: 60px;
            margin-bottom: 30px;
            border-left: 8px solid var(--color-primary-light);
            padding-left: 24px;
            transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        }}
        h2:hover {{
            transform: translateX(15px);
            border-left-color: var(--color-accent);
            color: var(--color-primary);
            text-shadow: 0 0 20px rgba(245, 124, 0, 0.3);
        }}
        h3 {{
            font-family: var(--font-heading);
            color: var(--color-primary);
            font-size: 1.7rem;
            font-weight: 600;
            margin-top: 40px;
            margin-bottom: 20px;
            transition: all 0.3s ease;
            position: relative;
        }}
        h3:hover {{
            color: var(--color-accent);
            transform: translateX(8px);
        }}
        h3::before {{
            content: '';
            position: absolute;
            left: -15px;
            top: 50%;
            transform: translateY(-50%);
            width: 4px;
            height: 60%;
            background: linear-gradient(180deg, var(--color-primary-light) 0%, transparent 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        h3:hover::before {{
            opacity: 1;
        }}
        h4 {{
            font-family: var(--font-body);
            color: var(--color-text-light);
            font-size: 1.3rem;
            font-weight: 600;
            margin-top: 30px;
            margin-bottom: 18px;
        }}
        p {{
            margin: 15px 0;
            line-height: 1.9;
        }}
        table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 35px 0;
            box-shadow: var(--shadow-md);
            border-radius: 12px;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
            font-family: var(--font-body);
        }}
        table:hover {{
            box-shadow: var(--shadow-lg);
            transform: translateY(-4px);
        }}
        th {{
            background: linear-gradient(135deg, var(--color-secondary) 0%, var(--color-primary) 100%);
            color: white;
            padding: 18px 20px;
            text-align: left;
            font-weight: 600;
            font-family: var(--font-heading);
            font-size: 1.05rem;
            letter-spacing: 0.3px;
        }}
        td {{
            padding: 16px 20px;
            border-bottom: 1px solid rgba(46, 125, 50, 0.08);
            transition: all 0.3s ease;
        }}
        tr:hover td {{
            background: linear-gradient(90deg, rgba(76, 175, 80, 0.08) 0%, rgba(66, 165, 245, 0.05) 100%);
            transform: scale(1.01);
        }}
        tr:last-child td {{
            border-bottom: none;
        }}
        blockquote {{
            background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
            border-left: 6px solid #2196F3;
            padding: 20px;
            margin: 25px 0;
            border-radius: 8px;
            transition: all 0.3s ease;
        }}
        blockquote:hover {{
            transform: translateX(10px);
            box-shadow: 0 4px 12px rgba(33,150,243,0.2);
        }}
        blockquote p {{
            margin: 10px 0;
        }}
        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
            line-height: 1.9;
        }}
        li {{
            margin: 8px 0;
            transition: all 0.2s ease;
        }}
        li:hover {{
            transform: translateX(5px);
        }}
        code {{
            background: #f4f4f4;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            color: #c7254e;
        }}
        strong {{
            color: #2C3E50;
            font-weight: 600;
        }}
        em {{
            color: #546E7A;
            font-style: italic;
        }}

        /* Enhanced Details/Summary */
        details {{
            background: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
            transition: all 0.3s ease;
        }}
        details:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-color: #4169E1;
        }}
        details[open] {{
            background: white;
            border-color: #4169E1;
        }}
        summary {{
            cursor: pointer;
            font-weight: 600;
            color: #4169E1;
            padding: 10px;
            user-select: none;
            transition: all 0.2s ease;
        }}
        summary:hover {{
            background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 50%);
            border-radius: 6px;
            transform: translateX(5px);
        }}

        /* Interactive Diagram Links - Distinctive Educational Design */
        a[href*="diagrams/"] {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 14px 28px;
            background: linear-gradient(135deg, var(--color-primary-light) 0%, var(--color-primary) 100%);
            color: white !important;
            text-decoration: none;
            border-radius: 12px;
            transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
            box-shadow: 0 4px 16px rgba(76,175,80,0.25);
            font-weight: 700;
            font-family: var(--font-heading);
            font-size: 1.05rem;
            letter-spacing: 0.5px;
            position: relative;
            overflow: hidden;
        }}
        a[href*="diagrams/"]::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.6s ease;
        }}
        a[href*="diagrams/"]:hover::before {{
            left: 100%;
        }}
        a[href*="diagrams/"]:hover {{
            transform: translateY(-6px) scale(1.08);
            box-shadow: var(--glow-green), var(--shadow-lg);
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{
                box-shadow: 0 6px 24px rgba(76,175,80,0.4);
            }}
            50% {{
                box-shadow: 0 8px 32px rgba(76,175,80,0.6), 0 0 40px rgba(76,175,80,0.3);
            }}
        }}

        hr {{
            border: none;
            border-top: 2px solid #e0e0e0;
            margin: 40px 0;
        }}

        /* Scroll Reveal Animation */
        .fade-in {{
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }}
        .fade-in.visible {{
            opacity: 1;
            transform: translateY(0);
        }}

        /* Mobile Responsive */
        @media (max-width: 768px) {{
            #toc-toggle, #toc-panel {{
                display: none;
            }}
            .container {{
                margin: 20px;
                padding: 20px;
            }}
            h1 {{
                font-size: 1.8rem;
            }}
            h2 {{
                font-size: 1.5rem;
            }}
        }}
    </style>
</head>
<body>
    <!-- Reading Progress Bar -->
    <div id="progress-bar"></div>

    <!-- Back to Top Button -->
    <button id="back-to-top" title="Back to top">↑</button>

    <!-- Table of Contents Toggle -->
    <button id="toc-toggle">📑 Contents</button>

    <!-- Table of Contents Panel -->
    <div id="toc-panel">
        <h3>📚 Quick Navigation</h3>
        <ul id="toc-list"></ul>
    </div>

    <nav id="main-nav">
        <a href="index.html">← Back to Chapter Overview</a>
        <span style="margin: 0 15px;">|</span>
        <span>Complete Study Notes</span>
    </nav>

    <div class="container">
        {content}
    </div>

    <footer style="background: #2C3E50; color: white; text-align: center; padding: 40px 20px; margin-top: 80px;">
        <h3>Complete Study Notes - Cell: The Unit of Life</h3>
        <p style="opacity: 0.9;">Plus One Biology | Kerala State Board + NEET Preparation</p>
        <p style="opacity: 0.8; font-size: 0.9rem; margin-top: 15px;">
            Comprehensive study material with detailed theory, flashcards, and exam tips
        </p>
    </footer>

    <script>
        // Reading Progress Bar
        window.addEventListener('scroll', () => {{
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            document.getElementById('progress-bar').style.width = scrolled + '%';
        }});

        // Back to Top Button
        const backToTop = document.getElementById('back-to-top');
        window.addEventListener('scroll', () => {{
            if (window.pageYOffset > 300) {{
                backToTop.classList.add('visible');
            }} else {{
                backToTop.classList.remove('visible');
            }}
        }});
        backToTop.addEventListener('click', () => {{
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }});

        // Shrink navbar on scroll
        const nav = document.getElementById('main-nav');
        window.addEventListener('scroll', () => {{
            if (window.pageYOffset > 50) {{
                nav.classList.add('scrolled');
            }} else {{
                nav.classList.remove('scrolled');
            }}
        }});

        // Auto-generate Table of Contents
        const tocList = document.getElementById('toc-list');
        const headings = document.querySelectorAll('h2[id]');
        headings.forEach((heading, index) => {{
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = '#' + heading.id;
            a.textContent = heading.textContent;
            a.addEventListener('click', (e) => {{
                e.preventDefault();
                heading.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }});
            li.appendChild(a);
            tocList.appendChild(li);
        }});

        // TOC Toggle
        const tocToggle = document.getElementById('toc-toggle');
        const tocPanel = document.getElementById('toc-panel');
        tocToggle.addEventListener('click', () => {{
            tocPanel.classList.toggle('visible');
        }});

        // Highlight active TOC item on scroll
        window.addEventListener('scroll', () => {{
            let current = '';
            headings.forEach(heading => {{
                const sectionTop = heading.offsetTop;
                if (window.pageYOffset >= sectionTop - 100) {{
                    current = heading.id;
                }}
            }});
            const tocLinks = document.querySelectorAll('#toc-list a');
            tocLinks.forEach(link => {{
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + current) {{
                    link.classList.add('active');
                }}
            }});
        }});

        // Scroll Reveal Animation
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }};

        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('visible');
                }}
            }});
        }}, observerOptions);

        // Add fade-in class to h2, h3, tables, and blockquotes
        document.querySelectorAll('h2, h3, table, blockquote').forEach(el => {{
            el.classList.add('fade-in');
            observer.observe(el);
        }});

        // Smooth details animation
        document.querySelectorAll('details').forEach(detail => {{
            detail.addEventListener('toggle', function() {{
                if (this.open) {{
                    this.style.animation = 'fadeInUp 0.3s ease';
                }}
            }});
        }});
    </script>
</body>
</html>
"""
    return html

def main():
    # Read study guide
    study_guide_path = 'D:/Plus_One_Doc/Botany/Docs/Cell-The-Unit-of-Life/chapter-doc/Cell_The_Unit_of_Life_Study_Guide.md'

    print("Reading study guide...")
    content = read_study_guide(study_guide_path)
    print(f"Loaded {len(content)} characters from study guide")

    # Remove interactive resource blockquotes
    print("Removing interactive resource sections...")
    content = remove_interactive_resources(content)
    print(f"Cleaned content: {len(content)} characters")

    # Remove NEET questions (available on separate exam page)
    print("Removing NEET questions sections...")
    content = remove_neet_questions(content)
    print(f"After removing NEET questions: {len(content)} characters")

    # Convert static diagram references to interactive links
    print("Converting diagram references to interactive links...")
    content = convert_diagram_references(content)
    print(f"Diagram references converted")

    # Convert markdown to HTML using markdown2
    print("Converting markdown to HTML...")
    html_content = markdown2.markdown(
        content,
        extras=[
            "tables",           # Enable table support
            "fenced-code-blocks",  # Support ```code blocks```
            "code-friendly",    # Better handling of code
            "cuddled-lists",    # Better list handling
            "header-ids",       # Add IDs to headers
            "break-on-newline"  # Line breaks
        ]
    )
    print(f"Generated {len(html_content)} characters of HTML")

    # Create complete page
    full_html = create_html_page(html_content)

    # Write output
    output_path = 'D:/Plus_One_Doc/Botany/Web/chapters/01-cell-the-unit-of-life/complete-notes.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"[OK] Complete study notes created: {output_path}")
    print(f"Source content: {len(content)} characters")
    print(f"HTML content: {len(html_content)} characters")
    print(f"Full HTML: {len(full_html)} characters")

if __name__ == '__main__':
    main()
