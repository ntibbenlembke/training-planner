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
  