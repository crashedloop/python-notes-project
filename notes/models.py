"""
================================================
NOTES APP MODELS
Database models for note-taking application
Features: User-owned notes, pinning, soft delete, image uploads
================================================
"""

from django.db import models
from django.contrib.auth.models import User
import uuid
import os
import hashlib


def upload_image_path(instance, filename):
    """
    Generate unique filename for uploaded images.
    
    Uses UUID to prevent filename collisions and maintain privacy.
    Images are stored in: media/uploads/[uuid].[ext]
    
    Args:
        instance: UploadedImage model instance
        filename: Original uploaded filename
        
    Returns:
        str: Path relative to MEDIA_ROOT
    """
    # Extract file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads', unique_filename)


# ================================================
# TAG MODEL (For categorizing notes)
# ================================================
class Tag(models.Model):
    """
    Tag model for categorizing and filtering notes.
    
    Features:
    - Unique tag names (case-insensitive)
    - User-specific tags
    - Auto-generated pastel colors for dark theme
    - Sorted alphabetically
    """
    
    # Tag name
    name = models.CharField(
        max_length=50,
        help_text="Tag name (e.g., 'work', 'personal', 'ideas')"
    )
    
    # Ownership
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Tag owner"
    )
    
    # Auto-generated color (pastel, dark mode friendly)
    color = models.CharField(
        max_length=7,
        default='#FFD580',
        help_text="Hex color code for tag chip"
    )
    
    # Timestamp
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When tag was created"
    )
    
    def save(self, *args, **kwargs):
        """
        Generate unique color based on tag name if not set.
        Uses hash to ensure consistent colors for same tag name.
        """
        if not self.color or self.color == '#FFD580':
            # Generate color from tag name hash
            hash_object = hashlib.md5(self.name.lower().encode())
            hash_hex = hash_object.hexdigest()
            
            # Generate pastel colors (dark mode friendly)
            pastel_colors = [
                '#FFD580',  # Pastel yellow
                '#A1C6EA',  # Pastel blue
                '#C3F0CA',  # Pastel green
                '#FFB3BA',  # Pastel pink
                '#FFDFBA',  # Pastel orange
                '#FFFFBA',  # Pastel lemon
                '#BAFFC9',  # Pastel mint
                '#BAE1FF',  # Pastel sky blue
                '#E0BBE4',  # Pastel lavender
                '#FFDFD3',  # Pastel peach
            ]
            
            # Select color based on hash
            color_index = int(hash_hex[:8], 16) % len(pastel_colors)
            self.color = pastel_colors[color_index]
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        unique_together = ['name', 'user']  # Each user can have unique tag names
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


# ================================================
# NOTE MODEL (Main content model)
# ================================================
class Note(models.Model):
    """
    Core note model with markdown support.
    
    Features:
    - User ownership (multi-user support)
    - Markdown content with images
    - Pinning (keep important notes at top)
    - Soft delete (move to recycle bin instead of permanent deletion)
    - Automatic timestamps
    
    Ordering: Pinned notes first, then by last updated
    """
    
    # Ownership
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        help_text="Note owner"
    )
    
    # Content
    title = models.CharField(
        max_length=200,
        help_text="Note title (required)"
    )
    content = models.TextField(
        blank=True,
        help_text="Note content in Markdown format"
    )
    
    # Tags (Many-to-Many relationship)
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='notes',
        help_text="Tags for categorizing this note"
    )
    
    # Status flags
    is_pinned = models.BooleanField(
        default=False,
        help_text="Whether note is pinned to top of list"
    )
    is_deleted = models.BooleanField(
        default=False,
        help_text="Soft delete flag (recycle bin)"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When note was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When note was last modified"
    )

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-is_pinned', '-updated_at']
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'


# ================================================
# UPLOADED IMAGE MODEL (For markdown images)
# ================================================
class UploadedImage(models.Model):
    """
    Model to store images uploaded via markdown editor.
    
    Images are stored with unique UUIDs to prevent conflicts.
    Images are associated with users for access control.
    """
    
    # Ownership
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        help_text="Image uploader"
    )
    
    # File storage
    image = models.ImageField(
        upload_to=upload_image_path,
        help_text="Uploaded image file"
    )
    
    # Timestamp
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When image was uploaded"
    )
    
    def __str__(self):
        return f"Image {self.id} by {self.user.username}"
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Uploaded Image'
        verbose_name_plural = 'Uploaded Images'
