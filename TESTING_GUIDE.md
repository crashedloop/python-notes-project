# Testing Guide - Notes App Features

## Quick Start

The development server should already be running. If not, start it with:
```bash
python manage.py runserver
```

Then open your browser to: `http://127.0.0.1:8000/`

---

## Feature Testing Checklist

### 1. Test Note Title Visibility ✅

**Steps:**
1. Navigate to the main notes page
2. Hover over any existing note card
3. Observe the note title

**Expected Result:**
- ✅ Title remains clearly visible in both light and dark modes
- ✅ Smooth color transition on hover
- ✅ No invisible or too-bright text

---

### 2. Test Image Upload ✅

**Steps:**
1. Click on the note title input box to expand the create form
2. Look for the image icon (📷) in the editor toolbar
3. Click the image icon
4. Select one or more images from your computer
5. Wait for preview thumbnails to appear below the editor
6. Hover over a thumbnail to see the remove (×) button
7. Click "Close" to save the note

**Expected Result:**
- ✅ File picker opens when clicking image icon
- ✅ Image previews appear immediately after selection
- ✅ Preview shows 80x80px thumbnails with rounded corners
- ✅ Remove button appears on hover
- ✅ Images are included in the saved note
- ✅ Form clears completely after submission

---

### 3. Test To-Do List Feature ✅

**Steps:**
1. Create a new note with the following markdown content:
   ```
   # My Tasks
   - [ ] Buy groceries
   - [ ] Walk the dog
   - [x] Complete homework
   - [ ] Call mom
   ```

2. Click "Close" to save
3. Click on the note to view it
4. Interact with the checkboxes

**Expected Result:**
- ✅ Checkboxes render as Google Keep-style (rounded, gray border)
- ✅ Clicking a checkbox toggles its state
- ✅ Checked items get strikethrough text
- ✅ Checked items smoothly move to the bottom of the list
- ✅ Hover effect shows subtle background change
- ✅ Checkboxes work in both light and dark modes

---

### 4. Test Duplicate Note Bug Fix ✅

**Steps:**
1. Create a new note with title "Test Note" and some content
2. Click "Close" to save
3. Observe the "new note" input box at the top

**Expected Result:**
- ✅ Form is completely cleared (no text remains)
- ✅ No empty duplicate note appears in the new note box
- ✅ The saved note appears in the grid below
- ✅ You can immediately create another note

---

### 5. Test UI Improvements ✅

