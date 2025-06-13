import { useState, useEffect } from 'react';
import { format } from 'date-fns';
import type { CalendarEvent, EventCreate } from '../data/schemas.tsx';
import { useCalendar } from '../context/CalendarContext';
import { useCalendarEvents } from '../hooks/useCalendarEvents';
import { 
  getWeekDays, 
  formatHour, 
  createTimeSlot, 
  goToPreviousWeek, 
  goToNextWeek, 
  goToToday,
  DAY_HOURS 
} from '../utils/calendarUtils';
import TimeSlot from './elements/TimeSlot';
import EventModal from './elements/EventModal';

export default function Calendar() {
  const { currentDate, setCurrentDate, weekStart, refreshTrigger } = useCalendar();
  const [showEventModal, setShowEventModal] = useState<boolean>(false);
  const [selectedEvent, setSelectedEvent] = useState<CalendarEvent | null>(null);
  const [newEvent, setNewEvent] = useState<EventCreate>({
    title: '',
    start_time: new Date().toISOString(),
    end_time: new Date().toISOString(),
    description: ''
  });

  //current user ID. Not ready for multiple users yet.
  const userId = 3;

  const {
    events,
    isLoading,
    error,
    fetchEventsByDateRange,
    createEvent,
    updateEvent,
    deleteEvent,
  } = useCalendarEvents(userId);

  const weekDays = getWeekDays(weekStart);

  const handleNavigation = (direction: 'prev' | 'next' | 'today') => {
    switch (direction) {
      case 'prev':
        setCurrentDate(goToPreviousWeek(currentDate));
        break;
      case 'next':
        setCurrentDate(goToNextWeek(currentDate));
        break;
      case 'today':
        setCurrentDate(goToToday());
        break;
    }
  };

  const handleEventClick = (event: CalendarEvent) => {
    setSelectedEvent(event);
    setNewEvent({
      title: event.title,
      start_time: event.start_time,
      end_time: event.end_time,
      description: event.description || ''
    });
    setShowEventModal(true);
  };

  const handleSlotClick = (day: Date, hour: number) => {
    const { start, end } = createTimeSlot(day, hour);
    
    setSelectedEvent(null);
    setNewEvent({
      title: '',
      start_time: start.toISOString(),
      end_time: end.toISOString(),
      description: ''
    });
    setShowEventModal(true);
  };

  const handleModalClose = () => {
    setShowEventModal(false);
    setSelectedEvent(null);
  };

  const handleEventSave = async () => {
    if (newEvent.title.trim() === '') return;
    
    let success = false;
    
    if (selectedEvent) {
      console.log('Updating event with ID:', selectedEvent.id);
      success = !!(await updateEvent(selectedEvent.id, newEvent));
    } else {
      console.log('Creating new event');
      success = !!(await createEvent(newEvent));
      //refresh events after creating
      if (success) {
        await fetchEventsByDateRange(currentDate);
      }
    }
    
    if (success) {
      handleModalClose();
    }
  };

  const handleEventDelete = async () => {
    if (!selectedEvent) return;
    
    console.log('Deleting event with ID:', selectedEvent.id);
    const success = await deleteEvent(selectedEvent.id);
    if (success) {
      handleModalClose();
    }
  };

  //fetch events if current date changes, refresh is triggered, or component is mounted
  useEffect(() => {
    fetchEventsByDateRange(currentDate);
  }, [currentDate, fetchEventsByDateRange, refreshTrigger]);

  return (
    <div className="bg-paper border-2 border-gray-800 mx-4 mt-4 p-4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-bold">
          Week of {format(weekDays[0], 'MMMM d, yyyy')}
        </h2>
        <div className="flex gap-2">
          <button 
            className="px-4 py-2 border border-gray-800"
            onClick={() => handleNavigation('prev')}
          >
            Previous
          </button>
          <button 
            className="px-4 py-2 bg-blue text-white"
            onClick={() => handleNavigation('today')}
          >
            Today
          </button>
          <button 
            className="px-4 py-2 border border-gray-800"
            onClick={() => handleNavigation('next')}
          >
            Next
          </button>
        </div>
      </div>

      {isLoading && <div className="text-center py-2">Loading events...</div>}
      {error && <div className="text-red-500 py-2">{error}</div>}

      <div className="grid grid-cols-8 border-t border-l border-gray-800">
        {/* time column */}
        <div className="border-r border-b border-gray-800">
          <div className="h-10"></div>
          {DAY_HOURS.map(hour => (
            <div key={hour} className="h-16 border-b border-gray-300 pr-2 text-right">
              {formatHour(hour)}
            </div>
          ))}
        </div>

        {/* days columns */}
        {weekDays.map((day, index) => (
          <div key={`${day}-${index}`} className="border-r border-gray-800">
            <div className="h-10 flex justify-center items-center font-semibold border-b border-gray-800">
              <div>{format(day, 'EEE')}</div>
              <div className="ml-1 text-xs">{format(day, 'd')}</div>
            </div>
            <div>
              {DAY_HOURS.map(hour => (
                <TimeSlot 
                  key={`${day}-${index}-${hour}`}
                  day={day}
                  hour={hour}
                  events={events}
                  onSlotClick={handleSlotClick}
                  onEventClick={handleEventClick}
                />
              ))}
            </div>
          </div>
        ))}
      </div>

      <EventModal
        isOpen={showEventModal}
        selectedEvent={selectedEvent}
        newEvent={newEvent}
        isLoading={isLoading}
        onClose={handleModalClose}
        onSave={handleEventSave}
        onDelete={handleEventDelete}
        onEventChange={setNewEvent}
      />
    </div>
  );
}
