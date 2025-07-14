<template>
  <div class="flex flex-col items-center justify-center py-12">
    <div class="relative">
      <div class="w-12 h-12 border-4 border-gray-200 border-t-blue-600 rounded-full animate-spin"></div>
    </div>
    
    <p class="mt-4 text-gray-600 text-sm font-medium">{{ text }}</p>
    
    <p v-if="subtitle" class="mt-1 text-gray-400 text-xs">{{ subtitle }}</p>
  </div>
</template>

<script setup lang="ts">
interface Props {
  text?: string;
  subtitle?: string;
}

withDefaults(defineProps<Props>(), {
  text: 'Carregando...',
  subtitle: ''
});
</script>
