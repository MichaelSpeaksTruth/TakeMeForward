import re

path = r'c:\Superceed_vscode\OPEN Source Contribution\TakeMeForward\frontend\src\components\WallCalendar.jsx'
with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. State
code = code.replace(
    'const [flipState, setFlipState] = useState({ direction: null, oldDate: null, oldNotes: [] });',
    'const [animationState, setAnimationState] = useState(null);'
)

# 2. Handlers
s1 = '  const handlePrevMonth = () => {'
e1 = '  const handleAddNote = () => {'
idx1 = code.find(s1)
idx2 = code.find(e1)
if idx1 != -1 and idx2 != -1:
    h_new = """  const handlePrevMonth = () => {
    if (animationState) return;
    setAnimationState("prev_out");
    setTimeout(() => {
      setCurrentDate(subMonths(currentDate, 1));
      setStartDate(null);
      setEndDate(null);
      setAnimationState("prev_in");
      setTimeout(() => setAnimationState(null), 300);
    }, 300);
  };

  const handleNextMonth = () => {
    if (animationState) return;
    setAnimationState("next_out");
    setTimeout(() => {
      setCurrentDate(addMonths(currentDate, 1));
      setStartDate(null);
      setEndDate(null);
      setAnimationState("next_in");
      setTimeout(() => setAnimationState(null), 300);
    }, 300);
  };

"""
    code = code[:idx1] + h_new + code[idx2:]

# 3. CSS
css_old = """        @keyframes pageTurnNext {
          0% { transform: rotateX(0deg); filter: brightness(1) drop-shadow(0 0 0 rgba(0,0,0,0)); }
          100% { transform: rotateX(180deg); filter: brightness(0.6) drop-shadow(0 -30px 20px rgba(0,0,0,0.3)); }
        }
        @keyframes pageTurnPrev {
          0% { transform: rotateX(180deg); filter: brightness(0.6) drop-shadow(0 -30px 20px rgba(0,0,0,0.3)); }
          100% { transform: rotateX(0deg); filter: brightness(1) drop-shadow(0 0 0 rgba(0,0,0,0)); }
        }
        .paper-flip-next {
          animation: pageTurnNext 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
          transform-origin: center 20px;
          transform-style: preserve-3d;
        }
        .paper-flip-prev {
          animation: pageTurnPrev 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
          transform-origin: center 20px;
          transform-style: preserve-3d;
        }"""
css_new = """        @keyframes pageFoldOutNext {
          0% { transform: rotateX(0deg); opacity: 1; filter: brightness(1); }
          100% { transform: rotateX(90deg); opacity: 0; filter: brightness(0.5); }
        }
        @keyframes pageFoldInNext {
          0% { transform: rotateX(-90deg); opacity: 0; filter: brightness(0.5); }
          100% { transform: rotateX(0deg); opacity: 1; filter: brightness(1); }
        }
        @keyframes pageFoldOutPrev {
          0% { transform: rotateX(0deg); opacity: 1; filter: brightness(1); }
          100% { transform: rotateX(-90deg); opacity: 0; filter: brightness(0.5); }
        }
        @keyframes pageFoldInPrev {
          0% { transform: rotateX(90deg); opacity: 0; filter: brightness(0.5); }
          100% { transform: rotateX(0deg); opacity: 1; filter: brightness(1); }
        }
        .fold-next-out { animation: pageFoldOutNext 0.3s ease-in forwards; transform-origin: center 25px; transform-style: preserve-3d; }
        .fold-next-in { animation: pageFoldInNext 0.3s ease-out forwards; transform-origin: center 25px; transform-style: preserve-3d; }
        .fold-prev-out { animation: pageFoldOutPrev 0.3s ease-in forwards; transform-origin: center 25px; transform-style: preserve-3d; }
        .fold-prev-in { animation: pageFoldInPrev 0.3s ease-out forwards; transform-origin: center 25px; transform-style: preserve-3d; }"""
code = code.replace(css_old, css_new)

# 4. JSX
c1_marker = "          {/* Component inner render helper for Calendar Content Layers */}"
c2_marker = "        {/* ======================== */}\n        {/* SIDEBAR - Table/Vase */}"
idx_c1 = code.find(c1_marker)
idx_c2 = code.find(c2_marker)

if idx_c1 != -1 and idx_c2 != -1:
    simple_jsx = """          {/* Simple Folding Calendar Content */}
          <div className={`flex flex-col lg:flex-row w-full pt-7 lg:pt-10 flex-1 min-h-0 h-full bg-white relative z-10 rounded-xl overflow-hidden
            ${animationState === 'next_out' ? 'fold-next-out' : ''}
            ${animationState === 'next_in' ? 'fold-next-in' : ''}
            ${animationState === 'prev_out' ? 'fold-prev-out' : ''}
            ${animationState === 'prev_in' ? 'fold-prev-in' : ''}
          `}>
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
              
              <div className="flex flex-col lg:flex-row flex-1 min-h-0 bg-white">
                {/* CALENDAR GRID */}
                <div className="w-full lg:w-[55%] px-3 py-2 sm:px-4 sm:py-3 lg:px-4 lg:py-4 shrink-0 flex flex-col justify-center border-b lg:border-b-0 lg:border-r border-gray-100 min-h-0">
                  <div className="grid grid-cols-7 gap-1 lg:gap-2 mb-1 lg:mb-3 shrink-0">
                    {weekDays.map((day) => (
                      <div key={day} className="text-center font-bold text-[9px] lg:text-[10px] text-gray-400 py-0.5 lg:py-1 uppercase tracking-widest">{day}</div>
                    ))}
                  </div>
                  <div className="grid grid-cols-7 gap-y-0.5 gap-x-1 sm:gap-y-1 lg:gap-y-2 lg:gap-x-2 pb-0.5 lg:pb-1">
                    {weeks.map((week, weekIndex) =>
                      week.map((day, dayIndex) => (
                        <div key={`${weekIndex}-${dayIndex}`} className="flex justify-center" onClick={() => day && isSameMonth(day, currentDate) && handleDayClick(day)}>
                          {day && isSameMonth(day, currentDate) ? (
                            <div className={getDayClasses(day)} title={format(day, "EEEE, MMMM d, yyyy")}>{format(day, "d")}</div>
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
                    {notes.length === 0 ? (
                      <p className="text-[11px] lg:text-[12px] text-gray-300 italic py-2">No notes for {monthNames[currentDate.getMonth()]}.</p>
                    ) : (
                      notes.map((note) => (
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
        </div>

"""
    # Replace the gigantic nested structure with the simple one!
    code = code[:idx_c1] + simple_jsx + code[idx_c2:]
    print("Replaced whole JSX successfully")

with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
