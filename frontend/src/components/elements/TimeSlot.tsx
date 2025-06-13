import { format, parseISO } from 'date-fns';
import type { CalendarEvent } from '../../data/schemas.tsx';

interface TimeSlotProps {
  day: Date;
  hour: number;
  events: CalendarEvent[];
  onSlotClick: (day: Date, hour: number) => void;
  onEventClick: (event: CalendarEvent) => void;
}

export default function TimeSlot({ day, hour, events, onSlotClick, onEventClick }: TimeSlotProps) {
  //filter events that START within this time slot
  const slotEvents = events.filter(event => {
    try {
      if (!event.start_time) return false;
      
      const eventDate = parseISO(event.start_time);
      
      const sameDay = 
        eventDate.getFullYear() === day.getFullYear() && 
        eventDate.getMonth() === day.getMonth() && 
        eventDate.getDate() === day.getDate();
      
      const sameHour = eventDate.getHours() === hour;
      
      return sameDay && sameHour;
    } catch (err) {
      console.error('Error parsing event date:', err, event);
      return false;
    }
  });

  //math for size of events on calendar
  const getEventStyle = (event: CalendarEvent) => {
    try {
      const startTime = parseISO(event.start_time);
      const endTime = parseISO(event.end_time);
      
      const durationMs = endTime.getTime() - startTime.getTime();
      const durationHours = durationMs / (1000 * 60 * 60);
      
      const startMinute = startTime.getMinutes();
      const topOffset = (startMinute / 60) * 100;
      
      const heightPercentage = durationHours * 100;
      
      return {
        top: `${topOffset}%`,
        height: `${heightPercentage}%`,
        minHeight: '20px'
      };
    } catch (err) {
      console.error('Error calculating event style:', err, event);
      return {
        top: '0%',
        height: '100%'
      };
    }
  };

  const getEventColor = (event: CalendarEvent) => {
    if (event.event_type === 'prep') return 'bg-green-500 bg-opacity-20 border-green-500';
    if (event.event_type === 'workout') return 'bg-red-500 bg-opacity-20 border-red-500';
    if (event.event_type === 'cooldown') return 'bg-yellow-500 bg-opacity-20 border-yellow-500';
    return 'bg-blue bg-opacity-20 border-blue';
  };

  return (
    <div 
      className="border border-gray-300 h-16 relative"
      onClick={() => onSlotClick(day, hour)}
    >
      {slotEvents.map((event, index) => {
        //offset overlapping events horizontally
        const leftOffset = index * 2;
        const widthReduction = index * 10;
        
        return (
          <div 
            key={`${event.id}-${event.title}`}
            className={`absolute rounded p-1 text-xs text-paper cursor-pointer overflow-hidden z-10 ${getEventColor(event)}`}
            style={{
              ...getEventStyle(event),
              left: `${1 + leftOffset}px`,
              right: `${1 + widthReduction}px`,
            }}
            onClick={(e) => {
              e.stopPropagation();
              onEventClick(event);
            }}
          >
            <div className="font-semibold truncate">{event.title}</div>
            <div className="text-xs opacity-75 truncate">
              {format(parseISO(event.start_time), 'HH:mm')} - {format(parseISO(event.end_time), 'HH:mm')}
            </div>
          </div>
        );
      })}
    </div>
  );
} 