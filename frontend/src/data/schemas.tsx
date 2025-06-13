
// Types for our calendar events matching the backend schemas
interface CalendarEvent {
    id: number;
    title: string;
    start_time: string; // ISO string from backend
    end_time: string; // ISO string from backend
    description?: string;
    user_id: number;
    event_type?: string;
    workout_type?: string;
    difficulty_level?: string;
    training_plan_id?: number;
    created_at: string;
    updated_at?: string;
  }
  
// Type for creating a new event
interface EventCreate {
    title: string;
    start_time: string;
    end_time: string;
    description?: string;
    event_type?: string;
    workout_type?: string;
    difficulty_level?: string;
    training_plan_id?: number;
}

// Type for updating an event
interface EventUpdate {
    title?: string;
    start_time?: string;
    end_time?: string;
    description?: string;
    event_type?: string;
    workout_type?: string;
    difficulty_level?: string;
}

export type { CalendarEvent, EventCreate, EventUpdate };
  