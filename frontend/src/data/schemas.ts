// Types for our calendar events matching the backend schemas
export interface CalendarEvent {
  id: number;
  title: string;
  start_time: string;
  end_time: string;
  description?: string;
  user_id: number;
  event_type?: string;
  workout_type?: string;
  difficulty_level?: string;
  training_plan_id?: number;
  created_at: string;
  updated_at?: string;
}

export interface EventCreate {
  title: string;
  start_time: string;
  end_time: string;
  description?: string;
  event_type?: string;
  workout_type?: string;
  difficulty_level?: string;
  training_plan_id?: number;
}

export interface EventUpdate {
  title?: string;
  start_time?: string;
  end_time?: string;
  description?: string;
  event_type?: string;
  workout_type?: string;
  difficulty_level?: string;
} 