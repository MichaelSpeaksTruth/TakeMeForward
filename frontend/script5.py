path = r'c:\Superceed_vscode\OPEN Source Contribution\TakeMeForward\frontend\src\components\WallCalendar.jsx'
with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

import re

# Replace state array
code = re.sub(r'const \[flipDirection, setFlipDirection\] = useState\(null\);', 
              r'const [flipState, setFlipState] = useState({ direction: null, oldDate: null, oldNotes: [] });', 
              code)

# Replace handler functions using string manipulation to avoid regex multi-line issues
s1 = '  const handlePrevMonth = () => {'
e1 = '  /**\n   * Add a new note'
idx1 = code.find(s1)
idx2 = code.find(e1)
if idx1 != -1 and idx2 != -1:
    h_new = """  const handlePrevMonth = () => {
    if (flipState.direction) return; 
    setFlipState({ direction: "prev", oldDate: currentDate, oldNotes: notes });
    setCurrentDate(subMonths(currentDate, 1));
    setStartDate(null);
    setEndDate(null);
    setTimeout(() => {
      setFlipState({ direction: null, oldDate: null, oldNotes: [] });
    }, 600);
  };

  /**
   * Navigate to the next month
   */
  const handleNextMonth = () => {
    if (flipState.direction) return; 
    setFlipState({ direction: "next", oldDate: currentDate, oldNotes: notes });
    setCurrentDate(addMonths(currentDate, 1));
    setStartDate(null);
    setEndDate(null);
    setTimeout(() => {
      setFlipState({ direction: null, oldDate: null, oldNotes: [] });
    }, 600);
  };

"""
    code = code[:idx1] + h_new + code[idx2:]
else:
    print("Failed to find handlers idx1={}, idx2={}".format(idx1, idx2))

# Extract the inner JSX
# We know it starts at `          {/* Add a top padding` and ends exactly before `        {/* ======================== */}\n        {/* SIDEBAR`
jsx_start_marker = "          {/* Add a top padding so absolutely no content rendering begins inside the bindings area! */}\n"
jsx_end_marker = "        {/* ======================== */}\n        {/* SIDEBAR - Table/Vase */}"
idx_start = code.find(jsx_start_marker)
idx_end = code.find(jsx_end_marker)

if idx_start != -1 and idx_end != -1:
    extracted_block = code[idx_start + len(jsx_start_marker):idx_end]
    # We want to keep exactly what's inside <div className={`flex flex-col...`}> ... </div>\n        </div>\n\n
    div_start = extracted_block.find('>') + 1
    div_end = extracted_block.rfind('</div>\n        </div>\n\n')
    
    if div_end == -1:
        # Fallback
        div_end = extracted_block.rfind('</div>\n        </div>')
        
    inner_content = extracted_block[div_start:div_end]
    
    # We create renderCalendarContent from it
    replaced_content = inner_content.replace('currentDate.', 'dateObj.')
    replaced_content = replaced_content.replace('notes.', 'pageNotes.')
    replaced_content = replaced_content.replace('notes.length', 'pageNotes.length')
    replaced_content = replaced_content.replace('notes.map', 'pageNotes.map')
    replaced_content = replaced_content.replace('isSameMonth(day, currentDate)', 'isSameMonth(day, dateObj)')
    replaced_content = replaced_content.replace('monthNames[currentDate.getMonth()]', 'monthNames[dateObj.getMonth()]')
    replaced_content = replaced_content.replace('getDayClasses(day)', 'getDayClassesInner(day)')
    
    new_layer_markup = """  // ========================
  // CALENDAR GENERATION FUNCTION
  // ========================
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

    const currentBloomY = bloomYPositions[dateObj.getMonth()];

    return (
      <div className={`flex flex-col lg:flex-row w-full pt-7 lg:pt-10 flex-1 min-h-0 h-full bg-white rounded-xl overflow-hidden ${isAnimating ? 'pointer-events-none' : ''}`}>""" + replaced_content + """
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

"""

    # We replace from old CALENDAR GENERATION to the old SIDEBAR marker.
    # Wait, CALENDAR GENERATION starts at line 283. So we delete everything from `  // ========================\n  // CALENDAR GENERATION` to `jsx_end_marker`.
    cg_marker = '  // ========================\n  // CALENDAR GENERATION\n  // ========================'
    cg_idx = code.find(cg_marker)
    if cg_idx != -1:
        code = code[:cg_idx] + new_layer_markup + code[idx_end:]
        print("JSX logic totally replaced successfully!")
    else:
        print("Could not find CALENDAR GENERATION marker")
else:
    print("Could not find JSX boundaries")


with open(path, 'w', encoding='utf-8') as f:
    f.write(code)

print("done script5")
