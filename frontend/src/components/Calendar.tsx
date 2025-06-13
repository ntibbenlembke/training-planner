import { useState, useEffect, useCallback } from 'react';
import { format, startOfWeek, addDays, startOfDay, addHours, parseISO } from 'date-fns';
import type { CalendarEvent, EventCreate, EventUpdate } from '../data/schemas.tsx';
import { ENDPOINTS, buildApiUrl } from '../config/api';
import { useCalendar } from '../context/CalendarContext';

export default function Calendar() {
  const { currentDate, setCurrentDate, weekStart, refreshTrigger } = useCalendar();
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [showEventModal, setShowEventModal] = useState<boolean>(false);
  const [selectedEvent, setSelectedEvent] = useState<CalendarEvent | null>(null);
  const [newEvent, setNewEvent] = useState<EventCreate>({
    title: '',
    start_time: new Date().toISOString(),
    end_time: new Date().toISOString(),
    description: ''
  });

  // current user's ID. Not ready for multiple users yet.
  const userId = 3;

  const weekDays = (() => {
    return Array.from({ length: 7 }).map((_, index) => addDays(weekStart, index));
  })();

  // start and end hours for the calendar
  const day_hours = Array.from({ length: 16 }).map((_, index) => index + 6);

  const goToNextWeek = () => {
    const nextWeekStart = addDays(currentDate, 7);
    setCurrentDate(nextWeekStart);
  };

  const goToPreviousWeek = () => {
    const prevWeekStart = addDays(currentDate, -7);
    setCurrentDate(prevWeekStart);
  };

  const goToToday = () => {
    setCurrentDate(new Date());
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
    const start = addHours(startOfDay(day), hour);
    const end = addHours(start, 1);
    
    setSelectedEvent(null);
    setNewEvent({
      title: '',
      start_time: start.toISOString(),
      end_time: end.toISOString(),
      description: ''
    });
    setShowEventModal(true);
  };

  const TimeSlot = ({ day, hour, events }: { day: Date, hour: number, events: CalendarEvent[] }) => {
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
        
        const matches = sameDay && sameHour;
        

        
        return matches;
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

    return (
      <div 
        className="border border-gray-300 h-16 relative"
        onClick={() => handleSlotClick(day, hour)}
      >
        {slotEvents.map((event, index) => {
          // Different colors for different event types
          const getEventColor = () => {
            if (event.event_type === 'prep') return 'bg-green-500 bg-opacity-20 border-green-500';
            if (event.event_type === 'workout') return 'bg-red-500 bg-opacity-20 border-red-500';
            if (event.event_type === 'cooldown') return 'bg-yellow-500 bg-opacity-20 border-yellow-500';
            return 'bg-blue bg-opacity-20 border-blue';
          };
          
          // Offset overlapping events horizontally
          const leftOffset = index * 2;
          const widthReduction = index * 10;
          
          return (
            <div 
              key={`${event.id}-${event.title}`}
              className={`absolute rounded p-1 text-xs text-paper cursor-pointer overflow-hidden z-10 ${getEventColor()}`}
              style={{
                ...getEventStyle(event),
                left: `${1 + leftOffset}px`,
                right: `${1 + widthReduction}px`,
              }}
              onClick={(e) => {
                e.stopPropagation();
                handleEventClick(event);
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
  };

  const fetchEventsByDateRange = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      const startDay = startOfWeek(currentDate);
      const endDay = addDays(startDay, 7);
      
      
      const response = await fetch(buildApiUrl(`${ENDPOINTS.EVENTS}/${startDay.toISOString()}/${endDay.toISOString()}`, userId));
      if (!response.ok) {
        throw new Error('Failed to fetch events');
      }
      
      const data = await response.json();
      
      const processedEvents = Array.isArray(data) ? data : [];
      
      // Temporary debug: Log events and their types
      console.log('📅 Calendar: Fetched events', {
        total: processedEvents.length,
        regular: processedEvents.filter(e => !e.event_type).length,
        training: processedEvents.filter(e => e.event_type).length,
        trainingDetails: processedEvents.filter(e => e.event_type).map(e => ({
          id: e.id,
          title: e.title,
          event_type: e.event_type,
          start_time: e.start_time
        }))
      });
      
      setEvents(processedEvents);
    } catch (err) {
      setError('Error fetching events: ' + (err instanceof Error ? err.message : String(err)));
      console.error('Error fetching events:', err);
    } finally {
      setIsLoading(false);
    }
  }, [currentDate]);

  const createEvent = async (eventData: EventCreate) => {
    try {
      setIsLoading(true);
      setError(null);
      
      const response = await fetch(buildApiUrl(ENDPOINTS.EVENTS, userId), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...eventData
        }),
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Create failed:', errorText);
        throw new Error(`Failed to create event: ${response.status} ${errorText}`);
      }
      
      const newEvent = await response.json();
      // Instead of just adding to local state, refresh all events from API
      // This ensures consistency between manual and generated events
      await fetchEventsByDateRange();
      return newEvent;
    } catch (err) {
      setError('Error creating event: ' + (err instanceof Error ? err.message : String(err)));
      console.error('Error creating event:', err);
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  const updateEvent = async (eventId: number, eventData: EventUpdate) => {
    try {
      if (!eventId || eventId === undefined) {
        throw new Error('Event ID is required for update');
      }
      
      setIsLoading(true);
      setError(null);
      
      const response = await fetch(buildApiUrl(`${ENDPOINTS.EVENTS}/${eventId}`, userId), {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...eventData,
        }),
      });
      
      console.log('Update response status:', response.status);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Update failed:', errorText);
        throw new Error(`Failed to update event: ${response.status} ${errorText}`);
      }
      
      const updatedEvent = await response.json();
      setEvents(prev => prev.map(event => 
        event.id === eventId ? updatedEvent : event
      ));
      return updatedEvent;
    } catch (err) {
      setError('Error updating event: ' + (err instanceof Error ? err.message : String(err)));
      console.error('Error updating event:', err);
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  const deleteEvent = async (eventId: number) => {
    try {
      console.log('deleteEvent called with:', { eventId });
      
      if (!eventId || eventId === undefined) {
        throw new Error('Event ID is required for deletion');
      }
      
      setIsLoading(true);
      setError(null);
      
      const response = await fetch(buildApiUrl(`${ENDPOINTS.EVENTS}/${eventId}`, userId), {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      console.log('Delete response status:', response.status);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Delete failed:', errorText);
        throw new Error(`Failed to delete event: ${response.status} ${errorText}`);
      }
      
      setEvents(prev => prev.filter(event => event.id !== eventId));
      return true;
    } catch (err) {
      setError('Error deleting event: ' + (err instanceof Error ? err.message : String(err)));
      console.error('Error deleting event:', err);
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateEvent = async () => {
    if (newEvent.title.trim() === '') return;
    
    if (selectedEvent) {
      console.log('Updating event with ID:', selectedEvent.id);
      const success = await updateEvent(selectedEvent.id, newEvent);
      if (success) {
        setShowEventModal(false);
        setSelectedEvent(null);
      }
    } else {
      console.log('Creating new event');
      const success = await createEvent(newEvent);
      if (success) {
        setShowEventModal(false);
      }
    }
  };

  const handleDeleteEvent = async () => {
    if (!selectedEvent) return;
    
    console.log('Deleting event with ID:', selectedEvent.id); // Debug log
    const success = await deleteEvent(selectedEvent.id);
    if (success) {
      setShowEventModal(false);
      setSelectedEvent(null);
    }
  };

  // Fetch events when component mounts, currentDate changes, or refresh is triggered
  useEffect(() => {
    fetchEventsByDateRange();
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
            onClick={goToPreviousWeek}
          >
            Previous
          </button>
          <button 
            className="px-4 py-2 bg-blue text-white"
            onClick={goToToday}
          >
            Today
          </button>
          <button 
            className="px-4 py-2 border border-gray-800"
            onClick={goToNextWeek}
          >
            Next
          </button>
        </div>
      </div>

      {isLoading && <div className="text-center py-2">Loading events...</div>}
      {error && <div className="text-red-500 py-2">{error}</div>}

      <div className="grid grid-cols-8 border-t border-l border-gray-800">
        {/* Time column */}
        <div className="border-r border-b border-gray-800">
          <div className="h-10"></div>
          {day_hours.map(hour => (
            <div key={hour} className="h-16 border-b border-gray-300 pr-2 text-right">
              {hour === 12 ? '12 PM' : hour > 12 ? `${hour - 12} PM` : `${hour} AM`}
            </div>
          ))}
        </div>

        {/* Days columns */}
        {weekDays.map((day, index) => (
          <div key={`${day}-${index}`} className="border-r border-gray-800">
            <div className="h-10 flex justify-center items-center font-semibold border-b border-gray-800">
              <div>{format(day, 'EEE')}</div>
              <div className="ml-1 text-xs">{format(day, 'd')}</div>
            </div>
            <div>
              {day_hours.map(hour => (
                <TimeSlot 
                  key={`${day}-${index}-${hour}`}
                  day={day}
                  hour={hour}
                  events={events}
                />
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* event create/update modal */}
      {showEventModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-paper p-6 rounded w-96 border-2 border-gray-800">
            <h3 className="text-xl font-bold mb-4">
              {selectedEvent ? 'Edit Event' : 'Add New Event'}
            </h3>
            <div className="mb-4">
              <label className="block mb-1">Title</label>
              <input 
                type="text"
                className="w-full p-2 border border-gray-800"
                value={newEvent.title}
                onChange={(e) => setNewEvent({...newEvent, title: e.target.value})}
              />
            </div>
            <div className="mb-4">
              <label className="block mb-1">Description</label>
              <textarea
                className="w-full p-2 border border-gray-800"
                value={newEvent.description || ''}
                onChange={(e) => setNewEvent({...newEvent, description: e.target.value})}
              />
            </div>
            <div className="flex gap-4 mb-4">
              <div>
                <label className="block mb-1">Start Time</label>
                <input 
                  type="time"
                  className="p-2 border border-gray-800"
                  value={format(parseISO(newEvent.start_time), 'HH:mm')}
                  onChange={(e) => {
                    const [hours, minutes] = e.target.value.split(':').map(Number);
                    const newStart = new Date(parseISO(newEvent.start_time));
                    newStart.setHours(hours, minutes);
                    setNewEvent({...newEvent, start_time: newStart.toISOString()});
                  }}
                />
              </div>
              <div>
                <label className="block mb-1">End Time</label>
                <input 
                  type="time"
                  className="p-2 border border-gray-800"
                  value={format(parseISO(newEvent.end_time), 'HH:mm')}
                  onChange={(e) => {
                    const [hours, minutes] = e.target.value.split(':').map(Number);
                    const newEnd = new Date(parseISO(newEvent.end_time));
                    newEnd.setHours(hours, minutes);
                    setNewEvent({...newEvent, end_time: newEnd.toISOString()});
                  }}
                />
              </div>
            </div>
            <div className="flex justify-between">
              <div>
                {selectedEvent && (
                  <button 
                    className="px-4 py-2 bg-red-500 text-white"
                    onClick={handleDeleteEvent}
                  >
                    Delete
                  </button>
                )}
              </div>
              <div className="flex gap-2">
                <button 
                  className="px-4 py-2 border border-gray-800"
                  onClick={() => {
                    setShowEventModal(false);
                    setSelectedEvent(null);
                  }}
                >
                  Cancel
                </button>
                <button 
                  className="px-4 py-2 bg-blue text-white"
                  onClick={handleCreateEvent}
                >
                  {selectedEvent ? 'Update' : 'Create'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
