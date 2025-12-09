"""
Convert Cell Study Guide Markdown to Complete HTML Study Notes
Extracts all content and creates comprehensive HTML page
"""

import re
import os

def read_study_guide(file_path):
    """Read the study guide markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def markdown_to_html(content):
    """Convert markdown content to HTML"""
    # Convert headers
    content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'<h2 id="\1">\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)

    # Convert bold
    content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)

    # Convert italic
    content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)

    # Convert code
    content = re.sub(r'`([^`]+)`', r'<code>\1</code>', content)

    # Convert lists (unordered)
    content = re.sub(r'^\- (.+)$', r'<li>\1</li>', content, flags=re.MULTILINE)

    # Convert lists (ordered)
    content = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', content, flags=re.MULTILINE)

    # Wrap paragraphs
    lines = content.split('\n\n')
    html_lines = []
    for line in lines:
        if line.strip():
            if not line.startswith('<') and line.strip():
                html_lines.append(f'<p>{line}</p>')
            else:
                html_lines.append(line)

    return '\n\n'.join(html_lines)

def create_html_page(content):
    """Create complete HTML page with styling"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Study Notes - Cell: The Unit of Life | Plus One Biology</title>
    <link rel="stylesheet" href="../../css/base.css">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            color: #333;
            background: #f5f7fa;
        }}
        nav {{
            background: linear-gradient(135deg, #4169E1 0%, #0047AB 100%);
            padding: 15px 30px;
            color: white;
            position: sticky;
            top: 0;
            z-index: 1000;
        }}
        nav a {{
            color: white;
            text-decoration: none;
            font-weight: 600;
        }}
        .container {{
            max-width: 1000px;
            margin: 40px auto;
            padding: 40px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #4169E1;
            font-size: 2.5rem;
            border-bottom: 4px solid #4169E1;
            padding-bottom: 15px;
        }}
        h2 {{
            color: #2C3E50;
            font-size: 2rem;
            margin-top: 50px;
            border-left: 6px solid #4CAF50;
            padding-left: 20px;
        }}
        h3 {{
            color: #34495E;
            font-size: 1.5rem;
            margin-top: 35px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        th {{
            background: linear-gradient(135deg, #4169E1 0%, #0047AB 100%);
            color: white;
            padding: 15px;
            text-align: left;
        }}
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }}
        tr:hover {{
            background-color: #f8f9fa;
        }}
        .info-box {{
            background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
            border-left: 6px solid #2196F3;
            padding: 20px;
            margin: 25px 0;
            border-radius: 8px;
        }}
        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
            line-height: 1.9;
        }}
    </style>
</head>
<body>
    <nav>
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
    </footer>
</body>
</html>
"""
    return html

def main():
    # Read study guide
    study_guide_path = 'D:/Plus_One_Doc/Botany/Docs/Cell-The-Unit-of-Life/chapter-doc/Cell_The_Unit_of_Life_Study_Guide.md'
    content = read_study_guide(study_guide_path)

    # Convert to HTML
    html_content = markdown_to_html(content)

    # Create complete page
    full_html = create_html_page(html_content)

    # Write output
    output_path = 'D:/Plus_One_Doc/Botany/Web/chapters/01-cell-the-unit-of-life/complete-notes.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"[OK] Complete study notes created: {output_path}")
    print(f"Content length: {len(content)} characters")
    print(f"HTML length: {len(full_html)} characters")

if __name__ == '__main__':
    main()
