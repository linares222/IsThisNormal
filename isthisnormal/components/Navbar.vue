<template>
  <nav class="flex justify-between items-center px-8 py-4">
    <p class="text-2xl font-bold">Isto é normal?</p>
    <div class="flex items-center gap-4">
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
      <button class="btn-sign">Sign in</button>
      <button class="btn-sign">Sign up</button>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from "vue";

const currentLanguage = ref("ENG");

const languages = [
  { code: "ENG", label: "English", flag: "🇺🇸" },
  { code: "PT", label: "Português", flag: "🇵🇹" },
];
</script>
