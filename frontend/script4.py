import os

path = r'c:\Superceed_vscode\OPEN Source Contribution\TakeMeForward\frontend\src\components\WallCalendar.jsx'
with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

# Replace state
code = code.replace(
    'const [flipDirection, setFlipDirection] = useState(null);',
    'const [flipState, setFlipState] = useState({ direction: null, oldDate: null, oldNotes: [] });'
)

# Handlers
s1 = '  const handlePrevMonth = () => {'
e1 = '  const handleAddNote = () => {'
idx1 = code.find(s1)
idx2 = code.find(e1)
if idx1 != -1 and idx2 != -1:
    h_new = """  const handlePrevMonth = () => {
    if (flipState.direction) return; 
    setFlipState({ direction: "prev", oldDate: currentDate, oldNotes: notes });
    setCurrentDate(subMonths(currentDate, 1));
    setStartDate(null);
    setEndDate(null);
    setTimeout(() => setFlipState({ direction: null, oldDate: null, oldNotes: [] }), 600);
  };

  const handleNextMonth = () => {
    if (flipState.direction) return; 
    setFlipState({ direction: "next", oldDate: currentDate, oldNotes: notes });
    setCurrentDate(addMonths(currentDate, 1));
    setStartDate(null);
    setEndDate(null);
    setTimeout(() => setFlipState({ direction: null, oldDate: null, oldNotes: [] }), 600);
  };

"""
    code = code[:idx1] + h_new + code[idx2:]

# JSX Replace
js1_marker = '{/* Add a top padding so absolutely no content rendering begins inside the bindings area! */}'
js2_marker = '</div>\n        </div>\n\n        {/* ========================'

jsx_start = code.find(js1_marker)
jsx_end = code.find(js2_marker, jsx_start)

if jsx_start != -1 and jsx_end != -1:
    # Everything inside this block is the calendar content wrapper.
    original_jsx = code[jsx_start + len(js1_marker):jsx_end]
    
    # Extract the true raw string without the top div entirely
    inner_start = original_jsx.find('>') + 1
    inner_jsx = original_jsx[inner_start:].strip()
    # The last div closes the outer div.
    inner_jsx = inner_jsx[:inner_jsx.rfind('</div>')].strip()
    
    # Replace variables:
    inner_jsx = inner_jsx.replace('currentDate.', 'dateObj.')
    inner_jsx = inner_jsx.replace('notes.', 'pageNotes.')
    inner_jsx = inner_jsx.replace('notes.length', 'pageNotes.length')
    inner_jsx = inner_jsx.replace('notes.map', 'pageNotes.map')
    inner_jsx = inner_jsx.replace('isSameMonth(day, currentDate)', 'isSameMonth(day, dateObj)')
    inner_jsx = inner_jsx.replace('monthNames[currentDate.getMonth()]', 'monthNames[dateObj.getMonth()]')
    inner_jsx = inner_jsx.replace('getDayClasses(day)', 'getDayClassesInner(day)')
    
    new_block = """          {/* Extract calendar contents inside WallCalendar component body */}
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
      <div className={`flex flex-col lg:flex-row w-full pt-7 lg:pt-10 flex-1 min-h-0 h-full bg-white rounded-xl overflow-hidden ${isAnimating ? 'pointer-events-none' : ''}`}>\n""" + inner_jsx + """\n      </div>
    );
  };

          {/* Calendar Content Layers */}
          <div className="relative flex-1 w-full h-full min-h-0 bg-transparent z-10">
            {/* Static Background Layer (Always under) */}
            <div className={`absolute inset-0 z-0 bg-white rounded-xl overflow-hidden ${flipState.direction ? '' : 'hidden'}`}>
              {flipState.direction && renderCalendarContent(
                flipState.direction === 'next' ? currentDate : flipState.oldDate,
                flipState.direction === 'next' ? notes : flipState.oldNotes,
                true
              )}
            </div>

            {/* Animating/Active Overlay Layer */}
            <div className={`absolute inset-0 z-10 origin-[center_20px] bg-white rounded-xl overflow-hidden
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
              <div className={`absolute inset-0 bg-gray-50 shadow-inner z-10 rounded-xl overflow-hidden pointer-events-none
                  ${flipState.direction === 'next' ? 'paper-flip-next' : ''}
                  ${flipState.direction === 'prev' ? 'paper-flip-prev' : ''}
              `} style={{ transform: 'rotateX(180deg)', transformStyle: 'preserve-3d', backfaceVisibility: 'hidden', transformOrigin: 'center 20px' }}></div>
            )}
          </div>
"""
    code = code[:jsx_start] + new_block + code[jsx_end:]
    print('JSX REPLACED!')
else:
    print('JSX MATCH FAILED')

with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
