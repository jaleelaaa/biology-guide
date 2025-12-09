# Plus One Biology Interactive Website - Setup Guide

## ✅ Completed Structure

### Main Website (Root Level)
```
Web/
├── index.html ✅ (Home page with all chapters)
├── css/
│   ├── base.css ✅ (Shared design system)
│   └── study-guide.css ✅ (Study guide specific styles)
├── js/ (For future JavaScript files)
├── assets/ (For shared images/icons)
└── chapters/
    └── 01-cell-the-unit-of-life/
        ├── index.html ⏳ (Needs completion)
        ├── README.md ✅
        ├── diagrams/ (11 HTML files needed)
        └── assets/ (Chapter-specific images)
```

## 📋 What's Been Created

### ✅ Completed Files:

1. **Web/index.html** - Main home page
   - Hero section
   - Features grid
   - Chapter cards (Chapter 1 active, others "Coming Soon")
   - Footer
   - Responsive design

2. **Web/css/base.css** - Complete design system
   - CSS variables for colors, spacing, typography
   - Base styles for all HTML elements
   - Utility classes
   - Responsive breakpoints
   - Accessibility support
   - Print styles

3. **Web/css/study-guide.css** - Study guide specific styles
   - Interactive diagram callouts
   - Exam tips styling
   - Flashcard styles
   - Section headers
   - Comparison tables
   - Sidebar navigation

4. **Web/chapters/01-cell-the-unit-of-life/README.md**
   - Lists all 11 interactive diagrams
   - File structure documentation

## ⏳ Next Steps to Complete

### 1. Complete Chapter 1 Index Page

Create: `Web/chapters/01-cell-the-unit-of-life/index.html`

**Structure Needed:**
- Navigation bar with "Back to Home" link
- Sidebar with table of contents
- Main content area with:
  - Chapter overview
  - Links to all 11 interactive diagrams (in grid layout)
  - Key topics summary
  - Quick reference cards
  - Exam tips section
  - Footer

**Template HTML Structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chapter 1: Cell - The Unit of Life</title>
    <link rel="stylesheet" href="../../css/base.css">
    <link rel="stylesheet" href="../../css/study-guide.css">
</head>
<body>
    <nav><!-- Back to Home link --></nav>

    <div class="layout-grid">
        <aside class="sidebar-toc">
            <!-- Table of Contents -->
        </aside>

        <main class="study-guide">
            <!-- Chapter content -->
            <!-- Interactive diagrams grid -->
            <!-- Key topics -->
            <!-- Exam tips -->
        </main>
    </div>

    <footer><!-- Footer --></footer>
</body>
</html>
```

### 2. Create 11 Interactive Diagram HTML Files

All files go in: `Web/chapters/01-cell-the-unit-of-life/diagrams/`

Each diagram needs standalone HTML with:
- React loaded via CDN
- Babel standalone for JSX transformation
- Import of the corresponding JSX component
- Back button to chapter index
- Proper styling

**Files to Create:**

1. **fluid-mosaic-model.html**
   - Source: `Docs/Cell-The-Unit-of-Life/chapter-images/interactive/FluidMosaicInteractive.jsx`

2. **mitochondria.html**
   - Source: `Docs/Cell-The-Unit-of-Life/chapter-images/interactive/MitochondriaInteractive.jsx`

3. **chloroplast.html**
   - Source: `Docs/Cell-The-Unit-of-Life/chapter-images/interactive/ChloroplastInteractive.jsx`

4. **nucleus.html**
   - Source: `Docs/Cell-The-Unit-of-Life/chapter-images/interactive/NucleusInteractive.jsx`

5. **plant-animal-cells.html**
   - Source: `Docs/Cell-The-Unit-of-Life/chapter-images/interactive/PlantAnimalCellInteractive.jsx`

6. **rer-ser.html**
   - Source: `Docs/Cell-The-Unit-of-Life/chapter-images/interactive/RERSERInteractive.jsx`

7. **golgi-er.html**
   - Source: `Docs/Cell-The-Unit-of-Life/chapter-images/interactive/GolgiERInteractive.jsx`

8. **prokaryotic-cell.html**
   - Source: `Docs/Cell-The-Unit-of-Life/chapter-images/interactive/ProkaryoticCellInteractive.jsx`

9. **chromosome-types.html**
   - Source: `Docs/Cell-The-Unit-of-Life/chapter-images/interactive/ChromosomeTypesInteractive.jsx`

10. **plastids.html**
    - Source: `Docs/Cell-The-Unit-of-Life/chapter-images/interactive/PlastidsInteractive.jsx`

11. **cell-wall.html**
    - Source: `Docs/Cell-The-Unit-of-Life/chapter-images/interactive/CellWallInteractive.jsx`

**Template for Each Diagram HTML:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Diagram Name] - Interactive</title>

    <!-- React & Babel -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

    <!-- Styles -->
    <link rel="stylesheet" href="../../../css/base.css">
    <style>
        /* Inline the specific CSS for this diagram */
    </style>
</head>
<body>
    <a href="../index.html" class="back-button">← Back to Chapter</a>
    <div id="root"></div>

    <script type="text/babel">
        // Copy the JSX component code here
        // Then render it:
        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<ComponentName />);
    </script>
</body>
</html>
```

