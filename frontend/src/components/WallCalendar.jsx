import React, { useState, useEffect } from "react";
import { ChevronLeft, ChevronRight, X } from "lucide-react";
import {
  format,
  startOfMonth,
  endOfMonth,
  eachDayOfInterval,
  isSameMonth,
  isSameDay,
  addMonths,
  subMonths,
  isWithinInterval,
} from "date-fns";

export default function WallCalendar() {
  // ========================
  // MONTH-TO-IMAGE MAPPING
  // ========================
  // Maps month index (0-11) to actual image paths with correct extensions
  const monthImages = {
    0: "/images/months/01-jan.jpg",
    1: "/images/months/02-feb.jpg",
    2: "/images/months/03-march.webp",
    3: "/images/months/04-april.jpeg",
    4: "/images/months/05-may.webp",
    5: "/images/months/06-june.webp",
    6: "/images/months/07-july.jpg",
    7: "/images/months/08-august.webp",
    8: "/images/months/09-sep.jpeg",
    9: "/images/months/10-oct.jpg",
    10: "/images/months/11-nov.jpg",
    11: "/images/months/12-dec.jpg",
  };

  // Per-month bloom Y positions (matches the flower SVG coordinates above)
  const bloomYPositions = [45, 20, 40, 30, 40, 40, 40, 20, 45, 30, 40, 30];

  const monthNames = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  // ========================
  // FLOWER TYPES & COLORS BY MONTH
  // ========================
  const flowerTypes = {
    0: { name: "Rose", color: "#FF6B6B", stem: "#2D5B2D" }, // January - Red Rose
    1: { name: "Tulip", color: "#FFB6C1", stem: "#2D5B2D" }, // February - Pink Tulip
    2: { name: "Daffodil", color: "#FFD700", stem: "#2D5B2D" }, // March - Yellow Daffodil
    3: { name: "Hyacinth", color: "#FF1493", stem: "#2D5B2D" }, // April - Deep Pink Hyacinth
    4: { name: "Peony", color: "#FF69B4", stem: "#2D5B2D" }, // May - Hot Pink Peony
    5: { name: "Poppy", color: "#FF4500", stem: "#2D5B2D" }, // June - Orange Red Poppy
    6: { name: "Sunflower", color: "#FFD700", stem: "#2D5B2D" }, // July - Gold Sunflower
    7: { name: "Lily", color: "#FFD700", stem: "#2D5B2D" }, // August - Gold Lily
    8: { name: "Marigold", color: "#FF8C00", stem: "#2D5B2D" }, // September - Dark Orange Marigold
    9: { name: "Chrysanthemum", color: "#FF4500", stem: "#2D5B2D" }, // October - Orange Red Chrysanthemum
    10: { name: "Dahlia", color: "#8B4513", stem: "#2D5B2D" }, // November - Brown Dahlia
    11: { name: "Poinsettia", color: "#DC143C", stem: "#2D5B2D" }, // December - Crimson Poinsettia
  };

  // ========================
  // STATE MANAGEMENT
  // ========================
  const [currentDate, setCurrentDate] = useState(new Date());
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [notes, setNotes] = useState([]);
  const [tempNoteContent, setTempNoteContent] = useState("");
  const [flipDirection, setFlipDirection] = useState(null);

  // ========================
  // UTILITIES
  // ========================

  /**
   * Generates a unique key for storing notes based on month/year
   * Notes always persist in their original month
   */
  const getNoteKey = () => {
    return `notes-${format(currentDate, "yyyy-MM")}`;
  };

  /**
   * Get date/duration text for a note
   */
  const getNoteDateLabel = (note) => {
    if (note.selectedStartDate && note.selectedEndDate) {
      return `${format(new Date(note.selectedStartDate), "MMM d")} - ${format(new Date(note.selectedEndDate), "MMM d")}`;
    }
    if (note.selectedDate) {
      return format(new Date(note.selectedDate), "MMM d, yyyy");
    }
    return "Month Note";
  };

  /**
   * Handles calendar day clicks for date range selection
   */
  const handleDayClick = (day) => {
    if (!startDate) {
      // First click: set start date
      setStartDate(day);
      setEndDate(null);
    } else if (!endDate) {
      // Second click: set end date (auto-order if needed)
      if (day < startDate) {
        setEndDate(startDate);
        setStartDate(day);
      } else {
        setEndDate(day);
      }
    } else {
      // Range already selected: reset and start new selection
      setStartDate(day);
      setEndDate(null);
    }
  };

  /**
   * Clear the selected date range
   */
  const handleClearRange = () => {
    setStartDate(null);
    setEndDate(null);
  };

  /**
   * Navigate to the previous month
   */
  /**
   * Navigate to the previous month
   */
  const handlePrevMonth = () => {
    if (flipDirection) return; // Prevent double clicking
    setFlipDirection("prev");
    setTimeout(() => {
      setCurrentDate(subMonths(currentDate, 1));
      setStartDate(null);
      setEndDate(null);
    }, 400); // perfectly hits the 50% mark of 0.8s animation
    setTimeout(() => {
      setFlipDirection(null);
    }, 800);
  };

  /**
   * Navigate to the next month
   */
  const handleNextMonth = () => {
    if (flipDirection) return; // Prevent double clicking
    setFlipDirection("next");
    setTimeout(() => {
      setCurrentDate(addMonths(currentDate, 1));
      setStartDate(null);
      setEndDate(null);
    }, 400);
    setTimeout(() => {
      setFlipDirection(null);
    }, 800);
  };

  /**
   * Add a new note
   */
  const handleAddNote = () => {
    if (!tempNoteContent.trim()) return;
    
    const newNote = {
      id: Date.now(),
      content: tempNoteContent,
      timestamp: new Date().toISOString(),
      selectedDate: startDate ? startDate.toISOString() : null,
      selectedStartDate: startDate && endDate ? startDate.toISOString() : null,
      selectedEndDate: startDate && endDate ? endDate.toISOString() : null,
    };
    
    const updatedNotes = [...notes, newNote];
    setNotes(updatedNotes);
    
    // Save to localStorage - always by month
    const key = getNoteKey();
    localStorage.setItem(key, JSON.stringify(updatedNotes));
    
    // Reset input but keep the date selection
    setTempNoteContent("");
  };

  /**
   * Delete a note by ID
   */
  const handleDeleteNote = (noteId) => {
    const updatedNotes = notes.filter(note => note.id !== noteId);
    setNotes(updatedNotes);
    
    // Save to localStorage
    const key = getNoteKey();
    if (updatedNotes.length > 0) {
      localStorage.setItem(key, JSON.stringify(updatedNotes));
    } else {
      localStorage.removeItem(key);
    }
  };

  // ========================
  // LOCAL STORAGE PERSISTENCE
  // ========================
  // Load notes from localStorage when the component mounts or the note key changes
  // ========================
  // LOCAL STORAGE PERSISTENCE & PRELOADING
  // ========================
  // Load notes from localStorage when the component mounts or the note key changes
  useEffect(() => {
    const key = getNoteKey();
    const stored = localStorage.getItem(key);
    if (stored) {
      try {
        setNotes(JSON.parse(stored));
      } catch {
        // Fallback for old string format
        setNotes([{ id: Date.now(), classification: "note", content: stored }]);
      }
    } else {
      setNotes([]);
    }
    setTempNoteContent("");
  }, [currentDate, startDate, endDate]);

  // Preload all month images to prevent pausing during transitions
  useEffect(() => {
    const imagesToPreload = [
      "/images/months/01-jan.jpg",
      "/images/months/02-feb.jpg",
      "/images/months/03-march.webp",
      "/images/months/04-april.jpeg",
      "/images/months/05-may.webp",
      "/images/months/06-june.webp",
      "/images/months/07-july.jpg",
      "/images/months/08-august.webp",
      "/images/months/09-sep.jpeg",
      "/images/months/10-oct.jpg",
      "/images/months/11-nov.jpg",
      "/images/months/12-dec.jpg",
    ];
    imagesToPreload.forEach((src) => {
      const img = new Image();
      img.src = src;
    });
  }, []);

  const handleNotesChange = (e) => {
    setTempNoteContent(e.target.value);
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && e.ctrlKey) {
      handleAddNote();
    }
  };

  /**
   * Get current selection label for the input header
   */
  const getCurrentSelectionLabel = () => {
    if (startDate && endDate) {
      return `${format(startDate, "MMM d")} - ${format(endDate, "MMM d")}`;
    }
    if (startDate) {
      return format(startDate, "MMM d, yyyy");
    }
    return monthNames[currentDate.getMonth()];
  };

  // ========================
  // CALENDAR GENERATION
  // ========================
  const monthStart = startOfMonth(currentDate);
  const monthEnd = endOfMonth(currentDate);

  // Get all days in the month (including days from previous/next month for full grid)
  const calendarDays = eachDayOfInterval({
    start: new Date(monthStart.getFullYear(), monthStart.getMonth(), 1),
    end: new Date(monthEnd.getFullYear(), monthEnd.getMonth() + 1, 0),
  });

  // Get only the days that belong to the current month
  const monthDays = calendarDays.filter((day) => isSameMonth(day, currentDate));

  // ========================
  // DETERMINE DAY STYLING CLASSES
  // ========================
  const getDayClasses = (day) => {
    const baseClasses =
      "h-7 w-7 sm:h-8 sm:w-8 lg:h-10 lg:w-10 mx-auto flex items-center justify-center rounded-full font-bold text-xs sm:text-sm lg:text-base cursor-pointer transition-all duration-200 hover:shadow";

    // Day not in current month
    if (!isSameMonth(day, currentDate)) {
      return `${baseClasses} text-gray-300 bg-transparent`;
    }

    // Start date
    if (startDate && isSameDay(day, startDate)) {
      return `${baseClasses} bg-blue-600 text-white shadow-md`;
    }

    // End date
    if (endDate && isSameDay(day, endDate)) {
      return `${baseClasses} bg-blue-600 text-white shadow-md`;
    }

    // Within range (between start and end)
    if (startDate && endDate && isWithinInterval(day, {
          start: startDate,
          end: endDate,
        })) {
      return `${baseClasses} bg-blue-100 text-blue-900`;
    }

    // Sunday - red text
    const isSunday = day.getDay() === 0;
    if (isSunday) {
      return `${baseClasses} bg-transparent hover:bg-gray-100 text-red-600`;
    }

    // Regular day in month
    return `${baseClasses} bg-transparent hover:bg-gray-100 text-gray-700`;
  };

  // ========================
  // Compute current bloom Y for label placement
  const currentBloomY = bloomYPositions[currentDate.getMonth()];

  // ========================
  // WEEK GRID GENERATION
  // ========================
  // Create weeks grid to properly display calendar
  const weekDays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  const firstDayOfWeek = monthStart.getDay();

  // Pad with previous month's days
  const paddedDays = [
    ...Array(firstDayOfWeek).fill(null),
    ...monthDays,
  ];

  // Pad with next month's days to complete the last week
  // Ensure EXACTLY 6 weeks (42 days) so the calendar height NEVER changes between months
  const fullyPaddedDays = [
    ...paddedDays,
    ...Array(Math.max(0, 42 - paddedDays.length)).fill(null)
  ];
  
  const weeks = [];
  for (let i = 0; i < fullyPaddedDays.length; i += 7) {
    weeks.push(fullyPaddedDays.slice(i, i + 7));
  }

  return (
    <div className="fixed inset-0 bg-[#DCD8CB] overflow-hidden flex items-center justify-center p-0 xl:p-8">
      {/* Wall Texture Background */}
      <style>{`
        .wall-bg {
          background-color: #E2DFD3;
          background-image: 
            radial-gradient(circle at 15% 10%, rgba(255,255,255,0.65) 0%, rgba(255,255,255,0) 50%),
            radial-gradient(circle at 85% 90%, rgba(0,0,0,0.12) 0%, rgba(0,0,0,0) 60%),
            url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='grain'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23grain)' opacity='0.16'/%3E%3C/svg%3E"),
            url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='plaster'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.015' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23plaster)' opacity='0.25'/%3E%3C/svg%3E");
          box-shadow: inset 0 0 150px rgba(20,15,10,0.15), inset 0 0 40px rgba(20,15,10,0.08);
        }
        @keyframes slideIn {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes pageTurnNext {
          0% { transform: rotateX(0deg); opacity: 1; filter: brightness(1); }
          40% { opacity: 1; filter: brightness(0.9); }
          49.99% { transform: rotateX(90deg); opacity: 0; filter: brightness(0.8); }
          50% { transform: rotateX(-90deg); opacity: 0; filter: brightness(0.8); }
          60% { opacity: 1; filter: brightness(0.9); }
          100% { transform: rotateX(0deg); opacity: 1; filter: brightness(1); }
        }
        @keyframes pageTurnPrev {
          0% { transform: rotateX(0deg); opacity: 1; filter: brightness(1); }
          40% { opacity: 1; filter: brightness(0.9); }
          49.99% { transform: rotateX(-90deg); opacity: 0; filter: brightness(0.8); }
          50% { transform: rotateX(90deg); opacity: 0; filter: brightness(0.8); }
          60% { opacity: 1; filter: brightness(0.9); }
          100% { transform: rotateX(0deg); opacity: 1; filter: brightness(1); }
        }
        .paper-flip-next {
          animation: pageTurnNext 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards;
          transform-origin: center 20px;
          transform-style: preserve-3d;
          backface-visibility: hidden;
        }
        .paper-flip-prev {
          animation: pageTurnPrev 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards;
          transform-origin: center 20px;
          transform-style: preserve-3d;
          backface-visibility: hidden;
        }
        .calendar-card {
          animation: slideIn 0.5s ease-out;
        }
      `}</style>
      <div className="absolute inset-0 wall-bg mix-blend-multiply opacity-90"></div>
      <div className="absolute inset-0 wall-bg opacity-30"></div>

      {/* Main Container - Desktop and Mobile Layout */}
      <div className="relative z-10 w-full h-[100dvh] xl:h-auto flex flex-row gap-6 xl:gap-8 items-center justify-start xl:justify-center max-w-[1250px] mx-auto overflow-x-auto xl:overflow-visible snap-x snap-mandatory px-[5vw] xl:px-0 [&::-webkit-scrollbar]:hidden" style={{ scrollbarWidth: 'none' }}>
        
        {/* CALENDAR - Main Card (Left on Desktop, Top on Mobile) */}
        <div className={`calendar-card bg-white rounded-xl overflow-hidden border border-gray-200/60 w-[90vw] xl:w-full max-w-[850px] h-[92dvh] max-h-[750px] xl:h-auto xl:max-h-none flex flex-col relative shrink-0 snap-center`}
             style={{
               perspective: '1500px',
               boxShadow: '0 45px 85px -20px rgba(30,20,15,0.35), 0 25px 35px -10px rgba(30,20,15,0.2), 0 10px 15px -5px rgba(30,20,15,0.1), inset 0 1px 0 rgba(255,255,255,0.8)'
             }}>
          
          {/* Wall Calendar Spiral Bindings - Minimalist */}
          <div className="absolute top-2 left-0 right-0 h-6 flex justify-around px-8 z-30 pointer-events-none">
            {[...Array(20)].map((_, i) => (
              <div key={i} className="relative flex flex-col items-center">
                <div className="w-1.5 h-6 -mt-1 bg-gradient-to-b from-gray-200 to-gray-300 rounded-sm shadow-sm border border-gray-300/50"></div>
                <div className="absolute top-4 left-1/2 transform -translate-x-1/2 w-3 h-3 bg-gray-800 rounded-full shadow-inner opacity-60 mix-blend-multiply"></div>
              </div>
            ))}
          </div>
          
          {/* Add a top padding so absolutely no content rendering begins inside the bindings area! */}
          <div className={`flex flex-col lg:flex-row w-full pt-7 lg:pt-10 flex-1 min-h-0 h-full bg-white relative z-10 rounded-xl overflow-hidden ${flipDirection === 'next' ? 'paper-flip-next' : flipDirection === 'prev' ? 'paper-flip-prev' : ''}`}>
            {/* LEFT: Hero Image */}
            <div className="w-full lg:w-[320px] h-[22%] min-h-[100px] lg:h-[420px] relative overflow-hidden bg-gray-100 shrink-0 border-b lg:border-b-0 lg:border-r border-gray-200">
              <img
                src={monthImages[currentDate.getMonth()]}
                alt={`${monthNames[currentDate.getMonth()]} Calendar`}
                className="absolute inset-0 w-full h-full object-cover object-center"
                style={{ imageRendering: '-webkit-optimize-contrast' }}
                loading="eager"
              />
            </div>
            
            {/* RIGHT: Calendar Platform */}
            <div className="flex-1 flex flex-col shrink-0 min-h-0 lg:h-[420px]">

              {/* Header & Navigate Merged */}
              <div className="px-4 py-2 lg:px-6 lg:py-4 bg-white border-b border-gray-50 flex items-center justify-between shrink-0">
                <button onClick={handlePrevMonth} className="flex items-center justify-center h-8 w-8 lg:h-9 lg:w-9 rounded-full text-gray-400 hover:bg-gray-100 hover:text-gray-800 active:scale-95 transition-all">
                  <ChevronLeft size={20} />
                </button>
                <div className="text-center flex-1">
                  <h1 className="text-xl lg:text-2xl font-black text-gray-800 tracking-tight">{monthNames[currentDate.getMonth()]}</h1>
                  <p className="text-[10px] lg:text-[11px] font-bold text-gray-400 tracking-widest uppercase lg:mt-0.5">{currentDate.getFullYear()}</p>
                </div>
                <button onClick={handleNextMonth} className="flex items-center justify-center h-8 w-8 lg:h-9 lg:w-9 rounded-full text-gray-400 hover:bg-gray-100 hover:text-gray-800 active:scale-95 transition-all">
                  <ChevronRight size={20} />
                </button>
              </div>
              
              {/* Bottom Split: Grid and Notes */}
              <div className="flex flex-col lg:flex-row flex-1 min-h-0 bg-white">

                {/* CALENDAR GRID */}
                <div className="w-full lg:w-[55%] px-3 py-2 sm:px-4 sm:py-3 lg:px-4 lg:py-4 shrink-0 flex flex-col justify-center border-b lg:border-b-0 lg:border-r border-gray-100 min-h-0">
            {/* Weekday Headers */}
            <div className="grid grid-cols-7 gap-1 lg:gap-2 mb-1 lg:mb-3 shrink-0">
              {weekDays.map((day) => (
                <div
                  key={day}
                  className="text-center font-bold text-[9px] lg:text-[10px] text-gray-400 py-0.5 lg:py-1 uppercase tracking-widest"
                >
                  {day}
                </div>
              ))}
            </div>

            {/* Calendar Days Grid */}
            <div className="grid grid-cols-7 gap-y-0.5 gap-x-1 sm:gap-y-1 lg:gap-y-2 lg:gap-x-2 pb-0.5 lg:pb-1">
              {weeks.map((week, weekIndex) =>
                week.map((day, dayIndex) => (
                  <div
                    key={`${weekIndex}-${dayIndex}`}
                    className="flex justify-center"
                    onClick={() => day && isSameMonth(day, currentDate) && handleDayClick(day)}
                  >
                    {day && isSameMonth(day, currentDate) ? (
                      <div
                        className={getDayClasses(day)}
                        title={format(day, "EEEE, MMMM d, yyyy")}
                      >
                        {format(day, "d")}
                      </div>
                    ) : day ? (
                      <div className="h-7 w-7 sm:h-8 sm:w-8 lg:h-10 lg:w-10 mx-auto flex items-center justify-center text-xs sm:text-sm lg:text-base text-gray-300 font-semibold bg-transparent">
                        {format(day, "d")}
                      </div>
                    ) : (
                      <div className="h-7 w-7 sm:h-8 sm:w-8 lg:h-10 lg:w-10 bg-transparent"></div>
                    )}
                  </div>
                ))
              )}
            </div>

                </div>

                {/* NOTES PANEL - SIMPLIFIED */}
                <div className="w-full lg:w-[45%] flex flex-col shrink-0 flex-1 min-h-[140px] bg-white border-l border-gray-50 overflow-hidden">
                  {/* Header with current selection */}
                  <div className="px-4 py-2 shrink-0 border-b border-gray-50 flex items-center justify-between">
                    <h3 className="text-[10px] lg:text-[11px] font-bold text-gray-700">📅 {getCurrentSelectionLabel()}</h3>
                    {(startDate || endDate) && (
                      <button
                        onClick={handleClearRange}
                        className="text-[9px] text-gray-400 hover:text-gray-700 transition-colors"
                      >
                        Clear
                      </button>
                    )}
                  </div>

                  {/* Notes List */}
                  <div className="flex-1 overflow-y-auto px-4 py-2 space-y-1.5 lg:space-y-2 min-h-[50px]">
                    {notes.length === 0 ? (
                      <p className="text-[11px] lg:text-[12px] text-gray-300 italic py-2">No notes for {monthNames[currentDate.getMonth()]}.</p>
                    ) : (
                      notes.map((note) => (
                        <div key={note.id} className="p-2 lg:p-3 rounded-lg bg-gray-50 border border-gray-200">
                          <div className="flex items-start justify-between gap-2 mb-0.5 lg:mb-1">
                            <span className="text-[9px] lg:text-[10px] font-semibold text-gray-500">
                              {getNoteDateLabel(note)}
                            </span>
                            <button
                              onClick={() => handleDeleteNote(note.id)}
                              className="text-gray-300 hover:text-red-500 transition-colors flex-shrink-0"
                              title="Delete note"
                            >
                              <X size={12} />
                            </button>
                          </div>
                          <p className="text-[11px] lg:text-[12px] text-gray-700 break-words whitespace-pre-wrap">
                            {note.content}
                          </p>
                        </div>
                      ))
                    )}
                  </div>

                  {/* Add Note Section - Textarea */}
                  <div className="px-4 py-2 border-t border-gray-50 shrink-0 bg-transparent">
                    <textarea
                      value={tempNoteContent}
                      onChange={handleNotesChange}
                      onKeyPress={handleKeyPress}
                      placeholder="Add a Note..."
                      className="w-full px-2 py-1.5 lg:py-2 text-[11px] lg:text-[12px] border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none h-10 lg:h-16"
                    />
                    <button
                      onClick={handleAddNote}
                      disabled={!tempNoteContent.trim()}
                      className="mt-1.5 lg:mt-2 w-full px-2 py-1.5 lg:py-2 bg-blue-500 text-white text-[11px] lg:text-[12px] font-semibold rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                    >
                      Add Note
                    </button>
                  </div>
                </div>

              </div>
            </div>
          </div>
        </div>

        {/* ======================== */}
        {/* SIDEBAR - Table/Vase */}
        {/* ======================== */}
        <div className="w-[90vw] xl:w-[340px] flex flex-col shrink-0 xl:shrink min-h-0 max-h-full snap-center pt-8 xl:pt-0">

          {/* Simple Wooden Table with Vase */}
          <div className="calendar-card bg-gradient-to-b from-amber-50 to-orange-50 rounded-xl overflow-hidden border border-amber-200/60 p-4 lg:p-6 pb-2 lg:pb-2 flex flex-col items-center justify-end shrink-0 h-48 lg:h-[460px] min-h-[200px]"
               style={{ 
                 perspective: '1200px',
                 boxShadow: '0 45px 85px -20px rgba(30,20,15,0.35), 0 25px 35px -10px rgba(30,20,15,0.2), 0 10px 15px -5px rgba(30,20,15,0.1), inset 0 1px 0 rgba(255,255,255,0.8)'
               }}>
            
            {/* Background */}
            <div className="absolute inset-0 bg-gradient-to-b from-amber-50 via-white to-orange-100 opacity-80"></div>
            
            {/* Simple Table & Vase SVG */}
            <div className="relative w-full h-full flex flex-col items-center justify-end">
              <svg width="100%" height="100%" viewBox="0 -105 360 350" preserveAspectRatio="xMidYMax meet" className="drop-shadow-xl relative z-10 overflow-visible">
                <defs>
                  <linearGradient id="luxuryWood" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style={{ stopColor: '#2A0800', stopOpacity: 1 }} />
                    <stop offset="100%" style={{ stopColor: '#120400', stopOpacity: 1 }} />
                  </linearGradient>
                  <linearGradient id="goldTrim" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style={{ stopColor: '#FFF3B0', stopOpacity: 1 }} />
                    <stop offset="30%" style={{ stopColor: '#D4AF37', stopOpacity: 1 }} />
                    <stop offset="70%" style={{ stopColor: '#AA7C11', stopOpacity: 1 }} />
                    <stop offset="100%" style={{ stopColor: '#FDF1A9', stopOpacity: 1 }} />
                  </linearGradient>
                  <linearGradient id="marbleTop" x1="0%" y1="0%" x2="100%" y2="10%">
                    <stop offset="0%" style={{ stopColor: '#F5F5F0', stopOpacity: 1 }} />
                    <stop offset="40%" style={{ stopColor: '#FFFFFF', stopOpacity: 1 }} />
                    <stop offset="45%" style={{ stopColor: '#E8E8E0', stopOpacity: 1 }} />
                    <stop offset="50%" style={{ stopColor: '#FFFFFF', stopOpacity: 1 }} />
                    <stop offset="85%" style={{ stopColor: '#F0F0EB', stopOpacity: 1 }} />
                    <stop offset="100%" style={{ stopColor: '#FFFFFF', stopOpacity: 1 }} />
                  </linearGradient>
                  <linearGradient id="marbleFront" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style={{ stopColor: '#E0E0D8', stopOpacity: 1 }} />
                    <stop offset="100%" style={{ stopColor: '#B8B8AC', stopOpacity: 1 }} />
                  </linearGradient>
                  <linearGradient id="vaseGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" style={{ stopColor: '#FFFFFF', stopOpacity: 1 }} />
                    <stop offset="50%" style={{ stopColor: '#F5F5F5', stopOpacity: 1 }} />
                    <stop offset="100%" style={{ stopColor: '#D5D5D5', stopOpacity: 1 }} />
                  </linearGradient>
                  <linearGradient id="waterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style={{ stopColor: 'rgba(100,150,220,0.3)', stopOpacity: 1 }} />
                    <stop offset="100%" style={{ stopColor: 'rgba(50,100,180,0.4)', stopOpacity: 1 }} />
                  </linearGradient>
                  <style>{`
                    @keyframes fishSwim {
                      0% { transform: translate(0px, 0px); }
                      25% { transform: translate(15px, -8px); }
                      50% { transform: translate(20px, 0px); }
                      75% { transform: translate(15px, 8px); }
                      100% { transform: translate(0px, 0px); }
                    }
                    .fish-swimmer {
                      animation: fishSwim 4s ease-in-out infinite;
                    }
                  `}</style>
                </defs>

                {/* Shadow under table */}
                <ellipse cx="180" cy="235" rx="190" ry="10" fill="rgba(0,0,0,0.15)" />

                {/* Luxury 2.5D Console Table */}
                
                {/* Table Top Surface (Depth) */}
                <path d="M 0 140 L 360 140 L 380 160 L -20 160 Z" fill="url(#marbleTop)" />
                
                {/* Table Top Edge Thickness */}
                <rect x="-20" y="160" width="400" height="8" fill="url(#marbleFront)" />
                
                {/* Gold Trim Under Marble */}
                <rect x="-20" y="168" width="400" height="4" fill="url(#goldTrim)" />

                {/* Table Front Face / Body */}
                <rect x="10" y="172" width="340" height="48" fill="url(#luxuryWood)" />
                
                {/* Drawer Detail */}
                <rect x="40" y="182" width="120" height="28" fill="rgba(0,0,0,0.2)" stroke="url(#goldTrim)" strokeWidth="1" />
                <rect x="200" y="182" width="120" height="28" fill="rgba(0,0,0,0.2)" stroke="url(#goldTrim)" strokeWidth="1" />
                
                {/* Drawer Knobs */}
                <circle cx="100" cy="196" r="4" fill="url(#goldTrim)" />
                <circle cx="260" cy="196" r="4" fill="url(#goldTrim)" />

                {/* Front Left Leg */}
                <path d="M 20 220 L 40 220 L 35 235 L 25 235 Z" fill="url(#luxuryWood)" />
                <path d="M 25 230 L 35 230 L 35 235 L 25 235 Z" fill="url(#goldTrim)" />

                {/* Front Right Leg */}
                <path d="M 320 220 L 340 220 L 335 235 L 325 235 Z" fill="url(#luxuryWood)" />
                <path d="M 325 230 L 335 230 L 335 235 L 325 235 Z" fill="url(#goldTrim)" />

                {/* Vase Drop Shadow on Marble Surface */}
                <ellipse cx="180" cy="155" rx="30" ry="6" fill="rgba(0,0,0,0.2)" />

                {/* Vase & Flower Group */}
                <g>
                  {/* Vase body - drawn lowest so flower goes inside */}
                  <path d="M 150 85 L 145 110 L 140 138 L 158 155 L 202 155 L 220 138 L 215 110 L 210 85 Q 180 75, 150 85" 
                        fill="url(#vaseGrad)" stroke="#999999" strokeWidth="2" />
                  
                  {/* FLOWER & STEM - perfectly embedded behind water but in front of back vase wall */}
                  <g transform="translate(90, -85)">
                     {/* Stem - accurately reaches bottom of vase (y=155 in parent SVG) -> translated y=240 */}
                    <line x1="90" y1="240" x2="90" y2="100" stroke="#2D5B2D" strokeWidth="2.5" strokeLinecap="round" />
                    
                    {/* Shift bloom down entirely by 30 so the whole SVG fits tighter vertically */}
                    <g transform="translate(0, 30)">
                      <line x1="90" y1="125" x2="55" y2="90" stroke="#3A6B2C" strokeWidth="2" opacity="0.9" strokeLinecap="round" />
                      <line x1="90" y1="125" x2="125" y2="90" stroke="#3A6B2C" strokeWidth="2" opacity="0.9" strokeLinecap="round" />
                      
                      {/* Leaves attached to ends of branches (branch ends are at 55,90 and 125,90) */}
                      <ellipse cx="45" cy="80" rx="8" ry="14" fill="#45A049" opacity="0.8" transform="rotate(-45 45 80)" />
                      <ellipse cx="135" cy="80" rx="8" ry="14" fill="#45A049" opacity="0.8" transform="rotate(45 135 80)" />

                      {/* Small connector at top of stem to better visually link to bloom */}
                      <circle cx="90" cy="70" r="3" fill={flowerTypes[currentDate.getMonth()].stem} />

                    {currentDate.getMonth() === 0 && (
                      <g>
                        <circle cx="90" cy="45" r="15" fill={flowerTypes[0].color} />
                        <circle cx="80" cy="30" r="12" fill={flowerTypes[0].color} opacity="0.9" />
                        <circle cx="100" cy="30" r="12" fill={flowerTypes[0].color} opacity="0.9" />
                        <circle cx="75" cy="45" r="11" fill={flowerTypes[0].color} opacity="0.85" />
                        <circle cx="105" cy="45" r="11" fill={flowerTypes[0].color} opacity="0.85" />
                        <circle cx="90" cy="65" r="10" fill={flowerTypes[0].color} opacity="0.8" />
                        <circle cx="90" cy="45" r="8" fill="#FFD700" opacity="0.7" />
                      </g>
                    )}
                    
                    {currentDate.getMonth() === 1 && (
                      <g>
                        <path d="M 90 20 Q 75 40, 80 65" stroke={flowerTypes[1].color} strokeWidth="8" fill="none" opacity="0.85" />
                        <path d="M 90 20 Q 90 45, 90 65" stroke={flowerTypes[1].color} strokeWidth="8" fill="none" />
                        <path d="M 90 20 Q 105 40, 100 65" stroke={flowerTypes[1].color} strokeWidth="8" fill="none" opacity="0.85" />
                      </g>
                    )}

                    {currentDate.getMonth() === 2 && (
                      <g>
                        <circle cx="90" cy="40" r="18" fill={flowerTypes[2].color} />
                        <circle cx="75" cy="25" r="14" fill={flowerTypes[2].color} opacity="0.9" />
                        <circle cx="105" cy="25" r="14" fill={flowerTypes[2].color} opacity="0.9" />
                        <circle cx="70" cy="45" r="13" fill={flowerTypes[2].color} opacity="0.85" />
                        <circle cx="110" cy="45" r="13" fill={flowerTypes[2].color} opacity="0.85" />
                        <ellipse cx="90" cy="40" rx="10" ry="12" fill="#FFB700" />
                      </g>
                    )}

                    {currentDate.getMonth() === 3 && (
                      <g>
                        <circle cx="85" cy="30" r="6" fill={flowerTypes[3].color} />
                        <circle cx="95" cy="30" r="6" fill={flowerTypes[3].color} />
                        <circle cx="80" cy="45" r="6" fill={flowerTypes[3].color} opacity="0.9" />
                        <circle cx="100" cy="45" r="6" fill={flowerTypes[3].color} opacity="0.9" />
                        <circle cx="88" cy="60" r="6" fill={flowerTypes[3].color} opacity="0.85" />
                        <circle cx="92" cy="60" r="6" fill={flowerTypes[3].color} opacity="0.85" />
                      </g>
                    )}

                    {currentDate.getMonth() === 4 && (
                      <g>
                        <circle cx="90" cy="40" r="16" fill={flowerTypes[4].color} />
                        <circle cx="75" cy="30" r="13" fill={flowerTypes[4].color} opacity="0.9" />
                        <circle cx="105" cy="30" r="13" fill={flowerTypes[4].color} opacity="0.9" />
                        <circle cx="78" cy="55" r="12" fill={flowerTypes[4].color} opacity="0.85" />
                        <circle cx="102" cy="55" r="12" fill={flowerTypes[4].color} opacity="0.85" />
                        <circle cx="90" cy="65" r="11" fill={flowerTypes[4].color} opacity="0.8" />
                      </g>
                    )}

                    {currentDate.getMonth() === 5 && (
                      <g>
                        <circle cx="90" cy="40" r="17" fill={flowerTypes[5].color} />
                        <circle cx="70" cy="30" r="13" fill={flowerTypes[5].color} opacity="0.8" />
                        <circle cx="110" cy="30" r="13" fill={flowerTypes[5].color} opacity="0.8" />
                        <circle cx="90" cy="40" r="10" fill="#1A1A1A" />
                        <circle cx="90" cy="40" r="6" fill="#3A3A3A" />
                      </g>
                    )}

                    {currentDate.getMonth() === 6 && (
                      <g>
                        <circle cx="90" cy="40" r="20" fill={flowerTypes[6].color} />
                        <circle cx="65" cy="20" r="12" fill={flowerTypes[6].color} opacity="0.9" />
                        <circle cx="115" cy="20" r="12" fill={flowerTypes[6].color} opacity="0.9" />
                        <circle cx="60" cy="45" r="12" fill={flowerTypes[6].color} opacity="0.85" />
                        <circle cx="120" cy="45" r="12" fill={flowerTypes[6].color} opacity="0.85" />
                        <circle cx="75" cy="65" r="11" fill={flowerTypes[6].color} opacity="0.8" />
                        <circle cx="105" cy="65" r="11" fill={flowerTypes[6].color} opacity="0.8" />
                        <circle cx="90" cy="40" r="14" fill="#8B6914" />
                        <circle cx="90" cy="40" r="10" fill="#5C4A0A" />
                      </g>
                    )}

                    {currentDate.getMonth() === 7 && (
                      <g>
                        <path d="M 90 20 Q 70 40, 65 70" stroke={flowerTypes[7].color} strokeWidth="12" fill="none" opacity="0.85" />
                        <path d="M 90 20 Q 90 50, 90 70" stroke={flowerTypes[7].color} strokeWidth="12" fill="none" />
                        <path d="M 90 20 Q 110 40, 115 70" stroke={flowerTypes[7].color} strokeWidth="12" fill="none" opacity="0.85" />
                        <circle cx="90" cy="20" r="8" fill={flowerTypes[7].color} />
                      </g>
                    )}

                    {currentDate.getMonth() === 8 && (
                      <g>
                        <circle cx="90" cy="45" r="12" fill={flowerTypes[8].color} />
                        <circle cx="75" cy="35" r="10" fill={flowerTypes[8].color} opacity="0.9" />
                        <circle cx="105" cy="35" r="10" fill={flowerTypes[8].color} opacity="0.9" />
                        <circle cx="72" cy="55" r="9" fill={flowerTypes[8].color} opacity="0.85" />
                        <circle cx="108" cy="55" r="9" fill={flowerTypes[8].color} opacity="0.85" />
                        <circle cx="90" cy="65" r="8" fill={flowerTypes[8].color} opacity="0.8" />
                      </g>
                    )}

                    {currentDate.getMonth() === 9 && (
                      <g>
                        <circle cx="80" cy="30" r="7" fill={flowerTypes[9].color} />
                        <circle cx="100" cy="30" r="7" fill={flowerTypes[9].color} />
                        <circle cx="75" cy="45" r="7" fill={flowerTypes[9].color} opacity="0.9" />
                        <circle cx="90" cy="42" r="7" fill={flowerTypes[9].color} opacity="0.9" />
                        <circle cx="105" cy="45" r="7" fill={flowerTypes[9].color} opacity="0.9" />
                        <circle cx="70" cy="60" r="7" fill={flowerTypes[9].color} opacity="0.85" />
                        <circle cx="110" cy="60" r="7" fill={flowerTypes[9].color} opacity="0.85" />
                      </g>
                    )}

                    {currentDate.getMonth() === 10 && (
                      <g>
                        <circle cx="90" cy="40" r="11" fill={flowerTypes[10].color} />
                        <circle cx="75" cy="32" r="9" fill={flowerTypes[10].color} opacity="0.9" />
                        <circle cx="105" cy="32" r="9" fill={flowerTypes[10].color} opacity="0.9" />
                        <circle cx="78" cy="52" r="9" fill={flowerTypes[10].color} opacity="0.85" />
                        <circle cx="102" cy="52" r="9" fill={flowerTypes[10].color} opacity="0.85" />
                        <circle cx="90" cy="62" r="8" fill={flowerTypes[10].color} opacity="0.8" />
                      </g>
                    )}

                    {currentDate.getMonth() === 11 && (
                      <g>
                        <path d="M 90 30 L 75 55 L 85 50 Z" fill={flowerTypes[11].color} />
                        <path d="M 90 30 L 105 55 L 95 50 Z" fill={flowerTypes[11].color} />
                        <path d="M 90 30 L 70 45 L 80 40 Z" fill={flowerTypes[11].color} opacity="0.9" />
                        <path d="M 90 30 L 110 45 L 100 40 Z" fill={flowerTypes[11].color} opacity="0.9" />
                        <circle cx="90" cy="45" r="8" fill="#FFD700" />
                      </g>
                    )}
                    
                    {/* Label drawn above the flower with ONE LINE OF SPACE (-55 space) */}
                    <g>
                      <rect x={90 - 55} y={currentBloomY - 55} width="110" height="24" rx="12" fill="white" stroke="#E2E8F0" strokeWidth="1.5" />
                      <text x="90" y={currentBloomY - 39} textAnchor="middle" fontWeight="800" fill="#4A5568" fontSize="11" letterSpacing="0.05em">
                        {flowerTypes[currentDate.getMonth()].name.toUpperCase()}
                      </text>
                    </g>
                    </g>
                  </g>

                  {/* Water fill inside vase */}
                  <path d="M 145 125 L 141 138 L 158 155 L 202 155 L 219 138 L 215 125 Q 180 120, 145 125" 
                        fill="url(#waterGrad)" opacity="0.7" />
                  
                  {/* Water surface ripple */}
                  <ellipse cx="180" cy="125" rx="35" ry="3.5" fill="rgba(150,180,220,0.3)" />
                  
                  {/* Vase rim - top opening */}
                  <ellipse cx="180" cy="85" rx="32" ry="8" fill="#E8E8E8" stroke="#888888" strokeWidth="1.5" />
                  <ellipse cx="180" cy="83" rx="30" ry="6" fill="#F8F8F8" />
                  
                  {/* Vase highlight */}
                  <path d="M 160 100 Q 155 120, 158 150" stroke="white" strokeWidth="3" fill="none" opacity="0.5" />
                </g>

                {/* Fish Swimming in Vase */}
                <g className="fish-swimmer" style={{ transformOrigin: '180px 135px' }}>
                  {/* Fish body */}
                  <ellipse cx="180" cy="135" rx="8" ry="5" fill="#FF6B35" />
                  {/* Fish eye */}
                  <circle cx="187" cy="133" r="1.5" fill="black" />
                  {/* Fish tail */}
                  <path d="M 172 133 L 165 128 L 165 138 Z" fill="#FF6B35" />
                  {/* Tail fin detail */}
                  <path d="M 165 128 L 160 125 L 160 125" stroke="#FF4500" strokeWidth="0.8" fill="none" opacity="0.6" />
                </g>
              </svg>

              {/* Flowers have been merged into the main SVG above for perfect unified scaling */}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
