# Transform to Minimal Landing Page + Complete History Archive

## Strategy

Ultra-clean professional site:
- **index.md**: 80-word landing page with CTAs
- **history.md**: Complete archive (about + people + projects + anthology)
- **support.md**: Unchanged
- **anthology/*.md**: 296 essays remain accessible via direct URL
- **projects/*.md**: Individual project pages remain for history links
- **Delete**: about.md, people.md, projects.md, anthology.md (after copying to history)

## Implementation Steps

### 1. Create `history.md`

Comprehensive archive combining four sections:

**Section 1: About**
- Complete content from about.md (27 lines)
- Full chronological biography from 2006-2024
- Education, licensing, achievements
- All career milestones and transitions

**Section 2: People**
- Complete content from people.md
- All 138 names who taught you
- "These people taught me things I could not have learnt otherwise"

**Section 3: Projects**
- Complete content from projects.md
- All 150+ projects with links to detail pages
- Full chronological list preserved

**Section 4: Anthology**
- Complete content from anthology.md
- All 296 essay links
- Description and index

### 2. ⚠️ VERIFICATION CHECKPOINT - STOP HERE

**DO NOT PROCEED WITHOUT USER APPROVAL**

After creating history.md, user must verify:

- [ ] All content from about.md appears in Section 1
- [ ] All 138 names from people.md appear in Section 2
- [ ] All 150+ projects from projects.md appear in Section 3
- [ ] All 296 essay links from anthology.md appear in Section 4
- [ ] All hyperlinks are preserved and functional
- [ ] No content is truncated, corrupted, or missing

**User must explicitly approve before proceeding to deletions.**

### 3. Simplify `index.md`

Replace entirely with minimal ~80-word landing:

```markdown
Kushal Samant

Licensed Architect & SaaS Developer
Building tools that preserve human voice in AI systems

[View Projects] → kvshvl.vercel.app
[Schedule Consultation] → kvshvl.setmore.com
[LinkedIn] → linkedin.com/in/kvshvl

Based in Navi Mumbai, India
+91 87796 32310
writetokushaldsamant@gmail.com
```

**Navigation (in index.md):**
```html
<nav class="main-navigation" role="navigation" aria-label="Main navigation">
    <a href="https://kvshvl.vercel.app" rel="noopener noreferrer" target="_blank">SaaS</a>
    <a href="https://kushalsamant.github.io/support.html">Support</a>
</nav>
```

Remove:
- Hero quote
- All project descriptions
- Work philosophy sections
- Old navigation links (About, People, Projects, "Get in Touch")

### 4. Update Footer in `_layouts/default.html`

**Add History link** to footer Legal section (around line 144-148):
```html
<a href="https://kushalsamant.github.io/history.html">History</a>
```

**Remove any dead links** that point to:
- About
- People  
- Projects
- Anthology (if linked separately from navigation or footer)

### 5. Delete Files (ONLY AFTER VERIFICATION)

**ONLY proceed after user confirms Step 2 verification**, delete:

- `about.md`
- `people.md`
- `projects.md`
- `anthology.md`

### 6. Setup Redirects

Add redirect rules for deleted pages to homepage:

- `/about.html` → `/`
- `/people.html` → `/`
- `/projects.html` → `/`
- `/anthology.html` → `/`

**Implementation options:**
1. Jekyll redirect-from plugin (add to _config.yml)
2. Create simple HTML redirect files
3. GitHub Pages settings (if available)

## Files Explicitly KEPT (No Changes)

- `support.md` - unchanged
- `anthology/*.md` - all 296 essay files remain
- `projects/*.md` - all individual project detail pages remain
- `_layouts/`, `_includes/`, `assets/` - unchanged except footer edit in default.html

## Final Site Structure

```
index.md (minimal 80-word landing)
history.md (complete archive: about+people+projects+anthology)
support.md (contact/consultation - unchanged)
anthology/*.md (296 essays - direct URL access only)
projects/*.md (detail pages - linked from history)
_layouts/
_includes/
assets/
```

**Navigation:** SaaS | Support

**Footer:** History link added to Legal section

## Expected Result

- Ultra-clean first impression with clear CTAs
- One comprehensive history archive accessible from footer
- No dead links anywhere on the site
- All content preserved and accessible
- Legacy URLs redirect gracefully to homepage
- Professional, minimal presentation focused on current work (SaaS)

## Implementation Checklist

- [ ] Step 1: Create history.md with all 4 sections
- [ ] Step 2: VERIFICATION - User confirms all content copied correctly
- [ ] Step 3: Replace index.md with minimal landing
- [ ] Step 4: Update footer to add History, remove dead links
- [ ] Step 5: Delete about.md, people.md, projects.md, anthology.md
- [ ] Step 6: Setup redirects for deleted pages

