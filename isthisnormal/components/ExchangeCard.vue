<template>
  <div>
    <p class="font-semibold text-xl">{{ exchange.question_text }}</p>
    <hr class="border-gray-200 my-4" />
    <p class="text-gray-500">{{ exchange.answer_text }}</p>
    <div class="flex justify-end items-center gap-2">
      <Icon
        v-if="exchange.answer_text"
        @click="copyToClipboard(exchange.answer_text)"
        name="mdi:content-copy"
        class="w-5 h-5 cursor-pointer hover:text-gray-700 active:text-gray-300"
      />
      <span class="text-sm text-gray-500">{{
        new Date(exchange.created_at).toLocaleString("pt-PT", {
          day: "2-digit",
          month: "2-digit",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
          hour12: false,
        })
      }}</span>
    </div>
    <hr class="border-gray-200 my-4" />
  </div>
</template>

<script setup lang="ts">
import type { Exchange } from "../types/api";

const props = defineProps<{
  exchange: Exchange;
}>();

const copyToClipboard = (text: string | null) => {
  if (text) {
    navigator.clipboard.writeText(text);
  }
};
</script>
