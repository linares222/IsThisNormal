
interface User {
  id: string;
  email: string;
}

interface Consultation {
  id: string;
  question_text: string;
  user_id: string;
  created_at: string;
  exchanges: Exchange[];
}

interface Exchange {
  id: string;
  question_text: string;
  answer_text: string | null;
  created_at: string;
}

const makeRequest = async <T>(
  endpoint: string,
  options: RequestInit
): Promise<T> => {
  const config = useRuntimeConfig();
  const baseUrl = config.public.apiBaseUrl;

  const url = `${baseUrl}${endpoint}`;

  const headers: Record<string, string> = {};
  if (!(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }

  const requestOptions: RequestInit = {
    ...options,
    credentials: "include",
    headers: {
      ...headers,
      ...options.headers,
    },
  };

  try {
    const response = await fetch(url, requestOptions);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data: T = await response.json();
    return data;
  } catch (error) {
    console.error("Error making request:", error);
    throw error;
  }
};

export const useApi = () => {
  const loading = ref(false);
  const error = ref<string | null>(null);

  const apiRequest = async <T>(
    requestFn: () => Promise<T>
  ): Promise<T | null> => {
    loading.value = true;
    error.value = null;

    try {
      const result = await requestFn();
      return result;
    } catch (err) {
      error.value =
        err instanceof Error ? err.message : "An unknown error occurred";
      return null;
    } finally {
      loading.value = false;
    }
  };

  const login = async (
    email: string,
    password: string
  ): Promise<User | null> => {
    return apiRequest(async () => {
      const formData = new FormData();
      formData.append("email", email);
      formData.append("password", password);

      const result = await makeRequest<User>("/login", {
        method: "POST",
        body: formData,
        headers: {},
      });
      
      return result;
    });
  };

  const signup = async (
    email: string,
    password: string
  ): Promise<User | null> => {
    return apiRequest(async () => {
      const formData = new FormData();
      formData.append("email", email);
      formData.append("password", password);

      return makeRequest<User>("/signup", {
        method: "POST",
        body: formData,
        headers: {},
      });
    });
  };

  const logout = async (): Promise<boolean> => {
    const result = await apiRequest(async () => {
      return makeRequest<{ message: string }>("/logout", {
        method: "GET",
      });
    });

    return result !== null;
  };

  const getCurrentUser = async (): Promise<User | null> => {
    return apiRequest(async () => {
      try {
        const result = await makeRequest<User>("/me", {
          method: "GET",
        });
        
        return result;
      } catch (error) {
        throw error;
      }
    });
  };

  const createConsultation = async (
    questionText: string
  ): Promise<Consultation | null> => {
    return apiRequest(async () => {
      return makeRequest<Consultation>("/consultations", {
        method: "POST",
        body: JSON.stringify({ question_text: questionText }),
        headers: {},
      });
    });
  };

  const getConsultations = async (): Promise<Consultation[] | null> => {
    return apiRequest(async () => {
      return makeRequest<Consultation[]>("/consultations", {
        method: "GET",
      });
    });
  };

  const getConsultation = async (id: string): Promise<Consultation | null> => {
    return apiRequest(async () => {
      return makeRequest<Consultation>(`/consultations/${id}`, {
        method: "GET",
      });
    });
  };

  const addExchange = async (
    consultationId: string,
    questionText: string
  ): Promise<Exchange | null> => {
    return apiRequest(async () => {
      return makeRequest<Exchange>(
        `/consultations/${consultationId}/exchanges`,
        {
          method: "POST",
          body: JSON.stringify({ question_text: questionText }),
          headers: {},
        }
      );
    });
  };

  function isAuthenticated(): boolean {
    if (typeof document === "undefined") return false;
    return document.cookie.includes("access_token=");
  }

  return {
    loading: readonly(loading),
    error: readonly(error),
    apiRequest,
    login,
    signup,
    logout,
    getCurrentUser,
    createConsultation,
    getConsultations,
    getConsultation,
    addExchange,
    isAuthenticated,
  };
};

export type ApiComposable = ReturnType<typeof useApi>;
