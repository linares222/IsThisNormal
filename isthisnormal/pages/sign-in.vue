<template>
  <div class="relative min-h-screen flex items-center justify-center">
    <div class="gradient-bg"></div>
    
    <div class="relative z-10 max-w-md w-full mx-4">
      <div class="bg-white shadow-xl rounded-lg p-8">
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold text-gray-900">Entrar</h1>
          <p class="text-gray-600 mt-2">Entre na sua conta para continuar</p>
        </div>

        <form @submit.prevent="handleSignIn" class="space-y-6">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Email
            </label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-0 focus:border-gray-400 transition-colors"
              placeholder="seu@email.com"
            />
          </div>

    <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              Palavra-passe
            </label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-0 focus:border-gray-400 transition-colors"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-black text-white py-2 px-4 rounded-md hover:bg-gray-800 focus:outline-none focus:ring-0 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">A entrar...</span>
            <span v-else>Entrar</span>
          </button>
        </form>

        <div v-if="error" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
          <p class="text-sm text-red-600">{{ error }}</p>
        </div>

        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            Não tem conta?
            <NuxtLink to="/sign-up" class="text-black hover:underline font-medium">
              Criar conta
            </NuxtLink>
          </p>
        </div>
      </div>
    </div>
    </div>
</template>

<script setup>
const authStore = useAuthStore()
const { loading, error } = storeToRefs(authStore)
// Meta data
definePageMeta({
  layout: 'auth'
})

// Reactive data
const form = ref({
  email: '',
  password: ''
})



// Methods
const handleSignIn = async () => {
  try {
    loading.value = true
    await authStore.login(form.value.email, form.value.password)
    navigateTo('/')
  } catch (error) {
    console.error('Login error:', error)
    error.value = error.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.gradient-bg {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 500px;
    height: 500px;
    background: radial-gradient(
      circle at center,
      rgba(59, 130, 246, 0.4) 0%,
      rgba(59, 130, 246, 0.2) 50%,
      transparent 70%
    );
    border-radius: 50%;
    z-index: -10;
    pointer-events: none;
    filter: blur(30px);
  }
</style>