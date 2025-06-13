import { useState, useCallback } from 'react';
import { startOfWeek, addDays } from 'date-fns';
import type { CalendarEvent, EventCreate, EventUpdate } from '../data/schemas.tsx';
import { ENDPOINTS, buildApiUrl } from '../config/api';

export function useCalendarEvents(userId: number) {
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchEventsByDateRange = useCallback(async (currentDate: Date) => {
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
      
      setEvents(processedEvents);
    } catch (err) {
      const errorMessage = 'Error fetching events: ' + (err instanceof Error ? err.message : String(err));
      setError(errorMessage);
      console.error('Error fetching events:', err);
    } finally {
      setIsLoading(false);
    }
  }, [userId]);

  const createEvent = async (eventData: EventCreate) => {
    try {
      setIsLoading(true);
      setError(null);
      
      const response = await fetch(buildApiUrl(ENDPOINTS.EVENTS, userId), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(eventData),
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Create failed:', errorText);
        throw new Error(`Failed to create event: ${response.status} ${errorText}`);
      }
      
      const newEvent = await response.json();
      return newEvent;
    } catch (err) {
      const errorMessage = 'Error creating event: ' + (err instanceof Error ? err.message : String(err));
      setError(errorMessage);
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
        body: JSON.stringify(eventData),
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
      const errorMessage = 'Error updating event: ' + (err instanceof Error ? err.message : String(err));
      setError(errorMessage);
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
      const errorMessage = 'Error deleting event: ' + (err instanceof Error ? err.message : String(err));
      setError(errorMessage);
      console.error('Error deleting event:', err);
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  return {
    events,
    isLoading,
    error,
    fetchEventsByDateRange,
    createEvent,
    updateEvent,
    deleteEvent,
  };
} 