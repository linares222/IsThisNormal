<template>
  <div class="relative">
    <div>
      <div class="gradient-bg"></div>
    </div>
    <div class="flex flex-col justify-center items-center h-screen gap-10 px-8">
      <h1 class="text-4xl font-bold text-center">
        O que se passa com a sua criança?
      </h1>

      <div class="flex flex-col items-center gap-8 max-w-6xl w-full">
        
        <!-- Loading State - substitui o form -->
        <div v-if="loading" class="flex flex-col gap-4 shadow-lg bg-white p-6 rounded-lg w-1/2 h-[200px] flex items-center justify-center">
          <LoadingSpinner 
            text="Criando consulta..." 
            subtitle="Aguarde enquanto processamos sua pergunta"
          />
        </div>

        <!-- Normal State - form da pergunta -->
        <div v-else class="flex flex-col gap-4 shadow-lg bg-white p-6 rounded-lg w-1/2">
          <Textarea
            placeholder="O meu filho está com..."
            class="h-24 resize-none focus:ring-0 focus:border-gray-300 focus:outline-none border-none shadow-none focus-visible:ring-0 focus-visible:ring-offset-0"
            v-model="question"
          />
          <div class="flex justify-end">
            <button
              :disabled="!question.trim()"
              class="rounded-full bg-black text-white px-6 py-2 hover:bg-gray-800 transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
              @click="handleSubmitQuestion(question)"
            >
              →
            </button>
          </div>
        </div>

        <!-- Exemplos de perguntas - sempre visível -->
        <div class="w-1/2 flex justify-start">
          <div class="flex flex-col gap-3">
            <h3 class="text-sm font-semibold text-gray-600">
              Exemplos de perguntas:
            </h3>
            <div class="flex flex-col gap-2">
              <button
                @click="handleQuestionClick(item.id)"
                v-for="item in questions"
                :key="item.id"
                :disabled="loading"
                class="flex items-start gap-3 px-3 py-2 hover:bg-gray-50 cursor-pointer transition-colors rounded-full border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <p class="text-sm font-medium text-gray-700">
                  {{ item.question }}
                </p>
                <span class="text-gray-400 text-sm mt-0.5">→</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { storeToRefs } from "pinia";
import { Textarea } from "@/components/ui/textarea";
import { useAuthStore } from "@/stores/auth";
import { useConsultationStore } from "@/stores/consultation";

const authStore = useAuthStore();
const consultationStore = useConsultationStore();

const { loading, error } = storeToRefs(consultationStore);
const { isLoggedIn } = storeToRefs(authStore);

const questions = [
  {
    id: 1,
    question: "O meu filho está com soluços, é normal?",
  },
  {
    id: 2,
    question: "O meu filho está com fezes verdes, é normal?",
  },
  {
    id: 3,
    question: "O meu filho está com febre e dores de garganta, é normal?",
  },
  {
    id: 4,
    question: "A minha criança está com diarreia, é normal?",
  },
];

const question = ref("");

const handleQuestionClick = (id) => {
  if (loading.value) return; // Prevenir cliques durante loading
  
  const selectedQuestion = questions.find((item) => item.id === id);
  if (selectedQuestion) {
    question.value = selectedQuestion.question;
  }
};

const handleSubmitQuestion = async (questionText) => {
  if (!isLoggedIn.value) {
    await navigateTo("/sign-in");
    return;
  }

  if (!questionText || questionText.trim() === "") {
    return;
  }

  try {
    const consultation = await consultationStore.createConsultation(questionText.trim());
    
    if (consultation) {
      question.value = ""; // Limpar campo
      await navigateTo(`/consultation/${consultation.id}`);
    }
  } catch (error) {
    console.error("Erro ao criar consulta:", error);
  }
};
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
