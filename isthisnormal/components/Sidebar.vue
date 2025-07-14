<template>
  <div
    class="fixed left-0 top-0 h-full bg-background border-r border-border z-50 flex flex-col"
    :style="{ width: FIXED_SIDEBAR_WIDTH }"
  >
    <div class="flex flex-col gap-2 p-2 border-b border-border">
      <div class="group/menu-item relative">
        <button
          class="flex w-full items-center gap-2 overflow-hidden rounded-md p-2 text-left outline-none ring-sidebar-ring transition-[width,height,padding] hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-2 active:bg-sidebar-accent active:text-sidebar-accent-foreground disabled:pointer-events-none disabled:opacity-50 group-has-[[data-sidebar=menu-action]]/menu-item:pr-8 aria-disabled:pointer-events-none aria-disabled:opacity-50 data-[active=true]:bg-sidebar-accent data-[active=true]:font-medium data-[active=true]:text-sidebar-accent-foreground data-[state=open]:hover:bg-sidebar-accent data-[state=open]:hover:text-sidebar-accent-foreground [&>span:last-child]:truncate [&>svg]:size-4 [&>svg]:shrink-0 h-12 text-sm"
        >
          <div
            class="flex aspect-square size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground"
          >
            <MessageSquare class="h-5 w-5" />
          </div>
          <div>
            <span class="font-semibold">Histórico de Consultas</span>
          </div>
        </button>
      </div>
    </div>

    <div class="flex min-h-0 flex-1 flex-col gap-2 overflow-y-auto">
      <div class="relative flex w-full min-w-0 flex-col p-2">
        <div
          class="duration-200 flex h-8 shrink-0 items-center rounded-md px-2 text-xs font-medium text-sidebar-foreground/70 outline-none ring-sidebar-ring transition-[margin,opa] ease-linear focus-visible:ring-2 [&>svg]:size-4 [&>svg]:shrink-0"
        >
          Conversas Recentes
        </div>
        <div class="w-full text-sm">
          <ul class="flex w-full min-w-0 flex-col gap-3">
            <template v-if="tabs.length === 0">
              <div
                class="flex flex-col items-center justify-center py-12 text-center"
              >
                <MessageSquare
                  class="size-16 text-sidebar-foreground/20 mb-4"
                />
                <h3 class="text-sm font-medium text-sidebar-foreground/70 mb-4">
                  Ainda não há conversas
                </h3>
                <p class="text-xs text-sidebar-foreground/50 mb-8 max-w-48">
                  Inicie uma nova conversa para ver o histórico de chats aqui
                </p>
              </div>
            </template>
            <template v-else>
              <li
                v-for="tab in tabs"
                :key="tab.id"
                class="group/menu-item relative"
              >
                <button
                  class="flex cursor-pointer w-full items-center gap-2 overflow-hidden rounded-md p-2 text-left outline-none ring-sidebar-ring transition-[width,height,padding] hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-2 active:bg-sidebar-accent active:text-sidebar-accent-foreground disabled:pointer-events-none disabled:opacity-50 group-has-[[data-sidebar=menu-action]]/menu-item:pr-8 aria-disabled:pointer-events-none aria-disabled:opacity-50 data-[active=true]:bg-sidebar-accent data-[active=true]:font-medium data-[active=true]:text-sidebar-accent-foreground data-[state=open]:hover:bg-sidebar-accent data-[state=open]:hover:text-sidebar-accent-foreground [&>span:last-child]:truncate [&>svg]:size-4 [&>svg]:shrink-0 h-8 text-sm justify-start"
                  @click="handleConsultationClick(tab.id)"
                  >
                  <MessageSquare
                    class="h-4 w-4 shrink-0 text-muted-foreground"
                  />
                  <div class="flex-1 min-w-0 flex flex-col">
                    <span class="text-sm font-medium truncate">{{
                      tab.label
                    }}</span>
                    <span class="text-xs text-muted-foreground">{{
                      tab.timestamp
                    }}</span>
                  </div>
                </button>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { MessageSquare } from "lucide-vue-next";
import { useConsultationStore } from "../stores/consultation";
import { storeToRefs } from "pinia";
import { useRouter } from "vue-router";

const router = useRouter();

const consultationStore = useConsultationStore();
const { consultations } = storeToRefs(consultationStore);
const FIXED_SIDEBAR_WIDTH = "240px";

onMounted(async () => {
  await consultationStore.fetchConsultations();
});

const tabs = computed(() => 
  consultations.value.map((consultation) => ({
    id: consultation.id,
    label: consultation.question_text,
    icon: MessageSquare,
    content: consultation.question_text,
    timestamp: new Date(consultation.created_at).toLocaleDateString('pt-PT')
  }))
);

const handleConsultationClick = (id: string) => {
  router.push(`/consultation/${id}`);
};
</script>
