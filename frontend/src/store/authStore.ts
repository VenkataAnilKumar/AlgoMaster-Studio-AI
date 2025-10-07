import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export interface User {
  id: string
  email: string
  username: string
  firstName: string
  lastName: string
  avatar?: string
  role: 'user' | 'premium' | 'admin'
  preferences: {
    theme: 'light' | 'dark' | 'system'
    language: string
    notifications: boolean
    autoSave: boolean
    codeTheme: string
    fontSize: number
  }
  subscription: {
    plan: 'free' | 'pro' | 'enterprise'
    expiresAt?: string
    features: string[]
  }
  progress: {
    algorithmsCompleted: number
    totalTime: number
    streak: number
    level: number
    xp: number
  }
  createdAt: string
  lastLoginAt: string
}

interface AuthState {
  user: User | null
  token: string | null
  isLoading: boolean
  isAuthenticated: boolean
  
  // Actions
  login: (email: string, password: string) => Promise<void>
  register: (userData: RegisterData) => Promise<void>
  logout: () => void
  updateUser: (userData: Partial<User>) => void
  refreshToken: () => Promise<void>
  setLoading: (loading: boolean) => void
}

interface RegisterData {
  email: string
  password: string
  username: string
  firstName: string
  lastName: string
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isLoading: false,
      isAuthenticated: false,

      login: async (email: string, password: string) => {
        try {
          set({ isLoading: true })
          
          // For demo purposes, create a mock user
          const mockUser: User = {
            id: 'demo-user-123',
            email,
            username: email.split('@')[0],
            firstName: 'Demo',
            lastName: 'User',
            avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${email}`,
            role: 'user',
            preferences: {
              theme: 'dark',
              language: 'en',
              notifications: true,
              autoSave: true,
              codeTheme: 'vs-dark',
              fontSize: 14,
            },
            subscription: {
              plan: 'pro',
              features: ['ai_analysis', 'visualizations', 'benchmarking', 'unlimited_algorithms'],
            },
            progress: {
              algorithmsCompleted: 23,
              totalTime: 1247,
              streak: 7,
              level: 5,
              xp: 2340,
            },
            createdAt: new Date().toISOString(),
            lastLoginAt: new Date().toISOString(),
          }

          const mockToken = `demo_token_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`

          set({
            user: mockUser,
            token: mockToken,
            isAuthenticated: true,
            isLoading: false,
          })

          // In a real app, this would be an API call
          console.log('🚀 Demo login successful for:', email)
          
        } catch (error) {
          console.error('Login failed:', error)
          set({ isLoading: false })
          throw error
        }
      },

      register: async (userData: RegisterData) => {
        try {
          set({ isLoading: true })
          
          // Mock registration - in real app, this would be an API call
          const newUser: User = {
            id: `user_${Date.now()}`,
            email: userData.email,
            username: userData.username,
            firstName: userData.firstName,
            lastName: userData.lastName,
            avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${userData.email}`,
            role: 'user',
            preferences: {
              theme: 'light',
              language: 'en',
              notifications: true,
              autoSave: true,
              codeTheme: 'vs-light',
              fontSize: 14,
            },
            subscription: {
              plan: 'free',
              features: ['basic_analysis', 'limited_algorithms'],
            },
            progress: {
              algorithmsCompleted: 0,
              totalTime: 0,
              streak: 0,
              level: 1,
              xp: 0,
            },
            createdAt: new Date().toISOString(),
            lastLoginAt: new Date().toISOString(),
          }

          const token = `token_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`

          set({
            user: newUser,
            token,
            isAuthenticated: true,
            isLoading: false,
          })

          console.log('🎉 Registration successful for:', userData.email)
          
        } catch (error) {
          console.error('Registration failed:', error)
          set({ isLoading: false })
          throw error
        }
      },

      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        })
        console.log('👋 User logged out')
      },

      updateUser: (userData: Partial<User>) => {
        const currentUser = get().user
        if (currentUser) {
          set({
            user: { ...currentUser, ...userData },
          })
        }
      },

      refreshToken: async () => {
        try {
          const currentToken = get().token
          if (!currentToken) {
            throw new Error('No token to refresh')
          }

          // Mock token refresh - in real app, this would be an API call
          const newToken = `refreshed_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
          
          set({ token: newToken })
          console.log('🔄 Token refreshed')
          
        } catch (error) {
          console.error('Token refresh failed:', error)
          // If refresh fails, logout the user
          get().logout()
          throw error
        }
      },

      setLoading: (loading: boolean) => {
        set({ isLoading: loading })
      },
    }),
    {
      name: 'algomaster-auth',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)

// Auth utilities
export const getAuthHeader = () => {
  const token = useAuthStore.getState().token
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export const isTokenExpired = (token: string): boolean => {
  try {
    // In a real app, you'd decode the JWT and check the expiration
    // For demo purposes, we'll assume tokens are valid for 1 hour
    const tokenTimestamp = parseInt(token.split('_')[1])
    const now = Date.now()
    const oneHour = 60 * 60 * 1000
    
    return (now - tokenTimestamp) > oneHour
  } catch {
    return true
  }
}

export const requireAuth = () => {
  const { isAuthenticated, user } = useAuthStore.getState()
  if (!isAuthenticated || !user) {
    throw new Error('Authentication required')
  }
  return user
}

// Demo login function for quick access
export const demoLogin = async () => {
  const { login } = useAuthStore.getState()
  await login('demo@algomaster.studio', 'demo123')
}