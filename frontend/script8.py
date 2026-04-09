import re

path = r'c:\Superceed_vscode\OPEN Source Contribution\TakeMeForward\frontend\src\components\WallCalendar.jsx'
with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update State
code = code.replace(
    'const [animationState, setAnimationState] = useState(null);',
    'const [flipState, setFlipState] = useState({ direction: null, oldDate: null, oldNotes: [] });'
)

# 2. Handlers
s1 = '  const handlePrevMonth = () => {'
e1 = '  const handleAddNote = () => {'
idx1 = code.find(s1)
idx2 = code.find(e1)
if idx1 != -1 and idx2 != -1:
    h_new = """  const handlePrevMonth = () => {
    if (flipState.direction) return; // Prevent double clicking
    setFlipState({ direction: "prev", oldDate: currentDate, oldNotes: notes });
    setCurrentDate(subMonths(currentDate, 1));
    setStartDate(null);
    setEndDate(null);
    setTimeout(() => {
      setFlipState({ direction: null, oldDate: null, oldNotes: [] });
    }, 1000); 
  };

  const handleNextMonth = () => {
    if (flipState.direction) return; // Prevent double clicking
    setFlipState({ direction: "next", oldDate: currentDate, oldNotes: notes });
    setCurrentDate(addMonths(currentDate, 1));
    setStartDate(null);
    setEndDate(null);
    setTimeout(() => {
      setFlipState({ direction: null, oldDate: null, oldNotes: [] });
    }, 1000);
  };

"""
    code = code[:idx1] + h_new + code[idx2:]

# 3. CSS
css_s = "        @keyframes pageFoldOutNext {"
css_e = "        .calendar-card {"
i_c1 = code.find(css_s)
i_c2 = code.find(css_e)
if i_c1 != -1 and i_c2 != -1:
    css_new = """        @keyframes pageSlowTurnNext {
          0% { transform: rotateX(0deg); filter: drop-shadow(0 0 0 rgba(0,0,0,0)); }
          50% { filter: drop-shadow(0 20px 20px rgba(0,0,0,0.3)); }
          100% { transform: rotateX(180deg); filter: drop-shadow(0 0 0 rgba(0,0,0,0)); }
        }
        @keyframes pageSlowTurnPrev {
          0% { transform: rotateX(180deg); filter: drop-shadow(0 0 0 rgba(0,0,0,0)); }
          50% { filter: drop-shadow(0 20px 20px rgba(0,0,0,0.3)); }
          100% { transform: rotateX(0deg); filter: drop-shadow(0 0 0 rgba(0,0,0,0)); }
        }
        .anim-turn-next {
          animation: pageSlowTurnNext 1s cubic-bezier(0.4, 0, 0.2, 1) forwards;
          transform-origin: center 25px;
          transform-style: preserve-3d;
          will-change: transform;
        }
        .anim-turn-prev {
          animation: pageSlowTurnPrev 1s cubic-bezier(0.4, 0, 0.2, 1) forwards;
          transform-origin: center 25px;
          transform-style: preserve-3d;
          will-change: transform;
        }
"""
    code = code[:i_c1] + css_new + code[i_c2:]

# 4. JSX Layout
jsx_s = "          {/* Simple Folding Calendar Content */}"
jsx_e = "        {/* ======================== */}\n        {/* SIDEBAR - Table/Vase */}"
idx_j1 = code.find(jsx_s)
idx_j2 = code.find(jsx_e)

