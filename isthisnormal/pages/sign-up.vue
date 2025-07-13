<template>
  <div class="relative min-h-screen flex items-center justify-center">
    <div class="gradient-bg"></div>
    
    <div class="relative z-10 max-w-md w-full mx-4">
      <div class="bg-white shadow-xl rounded-lg p-8">
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold text-gray-900">Criar Conta</h1>
          <p class="text-gray-600 mt-2">Crie a sua conta para começar</p>
        </div>

        <form @submit.prevent="handleSignUp" class="space-y-6">
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
              minlength="6"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-0 focus:border-gray-400 transition-colors"
              placeholder="••••••••"
            />
            <p class="text-xs text-gray-500 mt-1">Mínimo 6 caracteres</p>
          </div>

          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-2">
              Confirmar Palavra-passe
            </label>
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              type="password"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-0 focus:border-gray-400 transition-colors"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            :disabled="loading || !isFormValid"
            class="w-full bg-black text-white py-2 px-4 rounded-md hover:bg-gray-800 focus:outline-none focus:ring-0 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">A criar conta...</span>
            <span v-else>Criar Conta</span>
          </button>
        </form>

        <div v-if="error" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
          <p class="text-sm text-red-600">{{ error }}</p>
        </div>

        <div v-if="success" class="mt-4 p-3 bg-green-50 border border-green-200 rounded-md">
          <p class="text-sm text-green-600">{{ success }}</p>
        </div>

        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            Já tem conta?
            <NuxtLink to="/sign-in" class="text-black hover:underline font-medium">
              Entrar
            </NuxtLink>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'auth'
})

const form = ref({
  email: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)
const error = ref('')
const success = ref('')

const isFormValid = computed(() => {
 
})

const handleSignUp = async () => {}
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