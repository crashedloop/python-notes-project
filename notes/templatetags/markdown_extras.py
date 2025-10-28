"""
================================================
MARKDOWN TEMPLATE TAGS
Custom Django template filters for markdown rendering
Features: Safe HTML conversion, task lists, image handling
================================================
"""

from django import template
from django.utils.safestring import mark_safe
import markdown2
import bleach
import re

register = template.Library()


# ================================================
# BASIC MARKDOWN FILTER
# ================================================
@register.filter(name='markdown')
def markdown_filter(text):
    """
    Convert Markdown text to safe HTML.
    
    Process:
    1. Convert markdown to HTML using markdown2
    2. Sanitize HTML to prevent XSS attacks using bleach
    3. Linkify plain URLs
    
    Features:
    - Fenced code blocks with syntax highlighting
    - Tables
    - Strike-through text
    - Task lists (checkboxes)
    - Smart header IDs
    """
    if not text:
        return ''
    
    # Convert Markdown to HTML with extensions
    html = markdown2.markdown(
        text,
        extras=[
            'fenced-code-blocks',  # ```code blocks```
            'tables',              # GitHub-style tables
            'strike',              # ~~strikethrough~~
            'task_list',           # - [ ] checkboxes
            'code-friendly',       # Better code handling
            'cuddled-lists',       # Lists without blank lines
            'header-ids',          # Auto-generate header IDs
            'break-on-newline',    # Single newline = <br>
        ]
    )
    
    # Define allowed HTML tags and attributes for security
    allowed_tags = [
        'p', 'br', 'strong', 'em', 'u', 's', 'del', 'ins',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'blockquote', 'code', 'pre',
        'ul', 'ol', 'li',
        'a', 'img',
        'table', 'thead', 'tbody', 'tr', 'th', 'td',
        'hr', 'div', 'span', 'input',
    ]
    
    allowed_attrs = {
        '*': ['class', 'id'],
        'a': ['href', 'title', 'target', 'rel'],
        'img': ['src', 'alt', 'title', 'width', 'height', 'class'],
        'code': ['class'],
        'pre': ['class'],
        'th': ['align'],
        'td': ['align'],
        'input': ['type', 'checked', 'disabled', 'class'],
        'li': ['class'],
    }
    
    # Sanitize HTML to prevent XSS attacks
    clean_html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True
    )
    
    # Linkify URLs (optional - makes plain URLs clickable)
    clean_html = bleach.linkify(clean_html)
    
    # Mark as safe for Django template rendering
    return mark_safe(clean_html)



# ================================================
# NOTE PREVIEW FILTER (For Cards)
# ================================================
@register.filter(name='render_note_preview')
def render_note_preview(text):
    """
    Render note content for preview cards (truncated view).
    
    Features:
    - Extracts and displays task completion count
    - Shows image count or single image thumbnail
    - Truncates text to 200 characters
    - Removes images and tasks from text preview
    
    Returns formatted HTML with badges for tasks/images.
    """
    if not text:
        return ''
    
    result_parts = []
    
    # Extract images from markdown
    image_pattern = r'!\[.*?\]\((.*?)\)'
    images = re.findall(image_pattern, text)
    
    # Extract tasks from markdown
    task_pattern = r'- \[([ xX])\] (.+)'
    tasks = re.findall(task_pattern, text, re.IGNORECASE)
    
    # Remove images and tasks from text for clean preview
    preview_text = re.sub(image_pattern, '', text)
    preview_text = re.sub(task_pattern, '', preview_text)
    preview_text = preview_text.strip()
    
    # Add truncated text preview
    if preview_text:
        # Convert first 200 chars to HTML
        html = markdown2.markdown(
            preview_text[:200], 
            extras=['fenced-code-blocks', 'strike']
        )
        # Sanitize with minimal allowed tags
        allowed_tags = ['p', 'br', 'strong', 'em', 'code', 'del']
        clean_html = bleach.clean(html, tags=allowed_tags, strip=True)
        result_parts.append(clean_html)
    
    # Add task completion badge
    if tasks:
        completed = sum(1 for status, _ in tasks if status.lower() == 'x')
        total = len(tasks)
        task_html = f'<div class="flex items-center gap-1 mt-2 text-xs"><span class="inline-flex items-center px-2 py-1 rounded bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300"><svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20"><path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/><path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm9.707 5.707a1 1 0 00-1.414-1.414L9 12.586l-1.293-1.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>{completed}/{total} tasks</span></div>'
        result_parts.append(task_html)
    
    # Add image preview/badge
    if images:
        if len(images) == 1:
            # Single image: Show thumbnail
            img_html = f'<div class="mt-2"><img src="{images[0]}" alt="Image" class="rounded max-h-32 w-full object-cover" /></div>'
        else:
            # Multiple images: Show count badge
            img_html = f'<div class="flex items-center gap-1 mt-2 text-xs"><span class="inline-flex items-center px-2 py-1 rounded bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300"><svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clip-rule="evenodd"/></svg>{len(images)} images</span></div>'
        result_parts.append(img_html)
    
    return mark_safe(''.join(result_parts))



