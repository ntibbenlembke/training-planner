import Header from './components/Header'
import Calendar from './components/Calendar'
import CreateEvent from './components/EventCreate'
import GeneratePlan from './components/GeneratePlan'
import './App.css'

function App() {
  return (
    <div className="flex flex-col min-h-screen bg-paper">
      <div className="w-full">
        <Header />
      </div>
      <div className="flex flex-row flex-1">
        <div className="w-3/4">
          <Calendar />
        </div>
        <div className="w-1/4 flex flex-col">
          <CreateEvent />
          <GeneratePlan />
        </div>
      </div>
    </div>
  )
}

export default App
