<template>
  <div class="pt-24 pb-32 flex flex-col items-center relative min-h-screen">
    
    <LoadingSpinner 
      v-if="loading" 
      text="Carregando consulta..." 
      subtitle="Aguarde enquanto buscamos os dados"
    />
    
    <div v-else-if="error" class="text-center py-12">
      <div class="text-red-600 text-lg font-medium mb-2">Erro ao carregar consulta</div>
      <p class="text-gray-600 text-sm">{{ error }}</p>
      <button 
        @click="$router.go(-1)" 
        class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        Voltar
      </button>
    </div>
    
    <div v-else-if="currentConsultation" class="space-y-4 w-1/2">
      <div v-for="exchange in currentConsultation.exchanges" :key="exchange.id">
        <ExchangeCard :exchange="exchange" />
      </div>
    </div>

    
    <div class="fixed bottom-0 left-0 right-0 bg-white/60 backdrop-blur-sm border-t border-gray-200 p-4">
     <ConsultationInput />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useConsultationStore } from "../../stores/consultation";
import { storeToRefs } from "pinia";
import { onMounted, ref, nextTick } from "vue";
import { useRoute } from "vue-router";
import { Textarea } from "../../components/ui/textarea";

const route = useRoute();
const consultationStore = useConsultationStore();
const { loading, error, currentConsultation } = storeToRefs(consultationStore);

const newQuestion = ref('');
const textareaRef = ref<HTMLTextAreaElement>();

onMounted(async () => {
  await consultationStore.fetchConsultationById(route.params.id as string);
});

// Auto-resize textarea
const autoResize = () => {
  if (textareaRef.value) {
    textareaRef.value.style.height = 'auto';
    textareaRef.value.style.height = textareaRef.value.scrollHeight + 'px';
  }
};

// Handle send question
const handleSendQuestion = async () => {
  if (!newQuestion.value.trim() || loading.value) return;
  
  try {
    const consultationId = route.params.id as string;
    await consultationStore.addExchange(consultationId, newQuestion.value.trim());
    newQuestion.value = '';
    
    // Reset textarea height
    await nextTick();
    if (textareaRef.value) {
      textareaRef.value.style.height = 'auto';
    }
  } catch (error) {
    console.error('Erro ao enviar pergunta:', error);
  }
};
</script>
