path = r'c:\Superceed_vscode\OPEN Source Contribution\TakeMeForward\frontend\src\components\WallCalendar.jsx'
with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

import re

# We know handlers and state are already updated.
# Update CSS:
css_old = r"""        @keyframes pageTurnNext {
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
        }"""
css_new = r"""        @keyframes pageTurnNext {
          0% { transform: rotateX(0deg); filter: brightness(1) drop-shadow(0 0 0 rgba(0,0,0,0)); }
          100% { transform: rotateX(180deg); filter: brightness(0.6) drop-shadow(0 -30px 20px rgba(0,0,0,0.2)); }
        }
        @keyframes pageTurnPrev {
          0% { transform: rotateX(180deg); filter: brightness(0.6) drop-shadow(0 -30px 20px rgba(0,0,0,0.2)); }
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
        
code = code.replace(css_old, css_new)

# Locate the big JSX block!
start_marker = "          {/* Add a top padding so absolutely no content rendering begins inside the bindings area! */}"

# Notice that the `</div>` that closes that box is just above `{/* ======================== */}\n        {/* SIDEBAR`
end_marker = "        {/* SIDEBAR - Table/Vase */}"

idx_s = code.find(start_marker)
idx_e = code.find(end_marker)

if idx_s != -1 and idx_e != -1:
    extracted_block = code[idx_s:idx_e]
    
    # Locate the inner JSX by finding the first `<div` after the start_marker
    div_start = extracted_block.find('<div')
    div_inner_start = extracted_block.find('>', div_start) + 1
    
    # We strip out the outer `</div>` at the end
    raw_inner = extracted_block[div_inner_start:]
    # Go backwards to strip the closed divs
    raw_inner = raw_inner[:raw_inner.rfind('</div>\n        </div>')]
    
    replaced = raw_inner.replace('currentDate.', 'dateObj.')
    replaced = replaced.replace('notes.', 'pageNotes.')
    replaced = replaced.replace('notes.length', 'pageNotes.length')
    replaced = replaced.replace('notes.map', 'pageNotes.map')
    replaced = replaced.replace('isSameMonth(day, currentDate)', 'isSameMonth(day, dateObj)')
    replaced = replaced.replace('monthNames[currentDate.getMonth()]', 'monthNames[dateObj.getMonth()]')
    replaced = replaced.replace('getDayClasses(day)', 'getDayClassesInner(day)')
    
    new_code_block = """          {/* Extract calendar contents inside WallCalendar component body */}
  const renderCalendarContent = (dateObj, pageNotes, isAnimating) => {
    if (!dateObj) return null;
    const monthStart = startOfMonth(dateObj);
    const monthEnd = endOfMonth(dateObj);
    const calendarDays = eachDayOfInterval({
      start: new Date(monthStart.getFullYear(), monthStart.getMonth(), 1),
      end: new Date(monthEnd.getFullYear(), monthEnd.getMonth() + 1, 0),
    });
    const monthDays = calendarDays.filter((day) => isSameMonth(day, dateObj));
    const firstDayOfWeek = monthStart.getDay();
    const fullyPaddedDays = [
      ...Array(firstDayOfWeek).fill(null),
      ...monthDays,
      ...Array(Math.max(0, 42 - (firstDayOfWeek + monthDays.length))).fill(null)
    ];
    const weeks = [];
    for (let i = 0; i < fullyPaddedDays.length; i += 7) weeks.push(fullyPaddedDays.slice(i, i + 7));

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
      <div className={`flex flex-col lg:flex-row w-full pt-7 lg:pt-10 flex-1 min-h-0 h-full bg-white rounded-xl overflow-hidden ${isAnimating ? 'pointer-events-none' : ''}`}>""" + replaced + """
      </div>
    );
  };

          {/* Calendar Content Layers */}
          <div className="relative flex-1 w-full h-full min-h-0 bg-transparent z-10 rounded-xl overflow-hidden">
            {/* Static Background Layer (Always under) */}
            <div className={`absolute inset-0 z-0 bg-white ${flipState.direction ? '' : 'hidden'}`}>
              {flipState.direction && renderCalendarContent(
                flipState.direction === 'next' ? currentDate : flipState.oldDate,
                flipState.direction === 'next' ? notes : flipState.oldNotes,
                true
              )}
            </div>

            {/* Animating/Active Overlay Layer */}
            <div className={`absolute inset-0 z-10 origin-[center_20px] bg-white 
                ${flipState.direction === 'next' ? 'paper-flip-next backface-hidden' : ''}
                ${flipState.direction === 'prev' ? 'paper-flip-prev backface-hidden' : ''}
            `} style={{ transformStyle: 'preserve-3d', backfaceVisibility: 'hidden' }}>
              {renderCalendarContent(
                flipState.direction === 'next' ? flipState.oldDate : currentDate,
                flipState.direction === 'next' ? flipState.oldNotes : notes,
                !!flipState.direction
              )}
            </div>
            
            {/* The physical back of the paper (just white) */}
            {flipState.direction && (
              <div className={`absolute inset-0 bg-gray-50 shadow-inner z-10 pointer-events-none
                  ${flipState.direction === 'next' ? 'paper-flip-next' : ''}
                  ${flipState.direction === 'prev' ? 'paper-flip-prev' : ''}
              `} style={{ transform: 'rotateX(180deg)', transformStyle: 'preserve-3d', backfaceVisibility: 'hidden', transformOrigin: 'center 20px' }}></div>
            )}
          </div>
        </div>

        {/* ======================== */}
"""
    
    # We also need to strip everything from `  // ========================\n  // CALENDAR GENERATION` to `start_marker` since we put it inside `renderCalendarContent`!
    old_cg_start = code.find('  // ========================\n  // CALENDAR GENERATION\n')
    if old_cg_start != -1:
        code = code[:old_cg_start] + new_code_block + code[idx_e:]
        print("Replaced whole block")

with open(path, 'w', encoding='utf-8') as f:
    f.write(code)

print("done script6")
