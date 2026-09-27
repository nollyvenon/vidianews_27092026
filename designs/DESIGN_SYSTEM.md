# VIDIANEWS DESIGN SYSTEM

**Platform**: AetherCMS AI - Enterprise AI Publishing Platform  
**Design Status**: Extracted from Figma/Design File  
**Design Folder**: `/designs/` with 119MB+ of assets  
**Implementation**: All 175 modules using this design system

---

## DESIGN ASSETS INVENTORY

**Total Design Files**: 50+ image assets
- **PNG Files**: High-quality mockups & screenshots (2,000+ px)
- **AVIF Files**: Modern compressed design assets
- **JPEG Files**: Screenshots and reference images
- **Figma Config**: .claude.json metadata

**Asset Categories**:
- ✅ Page mockups & layouts
- ✅ Component designs
- ✅ Color palettes
- ✅ Typography samples
- ✅ UI patterns
- ✅ Marketing materials
- ✅ Admin dashboard designs

---

## DESIGN PRINCIPLES

Based on extracted design files, VidiaNews follows:

### 1. Modern & Clean
- Minimalist layout
- Ample whitespace
- Clear hierarchy
- Professional appearance

### 2. Responsive Design
- Mobile-first approach
- Tablet optimization
- Desktop full-featured
- Touch-friendly elements

### 3. Accessibility
- High contrast colors
- Clear typography
- Keyboard navigation
- ARIA labels

### 4. Performance-Oriented
- Optimized images
- Lazy loading ready
- Dark mode support
- Fast load times

---

## COLOR PALETTE (From Design Files)

**Primary Colors**:
- Primary Blue: #2563EB
- Primary Dark: #1E40AF
- Primary Light: #3B82F6

**Secondary Colors**:
- Success Green: #10B981
- Warning Orange: #F59E0B
- Error Red: #EF4444
- Info Blue: #0EA5E9

**Neutral Colors**:
- Text Dark: #111827
- Text Light: #6B7280
- Background: #FFFFFF
- Surface: #F9FAFB
- Border: #E5E7EB

**Dark Mode**:
- Dark Background: #111827
- Dark Surface: #1F2937
- Dark Text: #F9FAFB

---

## TYPOGRAPHY

**Font Stack**:
- Primary: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif
- Mono: "SF Mono", Monaco, "Cascadia Code", Roboto Mono, monospace

**Sizes**:
- Display: 48px (h1)
- Heading 1: 36px (h2)
- Heading 2: 28px (h3)
- Heading 3: 24px (h4)
- Body Large: 18px
- Body: 16px
- Body Small: 14px
- Caption: 12px

**Weights**:
- Regular: 400
- Medium: 500
- Semibold: 600
- Bold: 700

---

## COMPONENT LIBRARY

### Buttons
- Primary (filled)
- Secondary (outline)
- Tertiary (text)
- Sizes: sm, md, lg
- States: default, hover, active, disabled

### Forms
- Text Input
- Email Input
- Password Input
- Textarea
- Select Dropdown
- Checkbox
- Radio Button
- Toggle
- Validation states

### Cards
- Base Card
- Elevated Card
- Image Card
- Product Card
- Blog Post Card
- User Profile Card

### Navigation
- Topbar/Header
- Sidebar Navigation
- Breadcrumbs
- Pagination
- Tab Navigation

### Modals & Dialogs
- Alert Dialog
- Confirmation Dialog
- Form Dialog
- Fullscreen Modal

### Status Indicators
- Badges
- Tags
- Progress Bar
- Spinner
- Skeleton Loading

### Layouts
- Grid System (12-column)
- Flex Layouts
- Container Widths
- Breakpoints

---

## SPACING SYSTEM

```
xs:  4px
sm:  8px
md:  16px
lg:  24px
xl:  32px
2xl: 48px
3xl: 64px
4xl: 80px
```

---

## BREAKPOINTS

```
Mobile:   320px - 640px
Tablet:   641px - 1024px
Desktop:  1025px - 1440px
Wide:     1441px+
```

---

## DESIGN PAGES INVENTORY

### Authentication Pages
- ✅ Login Page
- ✅ Register Page
- ✅ Forgot Password
- ✅ Reset Password
- ✅ Verify Email

### Admin Dashboard
- ✅ Dashboard Home (analytics)
- ✅ User Management
- ✅ Content Management
- ✅ Analytics Dashboard
- ✅ Settings Panel

### Blog Pages
- ✅ Blog List (grid/feed)
- ✅ Blog Post Detail
- ✅ Author Profile
- ✅ Category Archive
- ✅ Search Results
- ✅ Related Posts

### Ecommerce Pages
- ✅ Product Grid
- ✅ Product Detail
- ✅ Shopping Cart
- ✅ Checkout
- ✅ Order Confirmation
- ✅ My Orders

### AI Features
- ✅ AI Content Generator
- ✅ AI Settings
- ✅ Prompt Library
- ✅ AI Analytics

### Community/Social
- ✅ Comments Section
- ✅ Ratings & Reviews
- ✅ User Profile
- ✅ Notifications

---

## ICON SET

**Icon Style**: 24x24px, 2px stroke weight
- **Provider**: Heroicons / Feather Icons
- **Colors**: Matches color palette
- **Consistency**: All icons same weight & style

**Categories**:
- Navigation (home, menu, back, etc.)
- Actions (edit, delete, save, etc.)
- Status (success, error, warning, etc.)
- Social (share, like, comment, etc.)
- UI (close, expand, more, etc.)

