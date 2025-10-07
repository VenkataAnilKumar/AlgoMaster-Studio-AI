import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useAuthStore } from '@/store/authStore'
import { useThemeStore } from '@/store/themeStore'

// Layout components
import Navbar from '@/components/layout/Navbar'
import Sidebar from '@/components/layout/Sidebar'
import Footer from '@/components/layout/Footer'

// Page components
import HomePage from '@/pages/HomePage'
import AlgorithmStudio from '@/pages/AlgorithmStudio'
import AlgorithmLibrary from '@/pages/AlgorithmLibrary'
import Visualizations from '@/pages/Visualizations'
import Benchmarks from '@/pages/Benchmarks'
import LearningPath from '@/pages/LearningPath'
import ProfilePage from '@/pages/ProfilePage'
import SettingsPage from '@/pages/SettingsPage'
import NotFoundPage from '@/pages/NotFoundPage'

// Auth components
import LoginPage from '@/pages/auth/LoginPage'
import RegisterPage from '@/pages/auth/RegisterPage'

// Protected route wrapper
import ProtectedRoute from '@/components/auth/ProtectedRoute'

const App: React.FC = () => {
  const { user, isLoading } = useAuthStore()
  const { theme } = useThemeStore()

  // Apply theme to document
  React.useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [theme])

  // Loading screen while checking authentication
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center"
        >
          <div className="w-16 h-16 border-4 border-blue-200 border-top-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            🚀 AlgoMaster-Studio-AI
          </h2>
          <p className="text-gray-600 dark:text-gray-300">
            Initializing AI-powered learning platform...
          </p>
        </motion.div>
      </div>
    )
  }

  return (
    <div className={`min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200 ${theme}`}>
      <div className="flex h-screen overflow-hidden">
        {/* Sidebar - only show when authenticated */}
        {user && (
          <motion.div
            initial={{ x: -300 }}
            animate={{ x: 0 }}
            className="hidden lg:flex lg:flex-shrink-0"
          >
            <Sidebar />
          </motion.div>
        )}

        {/* Main content area */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Navigation */}
          <Navbar />

          {/* Main content */}
          <main className="flex-1 overflow-y-auto bg-white dark:bg-gray-800">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className="h-full"
            >
              <Routes>
                {/* Public routes */}
                <Route path="/" element={<HomePage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />

                {/* Protected routes */}
                <Route
                  path="/studio"
                  element={
                    <ProtectedRoute>
                      <AlgorithmStudio />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/library"
                  element={
                    <ProtectedRoute>
                      <AlgorithmLibrary />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/visualizations"
                  element={
                    <ProtectedRoute>
                      <Visualizations />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/benchmarks"
                  element={
                    <ProtectedRoute>
                      <Benchmarks />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/learning"
                  element={
                    <ProtectedRoute>
                      <LearningPath />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/profile"
                  element={
                    <ProtectedRoute>
                      <ProfilePage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/settings"
                  element={
                    <ProtectedRoute>
                      <SettingsPage />
                    </ProtectedRoute>
                  }
                />

                {/* Catch-all route for 404 */}
                <Route path="*" element={<NotFoundPage />} />
              </Routes>
            </motion.div>
          </main>

          {/* Footer */}
          <Footer />
        </div>
      </div>

      {/* Global modals and overlays */}
      <div id="modal-root" />
      <div id="tooltip-root" />
    </div>
  )
}

export default App