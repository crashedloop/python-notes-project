# 🧪 Testing the New Google Keep Features

## Quick Start

The Django development server should now be running at: **http://127.0.0.1:8000/**

---

## 🎯 Feature Testing Guide

### 1. Test Search System

**Steps:**
1. Navigate to the main notes page
2. Look for the search bar in the navbar (top right)
3. Type in the search box
4. Results should update automatically after 300ms
5. Try searching for:
   - Part of a note title
   - Content from a note
   - A tag name

**Expected Behavior:**
- Notes filter instantly as you type
- "No matching notes found" message appears if no results
- Search works with filters and sorting active

---

### 2. Test Tags Feature

**Creating Notes with Tags:**
1. Click the yellow floating "+" button (bottom right)
2. Fill in title and content
3. In the "Tags" field, type: `work, important, idea`
4. Click "Save Note"
5. Note should appear with colored tag chips

**Filtering by Tags:**
1. Look for the "Tags:" section above the notes
2. Click any tag chip
3. Notes should filter to show only that tag
4. "Clear Tag Filter" button appears
5. Click to reset filter

**Tag Colors:**
- Each tag gets a unique pastel color
- Same tag name = same color (consistent)
- Colors are dark-mode friendly

---

### 3. Test Filtering

**Filter Buttons:**
1. Find "Filter:" section above notes
2. Click "All Notes" - shows everything
3. Click "📌 Pinned" - shows only pinned notes
4. Click "Unpinned" - shows only unpinned notes
5. Active filter should be highlighted in yellow

**Combining Filters:**
- Try: Filter by "Pinned" + Search for keyword
- Try: Filter by tag + Sort by "A→Z"
- All combinations should work together

---

### 4. Test Sorting

**Sorting Options:**
1. Find the "Sort:" dropdown
2. Try each option:
   - Last Updated (default)
   - Newest First
   - Oldest First
   - A → Z
   - Z → A
3. Notes should reorder instantly
4. Pinned notes always stay at top

---

### 5. Test UI/UX Improvements

**Glassmorphism:**
- Note cards should have a subtle blur/transparency effect
- Hover over note cards - they should lift up and scale slightly
- Search bar has glassmorphism effect
- Filter buttons have blur effect

**Hover Effects:**
- Note cards: Lift up, scale, and show actions
- Tag chips: Scale up and shadow increases
- Title should NOT become invisible (fixed bug)

**Modal:**
- Open note creation modal
- Add note with tags
- Save note
- Reopen modal - should be completely empty (no leftover data)

---

### 6. Test Dark Mode

**Toggle Dark Mode:**
1. Click the moon/sun icon in navbar
2. Theme should switch instantly
3. Check that:
   - Tag colors are still visible
   - Glassmorphism effects work
   - Note cards have yellow glow on hover
   - Search bar looks good
   - All text is readable

---

## ⚠️ Common Issues & Solutions

### Issue: Search doesn't work
**Solution:** Make sure you're logged in and have notes created

### Issue: Tags don't show on cards
**Solution:** Edit a note and add tags in the format: `tag1, tag2, tag3`

### Issue: Filter buttons don't highlight
**Solution:** Refresh the page, HTMX should be loaded

### Issue: No tag cloud appears
**Solution:** Create notes with tags first, then the tag cloud will appear

---

## 🔍 Visual Checklist

When testing, verify these visual elements:

### Search Bar:
- [ ] Visible in navbar (desktop only, hidden on mobile)
- [ ] Search icon on the left
- [ ] Placeholder text clear
- [ ] Rounded full design
- [ ] Focus ring appears (yellow)

