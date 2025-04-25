import { ref } from 'vue'
import { useRouter } from 'vue-router'

export function useAuth() {
  const isAuthenticated = ref(false)
  const username = ref('')
  const userAvatar = ref('')
  const router = useRouter()

  const login = (token, userData) => {
    localStorage.setItem('auth_token', token)
    isAuthenticated.value = true
    username.value = userData.username
    userAvatar.value = userData.avatar || ''
  }

  const logout = () => {
    localStorage.removeItem('auth_token')
    isAuthenticated.value = false
    username.value = ''
    userAvatar.value = ''
    router.push('/auth')
  }

  return {
    isAuthenticated,
    username,
    userAvatar,
    login,
    logout
  }
}