# ================================================
# INTERACTIVE NOTE FILTER (Full View)
# ================================================
@register.filter(name='render_interactive_note')
def render_interactive_note(text):
    """
    Render note content with interactive features (Google Keep style).
    
    Features:
    - Interactive checkboxes that can be toggled
    - Completed tasks get crossed out
    - Images rendered at the end
    - Full markdown support
    
    Process:
    1. Extract images from markdown
    2. Convert markdown to HTML
    3. Replace disabled checkboxes with interactive ones
    4. Sanitize HTML for security
    5. Append images at the end
    """
    if not text:
        return ''
    
    # Extract and remove images from content
    image_pattern = r'!\[.*?\]\((.*?)\)'
    images = re.findall(image_pattern, text)
    content_without_images = re.sub(image_pattern, '', text).strip()
    
    # Convert markdown to HTML with full feature set
    html = markdown2.markdown(
        content_without_images,
        extras=[
            'fenced-code-blocks',  # Code blocks
            'tables',              # Tables
            'strike',              # Strikethrough
            'task_list',           # Task checkboxes
            'code-friendly',       # Better code handling
            'cuddled-lists',       # Compact lists
            'header-ids',          # Header anchors
            'break-on-newline',    # Line breaks
        ]
    )
    
    # ------------------------------------------------
    # Replace disabled checkboxes with interactive ones
    # markdown2 generates: <input type="checkbox" disabled>
    # We convert to: <input type="checkbox" class="keep-checkbox">
    # ------------------------------------------------
    
    # Unchecked tasks: - [ ]
    html = re.sub(
        r'<li class="task-list-item"><input type="checkbox" disabled>\s*',
        r'<li class="task-list-item keep-task-item"><label class="keep-task-label"><input type="checkbox" class="keep-checkbox" /><span class="keep-task-text">',
        html
    )
    
    # Checked tasks: - [x]
    html = re.sub(
        r'<li class="task-list-item"><input type="checkbox" checked disabled>\s*',
        r'<li class="task-list-item keep-task-item"><label class="keep-task-label"><input type="checkbox" checked class="keep-checkbox" /><span class="keep-task-text keep-task-checked">',
        html
    )
    
    # Close span and label tags properly
    html = re.sub(
        r'(<li class="task-list-item keep-task-item">.*?)(</li>)',
        r'\1</span></label>\2',
        html,
        flags=re.DOTALL
    )
    
    # ------------------------------------------------
    # Sanitize HTML to prevent XSS attacks
    # Only allow safe tags and attributes
    # ------------------------------------------------
    allowed_tags = [
        'p', 'br', 'strong', 'em', 'u', 's', 'del', 'ins',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'blockquote', 'code', 'pre',
        'ul', 'ol', 'li',
        'a', 'img',
        'table', 'thead', 'tbody', 'tr', 'th', 'td',
        'hr', 'div', 'span', 'input', 'label',
    ]
    
    allowed_attrs = {
        '*': ['class', 'id'],
        'a': ['href', 'title', 'target', 'rel'],
        'img': ['src', 'alt', 'title', 'width', 'height', 'class'],
        'code': ['class'],
        'pre': ['class'],
        'th': ['align'],
        'td': ['align'],
        'input': ['type', 'checked', 'class'],
        'li': ['class'],
        'label': ['class'],
        'span': ['class'],
    }
    
    clean_html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True
    )
    
    # Make plain URLs clickable
    clean_html = bleach.linkify(clean_html)
    
    result = clean_html
    
    # ------------------------------------------------
    # Append images at the end in responsive grid
    # Single column on mobile, 2 columns on desktop
    # ------------------------------------------------
    if images:
        image_html = '<div class="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-3">'
        for img_url in images:
            image_html += f'<img src="{img_url}" alt="Image" class="rounded-lg border border-gray-200 dark:border-gray-700 w-full h-auto object-cover shadow-sm hover:shadow-md transition-shadow" loading="lazy" />'
        image_html += '</div>'
        result += image_html
    
    return mark_safe(result)
