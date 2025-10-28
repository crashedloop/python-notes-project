from django import forms
from .models import Note, Tag

class NoteForm(forms.ModelForm):
    # Tags field for comma-separated tag input
    tags_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Tags (comma-separated, e.g., work, important, ideas)',
            'class': 'w-full bg-white dark:bg-[#202124] text-[#202124] dark:text-[#e8eaed] text-sm px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#1a73e8] dark:focus:ring-[#8ab4f8] placeholder-[#5f6368] dark:placeholder-[#9aa0a6] border border-gray-300 dark:border-[#5f6368] transition-all'
        }),
        label='Tags'
    )
    
    class Meta:
        model = Note
        fields = ['title', 'content']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate tags field if editing existing note
        if self.instance and self.instance.pk:
            tags = self.instance.tags.all()
            if tags:
                self.initial['tags_input'] = ', '.join([tag.name for tag in tags])
    
    def save(self, commit=True):
        """
        Custom save to handle tags processing.
        Parses comma-separated tags and creates/assigns Tag objects.
        """
        note = super().save(commit=False)
        
        if commit:
            note.save()
            
            # Process tags
            tags_input = self.cleaned_data.get('tags_input', '')
            if tags_input:
                # Clear existing tags
                note.tags.clear()
                
                # Parse comma-separated tags
                tag_names = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
                
                # Create or get tags and add to note
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name.lower(),
                        user=note.user
                    )
                    note.tags.add(tag)
            else:
                # If no tags provided, clear all tags
                note.tags.clear()
            
            self.save_m2m()
        
        return note
