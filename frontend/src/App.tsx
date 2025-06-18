import { RouterProvider, createBrowserRouter } from 'react-router-dom'
import CalendarPage from './pages/CalendarPage'
import LoginPage from './pages/LoginPage'
import Root from './pages/Root'
import './App.css'

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    children: [
      {
        path: "/calendar",
        element: <CalendarPage />,
      },
      {
        path: "/login",
        element: <LoginPage />,
      }
    ]
  }
])

function App() {
  return (
    <RouterProvider router={router} />
  )
}

export default App