**Light Mode:**
1. Ensure light mode is active (moon icon in navbar)
2. Check the following:
   - ✅ Clean white background
   - ✅ Proper text contrast (readable titles and content)
   - ✅ Gray borders on note cards
   - ✅ Blue accent buttons (#1a73e8)
   - ✅ Smooth hover effects on cards
   - ✅ Action buttons appear on card hover

**Dark Mode:**
1. Click the dark mode toggle (moon/sun icon in navbar)
2. Check the following:
   - ✅ Dark background (#202124 - Google Keep dark)
   - ✅ Light text that's easy to read
   - ✅ Gray borders visible but subtle
   - ✅ Blue accent buttons work in dark mode
   - ✅ Hover effects use darker grays
   - ✅ Scrollbar matches dark theme

**Responsive Design:**
1. Resize browser window to different widths
2. Check the following:
   - ✅ 1 column on mobile (< 640px)
   - ✅ 2 columns on tablet (640px - 1024px)
   - ✅ 3 columns on desktop (1024px - 1280px)
   - ✅ 4 columns on large screens (1280px - 1536px)
   - ✅ 5 columns on extra large screens (> 1536px)

---

## Advanced Testing

### Test Markdown Features
Create a note with this content:
```markdown
# Heading 1
## Heading 2

**Bold text** and *italic text*

- Bullet list
- Another item

1. Numbered list
2. Second item

`inline code` here

```python
# Code block
def hello():
    print("Hello, World!")
```

[Link to Google](https://google.com)
```

**Expected Result:**
- ✅ All markdown renders correctly
- ✅ Code blocks have proper syntax highlighting
- ✅ Links are clickable and styled in blue
- ✅ Headings have proper hierarchy
- ✅ Colors match Google Keep palette

---

### Test Image + To-Do Combination
Create a note with:
```markdown
# Shopping List
- [ ] Apples
- [ ] Bananas
- [x] Milk

[Upload an image using the image button]
```

**Expected Result:**
- ✅ To-do items work correctly
- ✅ Image appears below the to-do list
- ✅ Both features work together seamlessly

---

### Test Pin Feature
1. Hover over a note card
2. Click the pin icon (📌)
3. Observe the note

**Expected Result:**
- ✅ "Pinned" badge appears on the note
- ✅ Note moves to the top of the grid
- ✅ Pin icon changes color (yellow)
- ✅ Click again to unpin

---

### Test Edit Workflow
1. Click on any note to edit it
2. Make changes to title or content
3. Upload additional images
4. Add to-do items
5. Click "Save Changes"

**Expected Result:**
- ✅ Edit page has consistent Google Keep styling
- ✅ Changes save correctly
- ✅ Redirects back to note list
- ✅ Updated note shows new content

---

### Test Delete and Restore
1. Hover over a note
2. Click the delete icon (🗑️)
3. Note disappears from the list
4. Navigate to "Recycle Bin" (trash icon in navbar)
5. Click "Restore" on the deleted note

**Expected Result:**
- ✅ Note is soft-deleted (not permanently removed)
- ✅ Appears in recycle bin
- ✅ Can be restored successfully
- ✅ Restored note returns to main list

---

## Performance Checks

### Page Load Speed
- ✅ Main page loads quickly (< 1 second)
- ✅ Images load progressively
- ✅ No visible lag when creating notes

### Smooth Animations
- ✅ Hover effects are smooth (150ms transitions)
- ✅ Checkbox toggle is instant
- ✅ Note creation/deletion animates nicely
- ✅ No jank or stuttering

### HTMX Functionality
- ✅ Form submission works without page refresh
- ✅ Note cards update dynamically
- ✅ Pin/unpin works without reload
- ✅ Delete works without reload

---

## Common Issues & Solutions

### Issue: Images not uploading
**Solution:** Check that:
- Font Awesome CDN is loaded (check browser console)
- Image size is under 5MB
- File type is JPEG, PNG, GIF, or WEBP

### Issue: To-do checkboxes not interactive
**Solution:** Make sure you're viewing the note (not just the preview card)
- Click on the note to open the view page
- Checkboxes only work in the full view, not in card previews

### Issue: Dark mode not working
**Solution:** 
- Check browser's local storage for theme setting
- Toggle the dark mode button in the navbar
- Refresh the page if needed

### Issue: Form not clearing after submit
**Solution:** This should be fixed now, but if it persists:
- Clear browser cache
- Check browser console for JavaScript errors
- Make sure HTMX library is loaded

---

## Browser Console Checks

Open browser developer tools (F12) and check:
1. **Console tab:** Should have no red errors
2. **Network tab:** All resources should load (200 status)
3. **Elements tab:** Inspect note cards to verify Google Keep colors are applied

---

## Accessibility Testing

### Keyboard Navigation
- ✅ Tab through all interactive elements
- ✅ Enter key submits forms
- ✅ Space bar checks/unchecks checkboxes
- ✅ Escape key closes modals (if any)

### Screen Reader Support
- ✅ Checkboxes have proper labels
- ✅ Buttons have descriptive titles
- ✅ Form inputs have labels
- ✅ Images have alt text

---

## Success Criteria

All features working correctly if:
1. ✅ Note title visible on hover
2. ✅ Images upload and display properly
3. ✅ To-do lists are interactive like Google Keep
4. ✅ No duplicate empty notes after creation
5. ✅ UI looks modern and matches Google Keep
6. ✅ Dark mode works perfectly
7. ✅ All HTMX interactions work smoothly
8. ✅ Responsive design works on all screen sizes
9. ✅ No console errors
10. ✅ Fast and smooth performance

---

## Next Steps

If all tests pass:
- ✅ Application is production-ready
- ✅ All requested features work correctly
- ✅ UI is polished and professional

If any tests fail:
- Check browser console for errors
- Verify all files were saved
- Restart the development server
- Clear browser cache

---

## Support

If you encounter any issues, check:
1. `FIXES_SUMMARY.md` - Detailed explanation of all changes
2. Browser console for JavaScript errors
3. Django console for server errors
4. Network tab for failed resource loads

