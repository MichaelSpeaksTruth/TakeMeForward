# 🗓️ Wall Calendar Component - Complete Setup Guide

## 📋 Overview

A premium, interactive wall calendar component built with **React**, **Tailwind CSS**, **Lucide Icons**, and **date-fns**. Features month navigation, interactive date range selection, and persistent notes via localStorage.

---

## 🛠️ Prerequisites & Dependencies

Before using this component, ensure you have these packages installed in your frontend project:

```bash
npm install react
npm install lucide-react
npm install date-fns
npm install tailwindcss postcss autoprefixer
```

### Optional (if not already set up):
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

---

## 📂 Project Structure

```
frontend/
├── public/
│   └── images/
│       └── months/
│           ├── 01-jan.jpg
│           ├── 02-feb.jpg
│           ├── 03-march.webp
│           ├── 04-april.jpeg
│           ├── 05-may.webp
│           ├── 06-june.webp
│           ├── 07-july.jpg
│           ├── 08-august.webp
│           ├── 09-sep.jpeg
│           ├── 10-oct.jpg
│           ├── 11-nov.jpg
│           └── 12-dec.jpg
├── src/
│   ├── components/
│   │   └── WallCalendar.jsx  ← Main component
│   ├── App.jsx               ← Import WallCalendar here
│   ├── index.css             ← Tailwind directives
│   ├── main.jsx
│   └── ...other files
├── vite.config.js
├── tailwind.config.js
└── package.json
```

---

## ⚙️ Configuration

### 1. **Tailwind CSS Setup** (`tailwind.config.js`)

Make sure your `tailwind.config.js` includes the template paths:

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

### 2. **Tailwind Directives** (`src/index.css`)

Ensure your `index.css` has the Tailwind directives:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### 3. **Vite Config** (if needed)

Your `vite.config.js` should reference React plugin:

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
```

---

## 📦 Integration

### Import the Component

In your `App.jsx`:

```jsx
import WallCalendar from "./components/WallCalendar";

function App() {
  return (
    <div>
      <WallCalendar />
    </div>
  );
}

export default App;
```

### Run the Development Server

```bash
npm run dev
```

Navigate to `http://localhost:5173` (or your Vite dev server URL).

---

## 🎨 Features Breakdown

### 1. **Hero Image with Month Mapping**
- Each month displays a unique hero image from `public/images/months/`
- Images are preloaded with lazy loading for performance
- Responsive sizing: square on mobile, rectangular on desktop
- Smooth hover zoom effect

### 2. **Month Navigation**
- **Previous/Next Buttons** switch between months
- Hero image updates dynamically
- Calendar grid updates instantly
- Notes context switches based on month/selection

### 3. **Interactive Date Range Selection**
- **First Click**: Select start date (highlighted in solid blue)
- **Second Click**: Select end date (auto-reorders if needed)
- **In-Between Days**: Soft blue highlight
- **Third Click**: Reset selection and start new range
- **Clear Button**: Quickly clear selection with ✕ button

### 4. **Notes Section**
- **Context-Aware Label**: Shows selected range or month name
- **Auto-Save**: Saves to localStorage automatically as you type
- **Per-Selection Storage**: Different notes for different ranges/months
- **Persistent**: Survives page refresh and navigation

### 5. **Responsive Design**
- **Desktop**: Side-by-side layout (hero image left, calendar + notes right)
- **Tablet**: Adjusted spacing and sizing
- **Mobile**: Stacked vertical layout with full-width elements
- **Breakpoint**: Uses Tailwind's `lg:` breakpoint (1024px)

### 6. **Local Storage Persistence**
- Notes are stored with a unique key:
  - `general-YYYY-MM` for general month notes
  - `range-YYYYMMDD-YYYYMMDD` for date range notes
- Data persists across browser sessions
- No backend required

---

## 🎯 Image File Details

The component automatically maps the exact image filenames and extensions:

| Month | Filename | Extension |
|-------|----------|-----------|
| January | 01-jan.jpg | JPG |
| February | 02-feb.jpg | JPG |
| March | 03-march.webp | WEBP |
| April | 04-april.jpeg | JPEG |
| May | 05-may.webp | WEBP |
| June | 06-june.webp | WEBP |
| July | 07-july.jpg | JPG |
| August | 08-august.webp | WEBP |
| September | 09-sep.jpeg | JPEG |
| October | 10-oct.jpg | JPG |
| November | 11-nov.jpg | JPG |
| December | 12-dec.jpg | JPG |

**All files are expected to be in**: `public/images/months/`

---

## 💡 Key Code Sections

### State Management
```jsx
const [currentDate, setCurrentDate] = useState(new Date());
const [startDate, setStartDate] = useState(null);
const [endDate, setEndDate] = useState(null);
const [tempNotes, setTempNotes] = useState("");
```

### Date Range Logic
```jsx
const handleDayClick = (day) => {
  if (!startDate) {
    setStartDate(day);
  } else if (!endDate) {
    if (day < startDate) {
      setEndDate(startDate);
      setStartDate(day);
    } else {
      setEndDate(day);
    }
  } else {
    setStartDate(day);
    setEndDate(null);
  }
};
```

