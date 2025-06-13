import { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';
import { startOfWeek, addDays } from 'date-fns';

interface CalendarContextType {
  currentDate: Date;
  weekStart: Date;
  weekEnd: Date;
  setCurrentDate: (date: Date) => void;
  refreshTrigger: number;
  triggerRefresh: () => void;
}

const CalendarContext = createContext<CalendarContextType | undefined>(undefined);

export function CalendarProvider({ children }: { children: ReactNode }) {
  const [currentDate, setCurrentDate] = useState<Date>(new Date());
  const [refreshTrigger, setRefreshTrigger] = useState<number>(0);
  
  // Calculate week start and end dates
  const weekStart = startOfWeek(currentDate);
  const weekEnd = addDays(weekStart, 7);

  const triggerRefresh = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  const value = {
    currentDate,
    weekStart,
    weekEnd,
    setCurrentDate,
    refreshTrigger,
    triggerRefresh
  };

  return (
    <CalendarContext.Provider value={value}>
      {children}
    </CalendarContext.Provider>
  );
}

export function useCalendar() {
  const context = useContext(CalendarContext);
  if (context === undefined) {
    throw new Error('useCalendar must be used within a CalendarProvider');
  }
  return context;
} 