if idx_j1 != -1 and idx_j2 != -1:
    jsx_new = """          {/* Component inner render helper for Calendar Content Layers */}
          {(() => {
            const renderCalendarContent = (dateObj, pageNotes, isAnimating) => {
              if (!dateObj) return null;
              
              const mStart = startOfMonth(dateObj);
              const mEnd = endOfMonth(dateObj);
              const cDays = eachDayOfInterval({
                start: new Date(mStart.getFullYear(), mStart.getMonth(), 1),
                end: new Date(mEnd.getFullYear(), mEnd.getMonth() + 1, 0),
              });
              const mDays = cDays.filter((day) => isSameMonth(day, dateObj));
              const fDayOfWeek = mStart.getDay();
              const pDays = [
                ...Array(fDayOfWeek).fill(null),
                ...mDays,
                ...Array(Math.max(0, 42 - (fDayOfWeek + mDays.length))).fill(null)
              ];
              const wks = [];
              for (let i = 0; i < pDays.length; i += 7) wks.push(pDays.slice(i, i + 7));

              const getDayClassesInner = (day) => {
                const baseClasses = "h-7 w-7 sm:h-8 sm:w-8 lg:h-10 lg:w-10 mx-auto flex items-center justify-center rounded-full font-bold text-xs sm:text-sm lg:text-base cursor-pointer transition-all duration-200 hover:shadow";
                if (!isSameMonth(day, dateObj)) return `${baseClasses} text-gray-300 bg-transparent`;
                if (startDate && isSameDay(day, startDate)) return `${baseClasses} bg-blue-600 text-white shadow-md`;
                if (endDate && isSameDay(day, endDate)) return `${baseClasses} bg-blue-600 text-white shadow-md`;
                if (startDate && endDate && isWithinInterval(day, { start: startDate, end: endDate })) return `${baseClasses} bg-blue-100 text-blue-900`;
                if (day.getDay() === 0) return `${baseClasses} bg-transparent hover:bg-gray-100 text-red-600`;
                return `${baseClasses} bg-transparent hover:bg-gray-100 text-gray-700`;
              };

              return (
                <div className={`flex flex-col lg:flex-row w-full pt-7 lg:pt-10 flex-1 min-h-0 h-full bg-white relative z-10 rounded-xl overflow-hidden ${isAnimating ? 'pointer-events-none' : ''}`}>
                  {/* LEFT: Hero Image */}
                  <div className="w-full lg:w-[320px] h-[22%] min-h-[100px] lg:h-[420px] relative overflow-hidden bg-gray-100 shrink-0 border-b lg:border-b-0 lg:border-r border-gray-200">
                    <img
                      src={monthImages[dateObj.getMonth()]}
                      alt={`${monthNames[dateObj.getMonth()]} Calendar`}
                      className="absolute inset-0 w-full h-full object-cover object-center"
                      style={{ imageRendering: '-webkit-optimize-contrast' }}
                      loading="eager"
                    />
                  </div>
                  
                  {/* RIGHT: Calendar Platform */}
                  <div className="flex-1 flex flex-col shrink-0 min-h-0 lg:h-[420px]">
                    <div className="px-4 py-2 lg:px-6 lg:py-4 bg-white border-b border-gray-50 flex items-center justify-between shrink-0">
                      <button onClick={handlePrevMonth} className="flex items-center justify-center h-8 w-8 lg:h-9 lg:w-9 rounded-full text-gray-400 hover:bg-gray-100 hover:text-gray-800 active:scale-95 transition-all">
                        <ChevronLeft size={20} />
                      </button>
                      <div className="text-center flex-1">
                        <h1 className="text-xl lg:text-2xl font-black text-gray-800 tracking-tight">{monthNames[dateObj.getMonth()]}</h1>
                        <p className="text-[10px] lg:text-[11px] font-bold text-gray-400 tracking-widest uppercase lg:mt-0.5">{dateObj.getFullYear()}</p>
                      </div>
                      <button onClick={handleNextMonth} className="flex items-center justify-center h-8 w-8 lg:h-9 lg:w-9 rounded-full text-gray-400 hover:bg-gray-100 hover:text-gray-800 active:scale-95 transition-all">
                        <ChevronRight size={20} />
                      </button>
                    </div>
                    
                    <div className="flex flex-col lg:flex-row flex-1 min-h-0 bg-white">
                      {/* CALENDAR GRID */}
                      <div className="w-full lg:w-[55%] px-3 py-2 sm:px-4 sm:py-3 lg:px-4 lg:py-4 shrink-0 flex flex-col justify-center border-b lg:border-b-0 lg:border-r border-gray-100 min-h-0">
                        <div className="grid grid-cols-7 gap-1 lg:gap-2 mb-1 lg:mb-3 shrink-0">
                          {weekDays.map((day) => (
                            <div key={day} className="text-center font-bold text-[9px] lg:text-[10px] text-gray-400 py-0.5 lg:py-1 uppercase tracking-widest">{day}</div>
                          ))}
                        </div>
                        <div className="grid grid-cols-7 gap-y-0.5 gap-x-1 sm:gap-y-1 lg:gap-y-2 lg:gap-x-2 pb-0.5 lg:pb-1">
                          {wks.map((week, weekIndex) =>
                            week.map((day, dayIndex) => (
                              <div key={`${weekIndex}-${dayIndex}`} className="flex justify-center" onClick={() => day && isSameMonth(day, dateObj) && handleDayClick(day)}>
                                {day && isSameMonth(day, dateObj) ? (
                                  <div className={getDayClassesInner(day)} title={format(day, "EEEE, MMMM d, yyyy")}>{format(day, "d")}</div>
                                ) : day ? (
                                  <div className="h-7 w-7 sm:h-8 sm:w-8 lg:h-10 lg:w-10 mx-auto flex items-center justify-center text-xs sm:text-sm lg:text-base text-gray-300 font-semibold bg-transparent">{format(day, "d")}</div>
                                ) : (
                                  <div className="h-7 w-7 sm:h-8 sm:w-8 lg:h-10 lg:w-10 bg-transparent"></div>
                                )}
                              </div>
                            ))
                          )}
                        </div>
                      </div>
                      
                      {/* NOTES PANEL */}
                      <div className="w-full lg:w-[45%] flex flex-col shrink-0 flex-1 min-h-[140px] bg-white border-l border-gray-50 overflow-hidden">
                        <div className="px-4 py-2 shrink-0 border-b border-gray-50 flex items-center justify-between">
                          <h3 className="text-[10px] lg:text-[11px] font-bold text-gray-700">📅 {getCurrentSelectionLabel()}</h3>
                          {(startDate || endDate) && <button onClick={handleClearRange} className="text-[9px] text-gray-400 hover:text-gray-700 transition-colors">Clear</button>}
                        </div>
                        <div className="flex-1 overflow-y-auto px-4 py-2 space-y-1.5 lg:space-y-2 min-h-[50px]">
                          {pageNotes.length === 0 ? (
                            <p className="text-[11px] lg:text-[12px] text-gray-300 italic py-2">No notes for {monthNames[dateObj.getMonth()]}.</p>
                          ) : (
                            pageNotes.map((note) => (
                              <div key={note.id} className="p-2 lg:p-3 rounded-lg bg-gray-50 border border-gray-200">
                                <div className="flex items-start justify-between gap-2 mb-0.5 lg:mb-1">
                                  <span className="text-[9px] lg:text-[10px] font-semibold text-gray-500">{getNoteDateLabel(note)}</span>
                                  <button onClick={() => handleDeleteNote(note.id)} className="text-gray-300 hover:text-red-500 transition-colors flex-shrink-0" title="Delete note"><X size={12} /></button>
                                </div>
                                <p className="text-[11px] lg:text-[12px] text-gray-700 break-words whitespace-pre-wrap">{note.content}</p>
                              </div>
                            ))
                          )}
                        </div>
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
              );
            };

            return (
              <div className="relative flex-1 w-full h-full min-h-0 bg-transparent z-10 rounded-xl overflow-hidden" style={{ perspective: '1500px' }}>
                
                {/* 1) STATIC BACKGROUND LAYER */}
                {/* Shows the month we are going TO (underneath the lifting page) */}
                <div className="absolute inset-0 z-0 bg-white">
                  {renderCalendarContent(
                    flipState.direction === 'prev' ? flipState.oldDate : currentDate,
                    flipState.direction === 'prev' ? flipState.oldNotes : notes,
                    !!flipState.direction // Lock pointer events during turn
                  )}
                </div>

                {/* 2) 3D ANIMATING PAGE LAYER */}
                {flipState.direction && (
                  <div className={`absolute inset-0 z-10 ${flipState.direction === 'next' ? 'anim-turn-next' : 'anim-turn-prev'}`} style={{ transformStyle: 'preserve-3d' }}>
                    
                    {/* Front Face of Page */}
                    <div className="absolute inset-0 bg-white shadow-lg overflow-hidden rounded-xl" style={{ backfaceVisibility: 'hidden' }}>
                      {renderCalendarContent(
                        flipState.direction === 'next' ? flipState.oldDate : currentDate,
                        flipState.direction === 'next' ? flipState.oldNotes : notes,
                        true
                      )}
                    </div>
                    
                    {/* Back Face of Page */}
                    <div className="absolute inset-0 bg-gray-100/90 backdrop-blur-sm rounded-xl overflow-hidden border border-gray-200/50 flex items-center justify-center opacity-95" 
                         style={{ backfaceVisibility: 'hidden', transform: 'rotateX(180deg)', boxShadow: 'inset 0 0 50px rgba(0,0,0,0.05)' }}>
                       {/* Light paper texture for the backside */}
                       <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'radial-gradient(circle, #000 1px, transparent 1px)', backgroundSize: '10px 10px' }}></div>
                    </div>

                  </div>
                )}
              </div>
            );
          })()}
        </div>

"""
    code = code[:idx_j1] + jsx_new + code[idx_j2:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