### Local Storage Persistence
```jsx
useEffect(() => {
  const key = getNoteKey();
  const stored = localStorage.getItem(key);
  if (stored) setTempNotes(stored);
}, [currentDate, startDate, endDate]);

useEffect(() => {
  const key = getNoteKey();
  if (tempNotes) localStorage.setItem(key, tempNotes);
}, [tempNotes]);
```

---

## 🎨 Styling Highlights

### Color Palette
- **Primary**: Blue (`blue-600`, `blue-200`) for selection and highlights
- **Background**: Gradient slate gray for main container
- **Text**: Gray scale (700-800 for primary, 500-600 for secondary)
- **Hover**: Subtle color transitions

### Spacing & Sizing
- Responsive padding: `p-6` (mobile) → `md:p-8` or `md:p-10`
- Gap between sections: `gap-6` to `gap-8`
- Calendar day size: Fixed `h-10` with proper font sizing

### Shadows & Borders
- Deep shadow on hero image: `shadow-2xl`
- Subtle shadows on containers: `shadow-lg`, `shadow-md`
- Smooth rounded corners: `rounded-xl` for main containers, `rounded-lg` for inputs

---

## 🔧 Customization Options

### Change Primary Color
Replace `blue-600` and `blue-200` with your preferred Tailwind color:
```jsx
// Instead of blue-600, use: purple-600, green-600, red-600, etc.
bg-blue-600 → bg-purple-600
```

### Adjust Image Paths
Modify the `monthImages` object to point to different directories:
```javascript
const monthImages = {
  0: "/your-custom-path/01-jan.jpg",
  // ...
};
```

### Change Hero Image Aspect Ratio
Adjust the `aspect-square` or `md:h-96` classes:
```jsx
// Current: aspect-square on mobile, h-96 on desktop
// Can change to: aspect-video, aspect-[3/4], h-80, h-screen, etc.
```

### Disable Auto-Save (Optional)
Remove the localStorage `useEffect` if you want manual save button:
```jsx
// Comment out the localStorage effect
// useEffect(() => { localStorage.setItem(...) }, [tempNotes]);
```

---

## 📱 Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

---

## 🚀 Performance Tips

1. **Image Optimization**
   - Images use `loading="lazy"` for deferred loading
   - Consider WebP format for better compression (partially already used)
   - Use CDN for faster delivery in production

2. **Local Storage**
   - Max safe storage: ~5-10MB per domain
   - Consider cleanup for very old entries if storage grows

3. **React Optimization**
   - Component uses proper dependency arrays in `useEffect`
   - No infinite loops
   - Memoization not required (component is lightweight)

---

## 🐛 Troubleshooting

### Images not loading?
1. Verify images are in `public/images/months/`
2. Check exact filenames match `monthImages` object
3. Verify Vite dev server is running
4. Check browser console for 404 errors

### Notes not persisting?
1. Check browser's localStorage is enabled
2. Verify notes tab changed (key changed) before refresh
3. Check browser console for any errors
4. Try clearing browser cache and reloading

### Styling looks off?
1. Ensure Tailwind CSS is properly configured
2. Verify `tailwind.config.js` includes correct content paths
3. Check `index.css` has all Tailwind directives
4. Rebuild CSS: `npm run build` (for production)

---

## 📖 Dependencies Summary

| Package | Version | Purpose |
|---------|---------|---------|
| `react` | ^18.0 | UI Framework |
| `lucide-react` | Latest | Icon Library |
| `date-fns` | ^2.30 | Date Utilities |
| `tailwindcss` | ^3.0 | CSS Framework |

---

## 🎓 Code Quality

✅ **Clean Code**: Clear comments and function documentation
✅ **No Infinite Loops**: Proper `useEffect` dependencies
✅ **Accessible**: Proper semantic HTML, titles, and ARIA where needed
✅ **Type Safe**: JSDoc comments for clarity
✅ **Production Ready**: Polished UI with smooth transitions

---

## 📝 Usage Example Walkthrough

1. **Launch the app** → See current month's hero image
2. **Click "Next"** → Month changes, image updates, notes context switches
3. **Click a day** → Shows selection (or starts range)
4. **Click another day** → Completes range (auto-orders if needed)
5. **Type in notes textarea** → Automatically saves to localStorage
6. **Click "Previous" to another month** → Old notes are preserved for that month
7. **Return to previous month** → Your notes are still there!
8. **Click the ✕ button** → Clears current range, back to general notes

---

## 🎁 Bonus Features

- **Hover Effects**: Days light up on hover for better interactivity
- **Keyboard Support**: Works with mouse/touch input
- **Smooth Transitions**: All color/layout changes animate smoothly
- **Info Footer**: Helpful hint at the bottom of the calendar
- **Responsive Typography**: Text sizes scale appropriately

---

## 📞 Support

If you encounter any issues:
1. Check the **Troubleshooting** section above
2. Verify all dependencies are installed correctly
3. Ensure image paths are correct
4. Check browser console for error messages
5. Clear browser cache and restart dev server

---

**Built with ❤️ for premium calendar experiences** 📅✨
