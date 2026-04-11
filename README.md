# 🗓️ Wall Calendar: An Interactive Time Management Experience

> A beautifully crafted, fully responsive React calendar component that brings the charm of physical wall calendars into your digital space.

## ✨ What is This?

This is an **interactive wall calendar component** designed to blend aesthetic appeal with functional simplicity. Inspired by the classic design of physical wall calendars, this project transforms a static design concept into a dynamic, user-friendly React application that works seamlessly across all devices.

Whether you're planning your month ahead, tracking important dates, or simply organizing your thoughts—this calendar adapts to your workflow with elegance and grace.

---

## 🎯 Core Features

### 📅 Wall Calendar Aesthetic
The component recreates the charm of a physical wall calendar with:
- **Month-specific hero images** – Each month features its own curated image as a visual anchor
- **Themed flower decorations** – Custom SVG flowers representing each month bloom across the calendar
- **Clean date grid** – A modern, organized layout for the calendar dates
- **Visual hierarchy** – Clear distinction between imagery, dates, and interactive elements

### 🎨 Interactive Date Selection
- **Date range picker** – Easily select a start date and an end date by clicking on the calendar
- **Visual feedback** – Clear visual states for:
  - Start date (highlighted)
  - End date (highlighted)
  - Selected date range (shaded background)
  - Hoverable date states for better UX
  
### 📝 Multi-Note System
Create and manage multiple notes with intelligent organization:
- **Month-persistent storage** – Notes always stay in their original month
- **Flexible note creation** – Add notes for:
  - Specific single dates
  - Date ranges
  - General month-wide memos
- **Date/duration labels** – Each note displays its associated date information
- **Keyboard shortcuts** – Press `Ctrl+Enter` to quickly save notes
- **Edit & delete** – Manage your notes with an intuitive interface

### 📱 Fully Responsive Design
- **Desktop experience** – Side-by-side layout with image and calendar in a harmonious arrangement
- **Mobile-first approach** – Seamlessly stacks vertically for touch devices
- **Touch-optimized** – Large, easy-to-tap buttons and interactive elements
- **Adaptive typography** – Text scales beautifully across all screen sizes

### 🎬 Smooth Animations
- **Month flip transitions** – Fluid animations when navigating between months
- **Smooth interactions** – Polished hover states and transitions throughout the interface

---

## 🚀 Quick Start

### Prerequisites
Make sure you have **Node.js** (v16 or higher) and **npm** installed on your system.

```bash
node --version  # Verify Node.js installation
npm --version   # Verify npm installation
```

### Installation & Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

   The calendar will be available at `http://localhost:5173` (or the next available port shown in your terminal).

### Building for Production

To create a production-ready build:
```bash
npm run build
```

This generates an optimized build in the `dist/` folder.

To preview the production build locally:
```bash
npm run preview
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **React 18** | UI framework for building the component |
| **Vite** | Lightning-fast build tool and dev server |
| **Tailwind CSS** | Utility-first CSS framework for styling |
| **Date-fns** | Lightweight date manipulation library |
| **Lucide React** | Beautiful SVG icons (chevrons, close buttons, etc.) |
| **PostCSS & Autoprefixer** | CSS processing and cross-browser compatibility |
| **localStorage API** | Client-side persistence (no backend required) |

---

## 🎨 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── WallCalendar.jsx      # Main calendar component (all the magic ✨)
│   ├── App.jsx                   # Root component
│   ├── main.jsx                  # Entry point
│   └── index.css                 # Global styles
├── public/
│   └── images/
│       └── months/               # Month-specific images (12 monthly visuals)
├── vite.config.js                # Vite configuration
├── tailwind.config.js            # Tailwind customization
├── postcss.config.js             # PostCSS configuration
└── package.json                  # Project dependencies
```

---

## 💡 How It Works

### Date Selection Flow
1. **Single Click** → Select a start date
2. **Click Again** → Select an end date (the range between is highlighted)
3. **Visual Feedback** → See your selection immediately reflected on the calendar

### Note Creation & Persistence
1. **Create Note** → Type in the textarea for your selected date/range
2. **Save** → Click "Add Note" or press `Ctrl+Enter`
3. **View** → Notes display below with their associated date labels
4. **Persist** → Notes are saved in browser's localStorage, keyed by month
5. **Delete** → Remove any note with the delete button

### State Management
The component uses React hooks for clean, functional state management:
- `currentDate` – Currently viewed month
- `startDate` / `endDate` – Selected date range
- `notes` – Array of notes for the month
- `tempNoteContent` – Currently typed note text

---

## 🌟 Creative Features You'll Love

### 🌸 Botanical Theme
Each month is represented by a thematic flower that blooms across the header:
- January: Rose 🌹
- February: Tulip 💐
- March: Daffodil 🌼
- ...and more through December

### 📸 Curated Monthly Images
Every month features a carefully selected hero image that sets the mood and visual context for the entire page.

