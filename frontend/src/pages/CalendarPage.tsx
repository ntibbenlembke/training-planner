import { CalendarProvider } from '../context/CalendarContext'
import Calendar from '../components/Calendar'
import GeneratePlan from '../components/GeneratePlan'

export default function CalendarPage() {
  return (
    <CalendarProvider>
      <div className="flex flex-col min-h-screen bg-paper">
        <div className="flex flex-row flex-1">
          <div className="w-3/4">
            <Calendar />
          </div>
          <div className="w-1/4 flex flex-col">
            <GeneratePlan />
          </div>
        </div>
      </div>
    </CalendarProvider>
  )
}
