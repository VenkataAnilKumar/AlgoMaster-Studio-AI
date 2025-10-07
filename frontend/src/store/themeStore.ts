import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export type Theme = 'light' | 'dark' | 'system'

interface ThemeState {
  theme: Theme
  systemTheme: 'light' | 'dark'
  actualTheme: 'light' | 'dark'
  
  // Actions
  setTheme: (theme: Theme) => void
  toggleTheme: () => void
  setSystemTheme: (theme: 'light' | 'dark') => void
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set, get) => ({
      theme: 'system',
      systemTheme: 'light',
      actualTheme: 'light',

      setTheme: (theme: Theme) => {
        const { systemTheme } = get()
        const actualTheme = theme === 'system' ? systemTheme : theme
        
        set({ theme, actualTheme })
        
        // Apply theme to document
        if (actualTheme === 'dark') {
          document.documentElement.classList.add('dark')
        } else {
          document.documentElement.classList.remove('dark')
        }
      },

      toggleTheme: () => {
        const { theme } = get()
        const newTheme = theme === 'light' ? 'dark' : 'light'
        get().setTheme(newTheme)
      },

      setSystemTheme: (systemTheme: 'light' | 'dark') => {
        const { theme } = get()
        const actualTheme = theme === 'system' ? systemTheme : theme
        
        set({ systemTheme, actualTheme })
        
        // Apply theme if using system theme
        if (theme === 'system') {
          if (actualTheme === 'dark') {
            document.documentElement.classList.add('dark')
          } else {
            document.documentElement.classList.remove('dark')
          }
        }
      },
    }),
    {
      name: 'algomaster-theme',
    }
  )
)

// Initialize system theme detection
if (typeof window !== 'undefined') {
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  
  // Set initial system theme
  useThemeStore.getState().setSystemTheme(mediaQuery.matches ? 'dark' : 'light')
  
  // Listen for system theme changes
  mediaQuery.addEventListener('change', (e) => {
    useThemeStore.getState().setSystemTheme(e.matches ? 'dark' : 'light')
  })
  
  // Apply initial theme
  const { theme, actualTheme } = useThemeStore.getState()
  if (actualTheme === 'dark') {
    document.documentElement.classList.add('dark')
  }
}