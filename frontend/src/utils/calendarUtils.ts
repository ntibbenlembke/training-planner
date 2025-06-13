import { addDays, addHours, startOfDay } from 'date-fns';

export const DAY_HOURS = Array.from({ length: 16 }).map((_, index) => index + 6);

export function getWeekDays(weekStart: Date): Date[] {
  return Array.from({ length: 7 }).map((_, index) => addDays(weekStart, index));
}

export function formatHour(hour: number): string {
  if (hour === 12) return '12 PM';
  if (hour > 12) return `${hour - 12} PM`;
  return `${hour} AM`;
}

export function createTimeSlot(day: Date, hour: number): { start: Date; end: Date } {
  const start = addHours(startOfDay(day), hour);
  const end = addHours(start, 1);
  return { start, end };
}

export function goToPreviousWeek(currentDate: Date): Date {
  return addDays(currentDate, -7);
}

export function goToNextWeek(currentDate: Date): Date {
  return addDays(currentDate, 7);
}

export function goToToday(): Date {
  return new Date();
} 