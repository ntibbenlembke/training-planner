import Header from './components/Header'
import Calendar from './components/Calendar'
import GeneratePlan from './components/GeneratePlan'
import { CalendarProvider } from './context/CalendarContext'
import './App.css'

function App() {
  return (
    <CalendarProvider>
      <div className="flex flex-col min-h-screen bg-paper">
        <div className="w-full">
          <Header />
        </div>
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

export default App