## 🚀 Alternative: Build Setup (Recommended for Production)

For better performance and easier maintenance, consider:

1. **Use Vite or Create React App**
   ```bash
   npm create vite@latest biology-study-guide -- --template react
   ```

2. **Structure:**
   ```
   src/
   ├── components/
   │   ├── diagrams/
   │   │   ├── FluidMosaicInteractive.jsx
   │   │   └── ... (all 11)
   │   └── ...
   ├── pages/
   │   ├── Home.jsx
   │   ├── Chapter1.jsx
   │   └── ...
   └── App.jsx
   ```

3. **Benefits:**
   - Faster loading (bundled and optimized)
   - Better code organization
   - Easy to add new chapters
   - Hot module replacement during development

## 📝 Content Integration

### Converting Markdown to HTML

The full study guide is in:
`Docs/Cell-The-Unit-of-Life/chapter-doc/Cell_The_Unit_of_Life_Study_Guide.md`

**Options:**
1. **Manual HTML conversion** - Copy sections and wrap in HTML
2. **Use markdown-it** - JavaScript library to convert on the fly
3. **Build-time conversion** - Use tools like marked or remark during build

### Recommended Sections to Include:

- Cell Theory
- Cell Discovery Timeline
- Prokaryotic Cell Structure
- Eukaryotic Cell Structure
- Plant vs Animal Cell Comparison
- Plasma Membrane (Fluid Mosaic Model)
- Cell Wall Structure
- Cell Organelles (detailed)
- Endomembrane System
- Plastids Classification
- Chromosome Types
- Flashcards (as collapsible details)
- Exam Questions Bank

## 🎨 Design System

### Colors (Already in base.css):
- Primary: `#4169E1` (Royal Blue)
- Secondary: `#0047AB` (Cobalt Blue)
- Accent: `#FF6347` (Tomato)
- Success: `#4CAF50` (Green)
- Warning: `#FF9800` (Orange)

### Spacing Scale:
- xs: 0.25rem
- sm: 0.5rem
- md: 1rem
- lg: 1.5rem
- xl: 2rem
- xxl: 3rem

### Typography:
- Base: 16px
- Headings: 2.5rem to 1rem (h1 to h6)
- Font: System font stack (-apple-system, etc.)

## 🧪 Testing Checklist

- [ ] Home page loads correctly
- [ ] Chapter 1 page loads correctly
- [ ] All 11 diagram links work
- [ ] Back navigation works everywhere
- [ ] Responsive on mobile (< 768px)
- [ ] Responsive on tablet (768px - 992px)
- [ ] Responsive on desktop (> 992px)
- [ ] All interactive diagrams render correctly
- [ ] Print styles work
- [ ] Accessibility (keyboard navigation, screen readers)

## 📦 Deployment Options

1. **GitHub Pages** (Free)
   - Push to GitHub
   - Enable Pages in settings
   - Access at: username.github.io/repo-name

2. **Netlify** (Free)
   - Drag and drop Web folder
   - Or connect to GitHub repo

3. **Vercel** (Free)
   - Similar to Netlify
   - Great for React apps

4. **Local Server** (For testing)
   ```bash
   cd Web
   python -m http.server 8000
   # Or
   npx serve
   ```

## 📚 Future Chapters Template

When adding Chapter 2 (Biomolecules):

1. Create folder: `Web/chapters/02-biomolecules/`
2. Copy structure from Chapter 1
3. Create new interactive diagrams
4. Add chapter card to main index.html
5. Update navigation

## 💡 Tips

1. **Development**: Use a local server (Live Server in VS Code)
2. **Images**: Optimize all images before adding (use WebP format)
3. **Performance**: Consider lazy loading for diagrams
4. **SEO**: Add proper meta tags to all pages
5. **Analytics**: Consider adding Google Analytics
6. **Offline**: Add service worker for offline access

## 🆘 Common Issues

### Issue: React component not rendering
**Solution**: Check browser console for errors. Ensure:
- React and ReactDOM scripts load before Babel
- JSX is in `<script type="text/babel">`
- Component name matches in render call

### Issue: CSS not loading
**Solution**: Check relative paths:
- From chapter index: `../../css/base.css`
- From diagram: `../../../css/base.css`

### Issue: Images not showing
**Solution**:
- Use relative paths
- Or copy images to `assets/` folder

## 📞 Support

For questions or issues:
- Check browser console (F12)
- Verify file paths
- Test in different browsers
- Check responsive design in DevTools

---

**Next Action**: Create the 11 diagram HTML files and complete Chapter 1 index.html following the templates above.