### Tag Chips:
- [ ] Rounded full shape
- [ ] Pastel background colors
- [ ] Dark text (#202124)
- [ ] Hover: Scale up + shadow
- [ ] On note cards below content

### Filter Buttons:
- [ ] Rounded full shape
- [ ] Active = yellow background + white text
- [ ] Inactive = gray background
- [ ] Hover effect visible

### Note Cards:
- [ ] Glassmorphism effect (blur + transparency)
- [ ] Hover: Lift up + scale + shadow
- [ ] Title doesn't disappear on hover
- [ ] Action buttons appear on hover
- [ ] Tags display at bottom

---

## 🎨 Color Reference

**Tag Pastel Colors:**
- Yellow: #FFD580
- Blue: #A1C6EA
- Green: #C3F0CA
- Pink: #FFB3BA
- Orange: #FFDFBA
- Lemon: #FFFFBA
- Mint: #BAFFC9
- Sky Blue: #BAE1FF
- Lavender: #E0BBE4
- Peach: #FFDFD3

**Active Filter:**
- Background: Yellow (#FBBC04)
- Text: White

**Dark Mode Accent:**
- Search focus: Yellow ring
- Hover glow: Yellow/500

---

## 🚀 Advanced Testing

### Test Complex Queries:
1. Create 10+ notes
2. Add various tags to each
3. Search + Filter + Sort simultaneously
4. Switch between filters while searching
5. Click tags while search is active

### Test Performance:
1. Type quickly in search bar
2. Verify 300ms debounce works
3. No lag or delay
4. HTMX requests visible in Network tab

### Test Mobile Responsiveness:
1. Resize browser to mobile size
2. Search bar should hide (hidden md:block)
3. Notes should stack in columns
4. Touch interactions should work

---

## 📊 Expected Results

**All Tests Pass:**
✅ Search works instantly
✅ Tags display with colors
✅ Filters work alone and combined
✅ Sorting works correctly
✅ UI is smooth and polished
✅ Dark mode looks great
✅ No console errors
✅ No server errors

**If Any Test Fails:**
1. Check browser console for errors
2. Check Django server logs
3. Verify you're logged in
4. Try hard refresh (Ctrl+Shift+R)
5. Clear browser cache

---

## 🎉 Success Criteria

Your app is ready when:
- ✅ You can search notes in real-time
- ✅ Tags appear on notes and are clickable
- ✅ Filtering and sorting work together
- ✅ UI feels smooth and modern
- ✅ Dark mode looks beautiful
- ✅ Everything works without errors

---

## 🐛 Debugging Tips

**Check HTMX:**
```javascript
// In browser console:
htmx.logAll(); // Enable HTMX logging
```

**Check Django Queries:**
```python
# In views.py, add temporary print:
print(notes.query)  # See the SQL query
```

**Check Tags:**
```python
# In Django shell:
python manage.py shell
from notes.models import Tag, Note
Tag.objects.all()  # List all tags
```

---

## 📝 Test Data Suggestions

Create notes with these tags for best testing:

**Note 1:**
- Title: "Team Meeting Notes"
- Tags: `work, meeting, important`
- Content: Meeting agenda and action items

**Note 2:**
- Title: "Project Ideas"
- Tags: `idea, brainstorming, creative`
- Content: List of project ideas

**Note 3:**
- Title: "Shopping List"
- Tags: `personal, shopping, groceries`
- Content: - [ ] Milk, - [ ] Bread, - [ ] Eggs

**Note 4:**
- Title: "Code Review Checklist"
- Tags: `work, code, development`
- Content: Code review guidelines

**Note 5:**
- Title: "Weekend Plans"
- Tags: `personal, leisure, weekend`
- Content: Fun activities for the weekend

---

## ✅ Final Checklist

Before marking as complete, verify:

- [ ] Django server runs without errors
- [ ] Can create notes with tags
- [ ] Search bar appears and works
- [ ] Tag cloud displays correctly
- [ ] Filter buttons work
- [ ] Sort dropdown works
- [ ] Note cards look polished
- [ ] Glassmorphism effects visible
- [ ] Dark mode works perfectly
- [ ] No JavaScript errors in console
- [ ] Modal resets after saving
- [ ] Edit page shows tags correctly

---

**Happy Testing! 🚀**

If everything works as expected, you now have a fully-featured Google Keep clone!

