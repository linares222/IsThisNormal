import { defineStore } from "pinia";
import type { Consultation } from "~/types/api";

export const useConsultationStore = defineStore("consultation", {
  state: () => ({
    consultations: [] as Consultation[],
    currentConsultation: null as Consultation | null,
    loading: false as boolean,
    error: null as string | null,
  }),
  getters: {
    totalConsultations: (state) => state.consultations.length,
    hasConsultations: (state) => state.consultations.length > 0,
    getConsultationById: (state) => (id: string) => {
      return (
        state.consultations.find((consultation) => consultation.id === id) ||
        null
      );
    },
    currentExchanges: (state) => state.currentConsultation?.exchanges || [],
    hasCurrentConsultation: (state) => state.currentConsultation !== null,
  },
  actions: {
    setLoading(loading: boolean) {
      this.loading = loading;
    },

    setError(error: string | null) {
      this.error = error;
    },
    async fetchConsultations() {
      this.setLoading(true);
      this.setError(null);

      try {
        const { getConsultations } = useApi();
        const consultations = await getConsultations();
        if (consultations) {
          this.consultations = consultations;
        }
      } catch (error) {
        this.setError(
          error instanceof Error ? error.message : "An unknown error occurred"
        );
      } finally {
        this.setLoading(false);
      }
    },
    async fetchConsultationById(id: string) {
      this.setLoading(true);
      this.setError(null);

      try {
        const { getConsultation } = useApi();
        const consultation = await getConsultation(id);
        if (consultation) {
          this.currentConsultation = consultation;
        }
        return consultation;
      } catch (error) {
        this.setError(
          error instanceof Error ? error.message : "An unknown error occurred"
        );
      } finally {
        this.setLoading(false);
      }
    },
    async createConsultation(questionText: string) {
      this.setLoading(true);
      this.setError(null);

      try {
        const { createConsultation } = useApi();
        const consultation = await createConsultation(questionText);
        if (consultation) {
          this.consultations.unshift(consultation);
          this.currentConsultation = consultation; 
          return consultation; 
        }
        return null;
      } catch (error) {
        this.setError(
          error instanceof Error ? error.message : "An unknown error occurred"
        );
        return null;
      } finally {
        this.setLoading(false);
      }
    },
    async addExchange(consultationId: string, questionText: string) {
      this.setLoading(true);
      this.setError(null);

      try {
        const { addExchange } = useApi();
        const exchange = await addExchange(consultationId, questionText);
        
        if (exchange) {
        
          if (this.currentConsultation?.id === consultationId) {
            this.currentConsultation.exchanges.push(exchange);
          }
          
        
          const consultationIndex = this.consultations.findIndex(
            c => c.id === consultationId
          );
          if (consultationIndex !== -1) {
            this.consultations[consultationIndex].exchanges.push(exchange);
          }
          
          return exchange; 
        }
        return null;
      } catch (error) {
        this.setError(
          error instanceof Error ? error.message : "An unknown error occurred"
        );
        return null;
      } finally {
        this.setLoading(false);
      }
    },

    clearState() {
      this.consultations = [];
      this.currentConsultation = null;
      this.error = null;
      this.loading = false;
    },
  },
});

export default useConsultationStore;
