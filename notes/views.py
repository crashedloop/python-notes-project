"""
================================================
NOTES APP VIEWS
Django views for note management with HTMX support
Features: CRUD operations, pinning, soft delete, image uploads
================================================
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import Note, UploadedImage, Tag
from .forms import NoteForm


# ================================================
# NOTE LIST VIEW (with search, filters, and sorting)
# ================================================
@login_required
def note_list_view(request):
    """
    Display notes for the current user with search, filtering, and sorting.
    
    Query Parameters:
    - search: Search term for title/content/tags
    - tag: Filter by specific tag name
    - filter: 'all', 'pinned', or 'unpinned'
    - sort: 'newest', 'oldest', 'az', 'za'
    """
    # Start with all non-deleted notes for current user
    notes = Note.objects.filter(
        user=request.user, 
        is_deleted=False
    ).prefetch_related('tags')
    
    # Get query parameters
    search_query = request.GET.get('search', '').strip()
    tag_filter = request.GET.get('tag', '').strip()
    pinned_filter = request.GET.get('filter', 'all')
    sort_param = request.GET.get('sort', 'default')
    
    # Apply search filter (title, content, or tags)
    if search_query:
        notes = notes.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()
    
    # Apply tag filter
    if tag_filter:
        notes = notes.filter(tags__name__iexact=tag_filter)
    
    # Apply pinned filter
    if pinned_filter == 'pinned':
        notes = notes.filter(is_pinned=True)
    elif pinned_filter == 'unpinned':
        notes = notes.filter(is_pinned=False)
    
    # Apply sorting
    if sort_param == 'newest':
        notes = notes.order_by('-is_pinned', '-created_at')
    elif sort_param == 'oldest':
        notes = notes.order_by('-is_pinned', 'created_at')
    elif sort_param == 'az':
        notes = notes.order_by('-is_pinned', 'title')
    elif sort_param == 'za':
        notes = notes.order_by('-is_pinned', '-title')
    else:  # default
        notes = notes.order_by('-is_pinned', '-updated_at')
    
    # Get all tags for the current user (for tag filter display)
    user_tags = Tag.objects.filter(user=request.user).distinct()
    
    context = {
        'notes': notes,
        'user_tags': user_tags,
        'search_query': search_query,
        'tag_filter': tag_filter,
        'pinned_filter': pinned_filter,
        'sort_param': sort_param,
    }
    
    # For HTMX requests, return only the partial
    if request.headers.get('HX-Request'):
        return render(request, 'notes/partials/note_list_partial.html', context)
    
    return render(request, 'notes/note_list.html', context)


# ================================================
# NOTE CREATE VIEW (HTMX-compatible)
# ================================================
@login_required
def note_create(request):
    """
    Create a new note with tags support.
    - For HTMX requests: Returns only the note card HTML for dynamic insertion
    - For regular requests: Redirects to note list after creation
    """
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            # Create note instance without saving
            note = form.save(commit=False)
            # Assign current user as note owner
            note.user = request.user
            # Save note (this will also process tags via form's custom save method)
            note = form.save()
            
            # Return partial HTML for HTMX (no full page reload)
            if request.headers.get('HX-Request'):
                return render(request, 'notes/partials/note_card.html', {'note': note})
            
            # Fallback for regular form POST
            return redirect('notes:note_list')
    else:
        form = NoteForm()
    
    return render(request, 'notes/note_form.html', {'form': form, 'action': 'Create'})




# ================================================
# NOTE EDIT VIEW
# ================================================
@login_required
def note_edit(request, pk):
    """
    Edit an existing note.
    - Ensures user owns the note (security)
    - Redirects to note list after successful update
    """
    note = get_object_or_404(Note, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes:note_list')
    else:
        form = NoteForm(instance=note)
    
    return render(request, 'notes/note_form.html', {
        'form': form, 
        'note': note, 
        'action': 'Edit'
    })


# ================================================
# NOTE DELETE VIEW (Soft Delete)
# ================================================
@login_required
def note_delete(request, pk):
    """
    Soft delete a note (moves to recycle bin).
    - Sets is_deleted=True instead of actually deleting
    - For HTMX: Returns empty response for seamless DOM removal
    """
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.is_deleted = True
    note.save()
    
    # HTMX: Empty response triggers DOM removal
    if request.headers.get('HX-Request'):
        return HttpResponse('')
    
    return redirect('notes:note_list')


# ================================================
# NOTE RESTORE VIEW
# ================================================
@login_required
def note_restore(request, pk):
    """
    Restore a deleted note from recycle bin.
    - Sets is_deleted=False to make note active again
    """
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.is_deleted = False
    note.save()
    
    # HTMX: Empty response for seamless removal from recycle bin
    if request.headers.get('HX-Request'):
        return HttpResponse('')
    
    return redirect('notes:recycle_bin')


# ================================================
# RECYCLE BIN VIEW
# ================================================
@login_required
def recycle_bin(request):
    """
    Display all deleted notes for the current user.
    Users can restore or permanently delete notes from here.
    """
    deleted_notes = Note.objects.filter(
        user=request.user, 
        is_deleted=True
    ).order_by('-updated_at')
    
    return render(request, 'notes/recycle_bin.html', {'notes': deleted_notes})


# ================================================
# PIN TOGGLE VIEW (HTMX)
# ================================================
@login_required
def pin_toggle(request, pk):
    """
    Toggle the pinned status of a note (Google Keep style).
    - Pinned notes appear at the top of the list
    - For HTMX: Returns updated note card for seamless UI update
    """
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.is_pinned = not note.is_pinned
    note.save()
    
    # HTMX: Return updated card to replace existing one
    if request.headers.get('HX-Request'):
        return render(request, 'notes/partials/note_card.html', {'note': note})
    
    return redirect('notes:note_list')


# ================================================
# AUTOSAVE ENDPOINT (AJAX)
# ================================================
@login_required
def autosave(request, pk):
    """
    Silent autosave endpoint for real-time updates.
    Used by interactive checkboxes to persist state changes.
    Returns JSON status for AJAX handling.
    """
    if request.method == 'POST':
        note = get_object_or_404(Note, pk=pk, user=request.user)
        note.content = request.POST.get('content', '')
        note.save()
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'invalid method'}, status=405)


# ================================================
# NOTE VIEW (Single Note Detail)
# ================================================
@login_required
def note_view(request, pk):
    """
    Display a single note with full content.
    - Shows interactive checkboxes for task lists
    - Renders markdown with images
    """
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'notes/note_view.html', {'note': note})


# ================================================
# USER SIGNUP VIEW
# ================================================
def signup(request):
    """
    User registration view.
    - Creates new user account
    - Automatically logs in user after successful signup
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto-login after registration
            login(request, user)
            return redirect('notes:note_list')
    else:
        form = UserCreationForm()
    
    return render(request, "registration/signup.html", {"form": form})


