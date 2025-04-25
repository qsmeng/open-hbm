import { ref } from 'vue';
import { useRouter } from 'vue-router';

export function useAuth() {
  const isAuthenticated = ref(false);
  const username = ref('');
  const userAvatar = ref('');

  const login = (userData) => {
    isAuthenticated.value = true;
    username.value = userData.username;
    userAvatar.value = userData.avatar;
  };

  const logout = () => {
    isAuthenticated.value = false;
    username.value = '';
    userAvatar.value = '';
    useRouter().push('/auth');
  };

  return {
    isAuthenticated,
    username,
    userAvatar,
    login,
    logout,
  };
}