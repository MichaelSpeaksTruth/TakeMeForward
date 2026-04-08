# 🗓️ Wall Calendar - Quick Reference

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd frontend
npm install react lucide-react date-fns tailwindcss postcss autoprefixer
```

### 2. Ensure Images are in Place
```
public/images/months/
├── 01-jan.jpg
├── 02-feb.jpg
├── 03-march.webp
├── 04-april.jpeg
├── 05-may.webp
├── 06-june.webp
├── 07-july.jpg
├── 08-august.webp
├── 09-sep.jpeg
├── 10-oct.jpg
├── 11-nov.jpg
└── 12-dec.jpg
```

### 3. Import Component
```jsx
import WallCalendar from "./components/WallCalendar";

function App() {
  return <WallCalendar />;
}
```

### 4. Run Dev Server
```bash
npm run dev
```

---

## 📋 Component Features

| Feature | Description |
|---------|-------------|
| **Hero Image** | Changes monthly, handles mixed image formats (jpg, jpeg, webp) |
| **Month Navigation** | Previous/Next buttons to switch months |
| **Date Range Selection** | Click two dates to select a range with visual highlighting |
| **Interactive Calendar** | 7-day grid with current month days highlighted |
| **Notes Section** | Auto-saving notes tied to month or date range |
| **Local Storage** | Persistent data across page refreshes |
| **Responsive Design** | Side-by-side on desktop, stacked on mobile |

---

## 🎨 Layout Details

### Desktop (≥1024px)
```
┌─────────────────┬──────────────────┐
│                 │                  │
│   Hero Image    │  Calendar Grid   │
│   (Left Panel)  │  (Right Panel)   │
│                 │  + Notes Below   │
└─────────────────┴──────────────────┘
```

### Mobile (<1024px)
```
┌──────────────────┐
│  Hero Image      │
├──────────────────┤
│  Calendar Grid   │
├──────────────────┤
│  Notes Section   │
└──────────────────┘
```

---

## 🎯 User Interactions

### Date Range Selection
1. **First Click** → Selects start date (blue background)
2. **Second Click** → Selects end date (blue background)
   - If clicked date < start date: auto-reorders
   - In-between days: light blue background
3. **Third Click** → Resets and starts new range

### Notes
- **Tied to Selection**: Different notes for different ranges
- **Auto-Save**: Saves instantly as you type
- **Per-Month**: Each month has "General Memos"
- **Per-Range**: Each date range has dedicated notes

### Navigation
- **Previous/Next Buttons**: Switch months
- **Hero Image Updates**: Automatically when month changes
- **Calendar Grid Updates**: Shows current month days
- **Notes Context**: Switches to "General [Month]" notes

---

## 🔑 Key Technologies

- **React 18+**: Component state management
- **Tailwind CSS**: Responsive styling & design system
- **Lucide Icons**: SVG icons (ChevronLeft, ChevronRight, X)
- **date-fns**: Date manipulation (formatting, interval checks, month math)
- **localStorage**: Client-side data persistence

---

## 💾 Local Storage Structure

```javascript
// Key Format 1: General monthly notes
localStorage.getItem("general-2024-04")
// Returns: "My April notes here..."

// Key Format 2: Date range notes
localStorage.getItem("range-20240410-20240415")
// Returns: "My notes for April 10-15..."
```

---

## 🎨 Color Palette (Tailwind)

| Element | Tailwind Class |
|---------|---|
| Start/End Date | `bg-blue-600 text-white` |
| Range Background | `bg-blue-200 text-blue-900` |
| Regular Day | `bg-gray-100 hover:bg-blue-100` |
| Main Background | `bg-gradient-to-br from-slate-100 to-slate-200` |
| Containers | `bg-white` |

---

## 📦 Month Images Mapping

```javascript
const monthImages = {
  0: "/images/months/01-jan.jpg",
  1: "/images/months/02-feb.jpg",
  2: "/images/months/03-march.webp",    // Note: "march" not "mar"
  3: "/images/months/04-april.jpeg",    // Note: "april" not "apr"
  4: "/images/months/05-may.webp",
  5: "/images/months/06-june.webp",     // Note: "june" not "jun"
  6: "/images/months/07-july.jpg",      // Note: "july" not "jul"
  7: "/images/months/08-august.webp",   // Note: "august" not "aug"
  8: "/images/months/09-sep.jpeg",
  9: "/images/months/10-oct.jpg",
  10: "/images/months/11-nov.jpg",
  11: "/images/months/12-dec.jpg",
};
```

---

## 🚨 Common Issues & Fixes

### Images not showing?
- ✅ Images in `public/images/months/` ?
- ✅ Filenames match `monthImages` object?
- ✅ Dev server running (`npm run dev`)?
- ✅ Browser cache cleared?

### Notes disappearing?
- ✅ localStorage enabled in browser?
- ✅ Not exceeding 5-10MB storage limit?
- ✅ Private/Incognito mode allows localStorage?

### Styles look broken?
- ✅ Tailwind CSS configured in `tailwind.config.js`?
- ✅ `@tailwind` directives in `src/index.css`?
- ✅ All required packages installed?

---

## 📱 Responsive Breakpoints

```
Mobile:         < 768px   (Full width, stacked)
Tablet:     768px - 1024px (Adjusted spacing)
Desktop:       ≥ 1024px   (Side-by-side layout)
```

---

## ⚡ Performance Features

✅ Lazy image loading (`loading="lazy"`)
✅ Smooth CSS transitions
✅ No infinite re-renders
✅ Efficient date calculations (date-fns)
✅ LocalStorage instead of backend calls

---

## 🎁 Included Features

- ✅ **12 Different Monthly Images** with mixed formats
- ✅ **Dynamic Hero Image** that updates monthly
- ✅ **Interactive Calendar Grid** with proper date layout
- ✅ **Date Range Selection** with auto-ordering
- ✅ **Context-Aware Notes** (per month or per range)
- ✅ **Auto-Save to LocalStorage** as you type
- ✅ **Fully Responsive** (Desktop, Tablet, Mobile)
- ✅ **Smooth Animations** and transitions
- ✅ **Clean, Production-Ready Code**
- ✅ **No Backend Required**

---

## 📖 Related Files

- **Component**: `src/components/WallCalendar.jsx`
- **Integration**: `src/App.jsx`
- **Full Setup Guide**: `WALL_CALENDAR_SETUP.md`
- **Images**: `public/images/months/`
- **Styling**: `src/index.css` (with Tailwind directives)

---

**Ready to use! Just import and run.** ✨
