import { defineStore } from "pinia";
import type { User } from "~/types/api";

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}

export const useAuthStore = defineStore("auth", {
  state: (): AuthState => ({
    user: null as User | null,
    isAuthenticated: false as boolean,
    loading: false as boolean,
    error: null as string | null,
  }),
  getters: {
    isLoggedIn: (state) => state.isAuthenticated && state.user !== null,
  },
  actions: {
    setUser(user: User) {
      this.user = user;
      this.isAuthenticated = true;
    },
    clearUser() {
      this.user = null;
      this.isAuthenticated = false;
    },
    setLoading(loading: boolean) {
      this.loading = loading;
    },

    async checkAuth() {
      if (import.meta.client) {
        const cookies = document.cookie;
        const hasToken = cookies.includes("access_token=");
        
        if (hasToken) {
          if (this.isAuthenticated && this.user) {
            return;
          }
          
          this.isAuthenticated = true;
          
          if (!this.user) {
            try {
              const { getCurrentUser } = useApi();
              const user = await getCurrentUser();
              if (user) {
                this.user = user;
              } else {
                this.isAuthenticated = false;
                this.user = null;
              }
            } catch (error) {
              this.isAuthenticated = false;
              this.user = null;
            }
          }
        } else {
          this.isAuthenticated = false;
          this.user = null;
        }
      }
    },

    async login(email: string, password: string) {
      this.loading = true;
      this.error = null;
      try {
        const { login } = useApi();
        const user = await login(email, password);
        if (user) {
          this.user = user;
          this.isAuthenticated = true;
        }
      } catch (error) {
        this.error =
          error instanceof Error ? error.message : "An unknown error occurred";
      } finally {
        this.loading = false;
      }
    },
    async logout() {
      this.loading = true;
      this.error = null;
      try {
        const { logout } = useApi();
        await logout();
        this.user = null;
        this.isAuthenticated = false;
      } catch (error) {
        this.error =
          error instanceof Error ? error.message : "An unknown error occurred";
      } finally {
        this.loading = false;
      }
    },
    async signup(email: string, password: string) {
      this.loading = true;
      this.error = null;
      try {
        const { signup } = useApi();
        await signup(email, password);
      } catch (error) {
        this.error =
          error instanceof Error ? error.message : "An unknown error occurred";
      } finally {
        this.loading = false;
      }
    },
  },
});
