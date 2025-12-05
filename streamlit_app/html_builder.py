import os
from datetime import datetime
from typing import Dict, List

def organize_content_for_html(markdown_files, summaries):
    """
    Organize content into logical groups to avoid overwhelming TOC
    """
    organized = {
        "README and Main Docs": {},
        "Documentation": {},
        "Guides and Tutorials": {},
        "API Reference": {},
        "Other Files": {}
    }
    
    for path in markdown_files.keys():
        file_name = os.path.basename(path).lower()
        dir_name = os.path.dirname(path).lower()
        
        # Categorize files
        if file_name in ["readme.md", "index.md"]:
            organized["README and Main Docs"][path] = summaries.get(path, "")
        elif "doc" in dir_name or "guide" in dir_name:
            organized["Documentation"][path] = summaries.get(path, "")
        elif "tutorial" in dir_name or "example" in dir_name:
            organized["Guides and Tutorials"][path] = summaries.get(path, "")
        elif "api" in dir_name or "reference" in dir_name:
            organized["API Reference"][path] = summaries.get(path, "")
        else:
            organized["Other Files"][path] = summaries.get(path, "")
    
    return organized

def create_file_section(file_path, summary, section_id, image_files, owner, repo_name):
    """
    Create a section for a single file (without inline images)
    """
    display_name = file_path.replace("/", " / ").replace("_", " ").replace("-", " ")
    
    # Create clickable link for the markdown file
    file_url = f"https://github.com/{owner}/{repo_name}/blob/main/{file_path}"
    
    return f'''
        <div class="section" id="{section_id}">
            <h2 class="section-title">{display_name}</h2>
            <div class="section-path">📁 <a href="{file_url}" target="_blank" class="file-link">{file_path}</a></div>
            <div class="section-content">
                {format_summary_content(summary, owner, repo_name)}
            </div>
        </div>
    '''

def generate_onboarding_html(
    summaries: Dict[str, str],
    repo_meta: Dict[str, str],
    author: str = "Riddhi Shah",
    company: str = "Bazel Inc",
    markdown_files: Dict[str, str] = None,
    image_files: List[str] = None

) -> str:
    """
    Generate a professional HTML onboarding document with:
    - Cover page
    - Table of contents  
    - Section-by-section content
    - Professional CSS styling
    """
    
    # Extract repo info
    repo_name = repo_meta.get("repo", "Repository")
    owner = repo_meta.get("owner", "Unknown")
    github_url = f"https://github.com/{owner}/{repo_name}"
    current_date = datetime.now().strftime("%B %d, %Y")
    
    # Organize content into categories to avoid overwhelming TOC
    if markdown_files and len(summaries) > 20:  # Only organize if many files
        organized_content = organize_content_for_html(markdown_files, summaries)
    else:
        # Keep simple structure for small repos
        organized_content = {"Documentation": summaries}
    
    # Generate table of contents for organized sections
    toc_items = []
    section_content = []
    section_counter = 1
    
    for category, files in organized_content.items():
        if not files:  # Skip empty categories
            continue
        
        # Add category header only if we have multiple categories
        if len(organized_content) > 1:
            toc_items.append(f'<li class="toc-category">{category} ({len(files)} files)</li>')
        
        # Create sections for each file in this category
        for file_path, summary in files.items():
            section_id = f"section-{section_counter}"
            display_name = file_path.replace("/", " / ").replace("_", " ").replace("-", " ")
            
            toc_items.append(f'<li><a href="#{section_id}">{os.path.basename(file_path)}</a></li>')
            
            # Create section with images
            section_content.append(create_file_section(
                file_path, 
                summary, 
                section_id,
                None,
                owner,
                repo_name
            ))
            section_counter += 1

        # Create separate image gallery
    image_gallery_section = create_image_gallery_section(image_files, owner, repo_name)
    
    # Build complete HTML
    html_template = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{repo_name} - Onboarding Documentation</title>
    <style>
        {get_css_styles()}
    </style>
</head>
<body>
    <!-- Cover Page -->
    <div class="cover-page">
        <div class="cover-header">
            <div class="company-branding">
                <h1 class="company-name">{company}</h1>
                <div class="company-tagline">Knowledge Base Documentation</div>
            </div>
        </div>
        
        <div class="cover-main">
            <h1 class="project-title">{repo_name}</h1>
            <h2 class="subtitle">Onboarding Documentation</h2>
            
            <div class="project-info">
                <div class="info-item">
                    <span class="label">Repository:</span>
                    <a href="{github_url}" target="_blank" class="repo-link">{github_url}</a>
                </div>
                <div class="info-item">
                    <span class="label">Author:</span>
                    <span class="value">{author}</span>
                </div>
                <div class="info-item">
                    <span class="label">Generated:</span>
                    <span class="value">{current_date}</span>
                </div>
                <div class="info-item">
                    <span class="label">Branch:</span>
                    <span class="value">{repo_meta.get("branch", "main")}</span>
                </div>
            </div>
        </div>
        
        <div class="cover-footer">
            <p>This document provides an overview of the repository structure and key documentation files.</p>
        </div>
    </div>

    <!-- Table of Contents Page -->
    <div class="toc-page">
        <h1 class="page-title">Table of Contents</h1>
        <div class="toc-summary">
            <p>This document contains <strong>{len(summaries)}</strong> sections covering the main documentation files in the repository.</p>
        </div>
        <ul class="toc-list">
            {"".join(toc_items)}
        </ul>
    </div>

    <!-- Content Sections -->
    <div class="content-pages">
        {"".join(section_content)}
    </div>

    <!-- Image Gallery Section -->
    {image_gallery_section}

    <!-- Footer -->
    <div class="document-footer">
        <p>Generated by AI-Powered Onboarding Documentation System</p>
        <p>For the most up-to-date information, please refer to the repository at <a href="{github_url}">{github_url}</a></p>
    </div>