# ================================================
# IMAGE UPLOAD ENDPOINT (AJAX)
# ================================================
@login_required
@require_http_methods(["POST"])
def upload_image(request):
    """
    Handle image uploads from Markdown editor.
    
    Security & Validation:
    - File type validation (JPEG, PNG, GIF, WEBP only)
    - File size limit (5MB max)
    - User authentication required
    
    Returns:
    - JSON with image URL on success
    - JSON with error message on failure
    """
    # Validate image file exists in request
    if 'image' not in request.FILES:
        return JsonResponse({
            'error': 'No image file provided'
        }, status=400)
    
    image_file = request.FILES['image']
    
    # Validate file type (security measure)
    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if image_file.content_type not in allowed_types:
        return JsonResponse({
            'error': 'Invalid file type. Allowed: JPEG, PNG, GIF, WEBP'
        }, status=400)
    
    # Validate file size (prevent large uploads)
    MAX_SIZE = 5 * 1024 * 1024  # 5MB in bytes
    if image_file.size > MAX_SIZE:
        return JsonResponse({
            'error': 'File too large. Maximum size: 5MB'
        }, status=400)
    
    try:
        # Create UploadedImage record in database
        uploaded_image = UploadedImage.objects.create(
            user=request.user,
            image=image_file
        )
        
        # Build absolute URL for image
        image_url = request.build_absolute_uri(uploaded_image.image.url)
        
        return JsonResponse({
            'success': True,
            'url': image_url
        })
    except Exception as e:
        # Handle any unexpected errors
        return JsonResponse({
            'error': f'Upload failed: {str(e)}'
        }, status=500)
