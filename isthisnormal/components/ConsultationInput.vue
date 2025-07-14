<template>
  <div class="max-w-4xl mx-auto">
    <div class="relative">
      <div
        class="flex items-end gap-3 bg-gray-50 rounded-2xl border border-gray-200 p-3 shadow-sm"
      >
        <div class="flex-1">
          <textarea
            v-model="newQuestion"
            @keydown.enter.prevent="handleSendQuestion"
            placeholder="Faça uma pergunta de acompanhamento..."
            rows="1"
            class="w-full bg-transparent border-none outline-none resize-none text-gray-800 placeholder-gray-500 text-sm leading-6"
            style="min-height: 24px; max-height: 120px"
            @input="autoResize"
            ref="textareaRef"
            :disabled="loading"
          />
        </div>

        <button
          @click="handleSendQuestion"
          :disabled="!newQuestion.trim() || loading"
          class="p-2 bg-black text-white rounded-full hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors relative"
        >
          <div
            v-if="loading"
            class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"
          ></div>
          <svg
            v-else
            class="w-4 h-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
            />
          </svg>
        </button>
      </div>
    </div>

    <p class="text-xs text-gray-500 text-center mt-2">
      O assistente pode cometer erros. Verifique informações importantes.
    </p>
  </div>
</template>

<script setup lang="ts">
import { useConsultationStore } from "../stores/consultation";
import { storeToRefs } from "pinia";
import { onMounted, ref, nextTick } from "vue";
import { useRoute, useRouter } from "vue-router";


const consultationStore = useConsultationStore();
const { loading } = storeToRefs(consultationStore);
const route = useRoute();
const textareaRef = ref<HTMLTextAreaElement>();

const newQuestion = ref("");
onMounted(async () => {
  await consultationStore.fetchConsultationById(route.params.id as string);
});

const autoResize = () => {
  if (textareaRef.value) {
    textareaRef.value.style.height = "auto";
    textareaRef.value.style.height = textareaRef.value.scrollHeight + "px";
  }
};

const handleSendQuestion = async () => {
  if (!newQuestion.value.trim() || loading.value) return;

  try {
    const consultationId = route.params.id as string;
    await consultationStore.addExchange(
      consultationId,
      newQuestion.value.trim()
    );
    newQuestion.value = "";

    await nextTick();
    if (textareaRef.value) {
      textareaRef.value.style.height = "auto";
    }
  } catch (error) {
    console.error("Erro ao enviar pergunta:", error);
  }
};
</script>