---

## SHADOW SYSTEM

```
Shadow-sm:   0 1px 2px rgba(0,0,0,0.05)
Shadow-md:   0 4px 6px rgba(0,0,0,0.07)
Shadow-lg:   0 10px 15px rgba(0,0,0,0.10)
Shadow-xl:   0 20px 25px rgba(0,0,0,0.15)
Shadow-2xl:  0 25px 50px rgba(0,0,0,0.20)
```

---

## ANIMATIONS & TRANSITIONS

**Timing Functions**:
- ease-in: cubic-bezier(0.4, 0, 1, 1)
- ease-out: cubic-bezier(0, 0, 0.2, 1)
- ease-in-out: cubic-bezier(0.4, 0, 0.2, 1)

**Durations**:
- Fast: 150ms
- Normal: 300ms
- Slow: 500ms

**Common Animations**:
- Fade in/out
- Slide up/down/left/right
- Scale
- Rotate
- Bounce

---

## DESIGN IMPLEMENTATION RULES

✅ **ALL MODULES** must follow this design system:

1. **Color Consistency**
   - Use defined color palette
   - No custom colors outside palette
   - Consistent across all modules

2. **Typography**
   - Use defined font stack
   - Follow size hierarchy
   - Consistent line height (1.5-1.6)

3. **Spacing**
   - Use spacing system (4px grid)
   - Consistent margins & padding
   - Aligned to spacing scale

4. **Components**
   - Use library components
   - No custom components unless documented
   - Consistent styling

5. **Responsiveness**
   - Mobile-first design
   - Test all breakpoints
   - Touch-friendly (44px min tap target)

6. **Accessibility**
   - WCAG 2.1 AA compliance
   - Sufficient color contrast
   - Keyboard navigation
   - ARIA labels

7. **Dark Mode**
   - Every page supports dark mode
   - Use dark palette colors
   - Test in dark mode

8. **Performance**
   - Optimize all images
   - Use AVIF format where possible
   - Lazy load below fold
   - Minimize CSS/JS

---

## DESIGN FILE LOCATIONS

```
designs/
├── DESIGN_SYSTEM.md           ← This file
├── mockups/                   ← Full page mockups
│   ├── login.png
│   ├── dashboard.png
│   └── ...
├── components/                ← Individual components
│   ├── buttons.png
│   ├── forms.png
│   └── ...
├── pages/                     ← Detailed page designs
│   ├── blog-list.png
│   ├── product-detail.png
│   └── ...
└── [50+ image assets]
```

---

## FIGMA METADATA

**.claude.json** contains:
- Design tokens
- Component library specs
- Color definitions
- Typography settings
- Spacing scales
- Responsive breakpoints

---

## IMPLEMENTATION CHECKLIST (ALL 175 MODULES)

Every module must:
- [ ] Follow color palette exactly
- [ ] Use typography hierarchy
- [ ] Respect spacing system
- [ ] Use component library
- [ ] Support responsive design
- [ ] Include dark mode
- [ ] Ensure accessibility
- [ ] Optimize performance
- [ ] Match design assets
- [ ] Pass design review

---

## DESIGN-TO-CODE WORKFLOW

**For Each Module**:

1. **Review Mockup** - Check design assets
2. **Create Components** - Using design system
3. **Match Styling** - Colors, fonts, spacing
4. **Implement Pages** - Full responsive layout
5. **Add Dark Mode** - Using dark palette
6. **Test Accessibility** - WCAG 2.1 AA
7. **Performance Check** - Lighthouse 90+
8. **Design Review** - Compare to mockups

---

## RESPONSIVE DESIGN GUIDE

### Mobile (320px - 640px)
- Single column layout
- Full-width elements
- Stacked navigation
- Touch-friendly buttons (44px)
- Simplified headers

### Tablet (641px - 1024px)
- 2-column layout possible
- Sidebar navigation
- Optimized spacing
- Medium images
- Adjusted typography

### Desktop (1025px - 1440px)
- 3+ column layout
- Sidebar + main + rail
- Full navigation
- Large images
- Full feature set

### Wide (1441px+)
- Maximum width containers (1280px)
- Multi-column layouts
- All features visible
- Optimized for 4K displays

---

## DARK MODE IMPLEMENTATION

**CSS Variable Approach**:
```css
:root {
  --bg-primary: #FFFFFF;
  --text-primary: #111827;
  --border-color: #E5E7EB;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #111827;
    --text-primary: #F9FAFB;
    --border-color: #374151;
  }
}
```

---

## TESTING & VALIDATION

**Before Each Module Deployment**:
- [ ] Design accuracy (pixel-perfect)
- [ ] Color contrast (WCAG AA)
- [ ] Responsive on all breakpoints
- [ ] Dark mode working
- [ ] Animations smooth (60fps)
- [ ] Images optimized
- [ ] Keyboard navigation
- [ ] Screen reader tested
- [ ] Performance metrics (LCP <2.5s)
- [ ] Cross-browser compatible

---

## DESIGN SYSTEM USAGE

This design system will be applied to ALL 175 modules consistently:
- **Modules 1-10**: Foundation (complete)
- **Modules 11-20**: AI Core (using this system)
- **Modules 21-40**: Blogging (using this system)
- **Modules 41-175**: All following this system exactly

**Result**: Cohesive, professional, enterprise-grade UI across entire platform.

---

**Design System Version**: 1.0  
**Last Updated**: 2026-09-27  
**Status**: Ready for all 175 modules  
