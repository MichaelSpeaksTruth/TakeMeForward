import re

path = r'c:\Superceed_vscode\OPEN Source Contribution\TakeMeForward\frontend\src\components\WallCalendar.jsx'
with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update state
code = re.sub(
    r'const \[flipDirection, setFlipDirection\] = useState\(null\);',
    r'const [flipState, setFlipState] = useState({ direction: null, oldDate: null, oldNotes: [] });',
    code
)

# 2. Update handlers (Regex to find exactly handlePrevMonth and handleNextMonth)
pattern = r'  const handlePrevMonth = \(\) => \{.+?  \};'
match = re.search(pattern, code, re.DOTALL)
if match:
    handlers_new = """  const handlePrevMonth = () => {
    if (flipState.direction) return; // Prevent double clicking
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
    if (flipState.direction) return; // Prevent double clicking
    setFlipState({ direction: "next", oldDate: currentDate, oldNotes: notes });
    setCurrentDate(addMonths(currentDate, 1));
    setStartDate(null);
    setEndDate(null);
    setTimeout(() => {
      setFlipState({ direction: null, oldDate: null, oldNotes: [] });
    }, 600);
  };"""
    code = re.sub(r'  const handlePrevMonth = \(\) => \{.+?  \};\n\n  /\*\*\n   \* Navigate to the next month\n   \*/\n  const handleNextMonth = \(\) => \{.+?  \};', handlers_new, code, flags=re.DOTALL)


# 4. Content Replacement
content_start_marker = "  // ========================\n  // CALENDAR GENERATION\n  // ========================"
content_end_marker = "        {/* ======================== */}\n        {/* SIDEBAR - Table/Vase */}"

start_idx = code.find(content_start_marker)
end_idx = code.find(content_end_marker)

if start_idx != -1 and end_idx != -1:
    old_content = code[start_idx:end_idx]
    
    # We find the JSX block
    jsx_start_idx = old_content.find("          {/* Add a top padding")
    jsx_end_idx = old_content.rfind("</div>\n        </div>\n\n")
    
    if jsx_start_idx != -1:
        # Extract the div with flex flex-col...
        div_start_idx = old_content.find("<div className={`flex flex-col lg:flex-row", jsx_start_idx)
        raw_jsx = old_content[div_start_idx:jsx_end_idx]
        
        # Clean up the initial div string
        raw_jsx = re.sub(r'<div className=\{`flex flex-col lg:flex-row.+?`\}>', '', raw_jsx, count=1)
        
        raw_jsx = raw_jsx.replace('currentDate.', 'dateObj.')
        raw_jsx = raw_jsx.replace('notes.', 'pageNotes.')
        raw_jsx = raw_jsx.replace('notes.length', 'pageNotes.length')
        raw_jsx = raw_jsx.replace('notes.map', 'pageNotes.map')
        raw_jsx = raw_jsx.replace('isSameMonth(day, currentDate)', 'isSameMonth(day, dateObj)')
        raw_jsx = raw_jsx.replace('monthNames[currentDate.getMonth()]', 'monthNames[dateObj.getMonth()]')
        raw_jsx = re.sub(r'getDayClasses\(day\)', 'getDayClassesInner(day)', raw_jsx)
        
        wrapper_func = """  const renderCalendarContent = (dateObj, pageNotes, isAnimating) => {
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
      <div className={`flex flex-col lg:flex-row w-full pt-7 lg:pt-10 flex-1 min-h-0 h-full bg-white rounded-xl overflow-hidden ${isAnimating ? 'pointer-events-none' : ''}`}>""" + raw_jsx + """      </div>
    );
  };"""
        
        new_content = wrapper_func + "\n\n          {/* Calendar Content Layers */}\n          <div className=\"relative flex-1 w-full h-full min-h-0 bg-transparent z-10\">\n"
        
        new_content += """            {/* Static Background Layer (Always under) */}\n            <div className={`absolute inset-0 z-0 bg-white rounded-xl overflow-hidden ${flipState.direction ? '' : 'hidden'}`}>\n              {flipState.direction && renderCalendarContent(\n                flipState.direction === 'next' ? currentDate : flipState.oldDate,\n                flipState.direction === 'next' ? notes : flipState.oldNotes,\n                true\n              )}\n            </div>\n"""
        
        new_content += """            {/* Animating/Active Overlay Layer */}\n            <div className={`absolute inset-0 z-10 origin-[center_20px] bg-white rounded-xl overflow-hidden\n                ${flipState.direction === 'next' ? 'paper-flip-next backface-hidden' : ''}\n                ${flipState.direction === 'prev' ? 'paper-flip-prev backface-hidden' : ''}\n            `} style={{ transformStyle: 'preserve-3d', backfaceVisibility: 'hidden' }}>\n              {renderCalendarContent(\n                flipState.direction === 'next' ? flipState.oldDate : currentDate,\n                flipState.direction === 'next' ? flipState.oldNotes : notes,\n                !!flipState.direction\n              )}\n            </div>\n            {/* The physical back of the paper (just white) */}\n            {flipState.direction && <div className={`absolute inset-0 bg-gray-50 shadow-inner z-10 rounded-xl overflow-hidden pointer-events-none\n                ${flipState.direction === 'next' ? 'paper-flip-next' : ''}\n                ${flipState.direction === 'prev' ? 'paper-flip-prev' : ''}\n            `} style={{ transform: 'rotateX(180deg)', transformStyle: 'preserve-3d', backfaceVisibility: 'hidden', transformOrigin: 'center 20px' }}></div>}\n          </div>\n        </div>\n\n"""
        code = code[:start_idx] + new_content + code[end_idx:]
    else:
        print("JSX start marker not found!")

with open(path, 'w', encoding='utf-8') as f:
    f.write(code)

print('Done 2')
