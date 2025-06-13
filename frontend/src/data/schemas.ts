// Types for our calendar events matching the backend schemas
export interface CalendarEvent {
  id: number;
  title: string;
  start_time: string;
  end_time: string;
  description?: string;
  user_id: number;
}

export interface EventCreate {
  title: string;
  start_time: string;
  end_time: string;
  description?: string;
}

export interface EventUpdate {
  title?: string;
  start_time?: string;
  end_time?: string;
  description?: string;
} 