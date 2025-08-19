import { RouterProvider, createBrowserRouter } from 'react-router-dom'
import CalendarPage from './pages/CalendarPage'
import LoginPage from './pages/LoginPage'
import Root from './pages/Root'
import './App.css'
import { AuthProvider } from './context/AuthContext'

// Callback page to handle Google OAuth redirect
import AuthCallback from './pages/AuthCallback.tsx'

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
      },
      {
        path: "/auth-callback",
        element: <AuthCallback />
      }
    ]
  }
])

function App() {
  return (
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  )
}

export default App