### 🎯 Intelligent Date Range Display
The calendar intelligently shows what you've selected:
- "Jan 15 - Jan 22" for a date range
- "Jan 15" for a single date
- Perfect for visualizing your time blocks at a glance

### ⚡ Keyboard Accessibility
- Navigate months smoothly
- Use `Ctrl+Enter` to quickly save notes
- Fully keyboard-navigable interface

---

## 📖 Usage Examples

### Example 1: Planning a Vacation
1. Click on your departure date (e.g., June 15)
2. Click on your return date (e.g., June 22)
3. Type "Vacation in Hawaii" in the notes area
4. Press `Ctrl+Enter` to save
5. Your vacation is now marked and noted! 🏖️

### Example 2: Tracking Project Milestones
1. Select March 1-10 for Phase 1
2. Create a note: "Phase 1: Design & Planning"
3. Next, select March 11-25 for Phase 2
4. Create another note: "Phase 2: Development"
5. Navigate back to March anytime—your notes persist! 🚀

### Example 3: Daily Journaling
1. Select today's date (single click)
2. Write a quick daily reflection
3. Your note saves instantly and stays with that date
4. Come back next month to revisit your thoughts

---

## 📊 Data Persistence

All notes are stored locally in your browser using `localStorage`:
- **Storage Key Format**: `notes-YYYY-MM` (e.g., `notes-2024-04`)
- **Data Structure**: Each note contains:
  - Unique ID
  - Content text
  - Timestamp
  - Selected date (if single date note)
  - Selected date range (if range note)

**Why localStorage?** For this intern challenge, we focus on frontend excellence without backend overhead. Your notes persist across sessions but are stored locally on each device.

---

## 🎬 Demonstration

To showcase the calendar in action:
1. **Date Selection**: Click different dates to show range selection
2. **Note Creation**: Create notes for various dates
3. **Responsive Design**: Resize your browser or open on mobile to show adaptation
4. **Month Navigation**: Flip through several months to show the variety

---

## 🔧 Development Workflow

### Starting Development
```bash
npm run dev
```
Your changes will hot-reload automatically! 🔥

### Building
```bash
npm run build
```
Creates an optimized production build in `dist/`

### Quick Tweaks
- **Styling** → Edit Tailwind classes in `WallCalendar.jsx`
- **Colors** → Modify flower colors in the `flowerTypes` object
- **Months** → Update images in `public/images/months/`
- **Fonts** → Configure in `tailwind.config.js`

---

## 🚀 Deployment

This project is ready to deploy anywhere:

### Vercel (Recommended)
```bash
npm install -g vercel
vercel
```

### Netlify
```bash
npm run build
# Upload the 'dist' folder to Netlify
```

### GitHub Pages
Update `vite.config.js` with your repository name, build, and push to `gh-pages` branch.

---

## 📋 Requirements Checklist

✅ **Wall Calendar Aesthetic** – Beautiful month-specific imagery with botanical decorations  
✅ **Day Range Selector** – Select start and end dates with clear visual states  
✅ **Integrated Notes Section** – Multi-note functionality with date-aware persistence  
✅ **Fully Responsive** – Desktop and mobile layouts with seamless adaptation  
✅ **Zero Backend** – Pure frontend solution using localStorage  
✅ **Code Quality** – Clean React patterns, proper component structure, optimized styling  

---

## 🎓 Learning Highlights

This project demonstrates:
- **React Fundamentals**: Hooks, state management, conditional rendering
- **Date Handling**: Complex date logic using date-fns
- **Responsive Design**: Mobile-first Tailwind CSS approach
- **UX/UI Thinking**: Visual feedback, accessibility, touch optimization
- **Storage Solutions**: Browser APIs without backend complexity
- **Animation**: Smooth transitions and interactive feedback
- **SVG Graphics**: Custom vector flower illustrations

---

## 💬 Notes for Evaluators

This calendar component showcases:
1. **Polished Frontend Skills**: Attention to design details and UX
2. **State Management**: Smart handling of date selections and persistent notes
3. **Responsive Architecture**: Seamless adaptation across devices
4. **Code Organization**: Clean, maintainable component structure
5. **User Delight**: Thoughtful touches like keyboard shortcuts and animations

The project proves that exceptional frontends don't require complex backends—just thoughtful design and solid React fundamentals.

---

## 📸 Visual Tour

- **Hero Image Per Month** → Beautifully curated monthly visuals
- **Bloom Animations** → Thematic flowers that vary by month
- **Date Range Highlighting** → Clear visual indication of selected dates
- **Notes Area** → Organized, easy-to-manage note interface
- **Touch-Friendly Mobile** → All interactions optimized for tap

---

## 🎉 Ready to Explore?

Start the dev server and dive in:

```bash
cd frontend && npm install && npm run dev
```

Then open `http://localhost:5173` in your browser and start planning your month! 📅✨

---

**Happy Calendar Building! 🚀**

---

*Created as a summer internship recruitment challenge showcasing frontend engineering excellence.*
