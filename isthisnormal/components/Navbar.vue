<template>
  <nav class="flex justify-between items-center px-8 py-4 bg-white/80 backdrop-blur-sm">
    <RouterLink to="/" class="text-2xl font-bold">Isto é normal?</RouterLink>
    <div class="flex items-center gap-4">
      <!-- 
      <div class="relative">
        <select
          v-model="currentLanguage"
          class="appearance-none border-0 shadow-none bg-gray-200 hover:bg-gray-600 hover:text-white focus:ring-0 focus:outline-none px-3 py-2 rounded-full cursor-pointer text-sm font-medium transition-colors items-center"
        >
          <option
            class="text-sm font-medium text-gray-600 transition-colors"
            value="ENG"
          >
            🇺🇸 ENG
          </option>
          <option
            class="text-sm font-medium text-gray-600 transition-colors"
            value="PT"
          >
            🇵🇹 PT
          </option>
        </select>
      </div>
      -->
      
      <NuxtLink v-if="!isLoggedIn" to="/sign-in" class="btn-sign">Sign in</NuxtLink>
      <NuxtLink v-if="!isLoggedIn" to="/sign-up" class="btn-sign">Sign up</NuxtLink>
      <NuxtLink v-else to="/" class="btn-logout" @click="handleLogout">Logout</NuxtLink>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { useAuthStore } from "../stores/auth";
const authStore = useAuthStore()
const { isLoggedIn } = storeToRefs(authStore)
import { ref } from "vue";

const currentLanguage = ref("PT");

const handleLogout = () => {
  try {
    authStore.logout()
  } catch (error) {
    console.error(error)
  }
}

// const languages = [
//   { code: "ENG", label: "English", flag: "🇺🇸" },
//   { code: "PT", label: "Português", flag: "🇵��" },
// ];
</script>