</body>
</html>
'''
    
    return html_template

def create_image_gallery_section(image_files, owner, repo_name):
    """
    Create a dedicated section for all images/diagrams
    """
    if not image_files:
        return ""
    
    # Categorize images
    architecture_images = []
    screenshot_images = []
    other_images = []
    
    for img_path in image_files:
        img_lower = img_path.lower()
        if any(keyword in img_lower for keyword in ['architecture', 'diagram', 'flow', 'design']):
            architecture_images.append(img_path)
        elif any(keyword in img_lower for keyword in ['screenshot', 'screen', 'demo']):
            screenshot_images.append(img_path)
        else:
            other_images.append(img_path)
    
    gallery_html = '''
    <div class="image-gallery-section">
        <h1 class="gallery-title">🎨 Visual Assets & Architecture</h1>
        <div class="gallery-intro">
            <p>This section contains all visual assets found in the repository, organized by type.</p>
        </div>
    '''
    
    # Architecture diagrams
    if architecture_images:
        gallery_html += '<h2 class="gallery-category">🏗️ Architecture & Diagrams</h2><div class="image-grid">'
        for img_path in architecture_images:
            img_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/main/{img_path}"
            img_name = os.path.basename(img_path)
            gallery_html += f'''
                <div class="gallery-item">
                    <img src="{img_url}" alt="{img_name}" class="gallery-image" />
                    <div class="gallery-caption">
                        <strong>{img_name}</strong><br>
                        <small>📁 {img_path}</small>
                    </div>
                </div>
            '''
        gallery_html += '</div>'
    
    # Screenshots
    if screenshot_images:
        gallery_html += '<h2 class="gallery-category">📷 Screenshots & Demos</h2><div class="image-grid">'
        for img_path in screenshot_images:
            img_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/main/{img_path}"
            img_name = os.path.basename(img_path)
            gallery_html += f'''
                <div class="gallery-item">
                    <img src="{img_url}" alt="{img_name}" class="gallery-image" />
                    <div class="gallery-caption">
                        <strong>{img_name}</strong><br>
                        <small>📁 {img_path}</small>
                    </div>
                </div>
            '''
        gallery_html += '</div>'
    
    # Other images
    if other_images:
        gallery_html += '<h2 class="gallery-category">🖼️ Other Images</h2><div class="image-grid">'
        for img_path in other_images:
            img_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/main/{img_path}"
            img_name = os.path.basename(img_path)
            gallery_html += f'''
                <div class="gallery-item">
                    <img src="{img_url}" alt="{img_name}" class="gallery-image" />
                    <div class="gallery-caption">
                        <strong>{img_name}</strong><br>
                        <small>📁 {img_path}</small>
                    </div>
                </div>
            '''
        gallery_html += '</div>'
    
    gallery_html += '</div>'
    return gallery_html

def format_summary_content(summary: str, owner: str = None, repo_name: str = None) -> str:
    """Format summary content with proper HTML markup and correct GitHub links"""
    # Split into paragraphs
    paragraphs = summary.split('\n\n')
    formatted_paragraphs = []
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        # Check for special formatting
        if para.startswith("Note:"):
            formatted_paragraphs.append(f'<div class="note">{para}</div>')
        elif "For full details, refer to:" in para and owner and repo_name:
            # Fix the GitHub link in the summary
            import re
            # Look for markdown link format [filename](path)
            link_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', para)
            if link_match:
                file_name = link_match.group(1)
                file_path = link_match.group(2)
                github_url = f"https://github.com/{owner}/{repo_name}/blob/main/{file_path}"
                para = f'For full details, refer to: <a href="{github_url}" target="_blank" class="file-link">{file_name}</a>'
            formatted_paragraphs.append(f'<div class="reference">{para}</div>')
        else:
            formatted_paragraphs.append(f'<p>{para}</p>')
    
    return "".join(formatted_paragraphs)


def get_css_styles() -> str:
    """Return comprehensive CSS styles for the onboarding document"""
    return '''
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #ffffff;
        }

        /* Cover Page Styles */
        .cover-page {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 60px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            page-break-after: always;
        }

        .cover-header {
            text-align: right;
        }

        .company-branding .company-name {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .company-tagline {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .cover-main {
            text-align: center;
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .project-title {
            font-size: 4rem;
            font-weight: 800;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .subtitle {
            font-size: 1.8rem;
            font-weight: 300;
            margin-bottom: 60px;
            opacity: 0.9;
        }

        .project-info {
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
            max-width: 600px;
            margin: 0 auto;
        }

        .info-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }

        .info-item:last-child {
            border-bottom: none;
        }

        .label {
            font-weight: 600;
        }

        .value {
            font-weight: 400;
        }

        .repo-link {
            color: #ffffff;
            text-decoration: none;
            border-bottom: 1px dotted rgba(255,255,255,0.5);
        }

        .repo-link:hover {
            border-bottom: 1px solid rgba(255,255,255,0.8);
        }

        .cover-footer {
            text-align: center;
            font-size: 1.1rem;
            opacity: 0.8;
        }

        /* Table of Contents Styles */
        .toc-page {
            min-height: 100vh;
            padding: 60px 40px;
            page-break-after: always;
        }

        .page-title {
            font-size: 3rem;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 30px;
            text-align: center;
        }

        .toc-summary {
            text-align: center;
            margin-bottom: 50px;
            font-size: 1.1rem;
            color: #666;
        }
        .toc-category {
        font-size: 1.1rem;
        color: #667eea;
        margin: 15px 0 5px 0;
        padding: 8px 15px;
        background: #f0f4ff;
        border-left: 4px solid #667eea;
        font-weight: 600;
        }

        .toc-list {
            list-style: none;
            max-width: 800px;
            margin: 0 auto;
        }

        .toc-list li {
            margin-bottom: 15px;
            padding: 15px 20px;
            background: #f7fafc;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }

        .toc-list a {
            text-decoration: none;
            color: #2d3748;
            font-size: 1.1rem;
            font-weight: 500;
        }

        .toc-list a:hover {
            color: #667eea;
        }

        /* Content Section Styles */
        .content-pages {
            max-width: 900px;
            margin: 0 auto;
            padding: 40px;
        }

        .section {
            margin-bottom: 60px;
            padding-bottom: 40px;
            border-bottom: 2px solid #e2e8f0;
            page-break-inside: avoid;
        }

        .section:last-child {
            border-bottom: none;
        }

        .section-title {
            font-size: 2rem;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 10px;
        }

        .section-path {
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            color: #666;
            background: #f7fafc;
            padding: 8px 12px;
            border-radius: 5px;
            margin-bottom: 25px;
            display: inline-block;
        }

        .section-content {
            font-size: 1.1rem;
            line-height: 1.7;
        }

        .section-content p {
            margin-bottom: 15px;
        }

        .note {
            background: #fff5cd;
            border: 1px solid #f6e05e;
            border-radius: 5px;
            padding: 15px;
            margin: 20px 0;
            font-style: italic;
        }

        .reference {
            background: #e6fffa;
            border: 1px solid #81e6d9;
            border-radius: 5px;
            padding: 12px;
            margin: 15px 0;
            font-size: 0.95rem;
        }

        /* Footer Styles */
        .document-footer {
            background: #f7fafc;
            padding: 30px;
            text-align: center;
            color: #666;
            border-top: 2px solid #e2e8f0;
            margin-top: 60px;
        }

        .document-footer p {
            margin-bottom: 10px;
        }

        .document-footer a {
            color: #667eea;
            text-decoration: none;
        }
        /* File Link Styles */
        .file-link {
            color: #667eea;
            text-decoration: none;
        }

        .file-link:hover {
            text-decoration: underline;
        }

        /* Image Gallery Styles */
        .image-gallery {
            margin: 25px 0;
            padding: 20px;
            background: #f8fafc;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        }

        .image-gallery h4 {
            margin-bottom: 15px;
            color: #4a5568;
        }

        .image-item {
            margin: 15px 0;
            text-align: center;
        }

        .content-image {
            max-width: 100%;
            max-height: 300px;
            border-radius: 5px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border: 1px solid #e2e8f0;
        }

        .image-caption {
            margin-top: 8px;
            font-size: 0.9rem;
            color: #666;
            font-style: italic;
        }

        /* Print Styles */
        @media print {
            .cover-page,
            .toc-page {
                page-break-after: always;
            }
            
            .section {
                page-break-inside: avoid;
            }
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .cover-page,
            .toc-page,
            .content-pages {
                padding: 30px 20px;
            }
            
            .project-title {
                font-size: 2.5rem;
            }
            
            .page-title {
                font-size: 2rem;
            }
            
            .info-item {
                flex-direction: column;
                gap: 5px;
            }
        }
    '''


def save_html_file(html_content: str, filename: str = "onboarding_document.html") -> str:
    """Save HTML content to file and return the file path"""
    filepath = os.path.abspath(filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filepath