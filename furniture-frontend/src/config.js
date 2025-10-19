// API Configuration
// You can change this URL to match your backend
export const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

// Alternative URLs for different environments
// export const API_BASE = "http://localhost:8000";
// export const API_BASE = "https://your-backend-url.com";

export const API_ENDPOINTS = {
  CHAT: `${API_BASE}/recommend/chat`,
  ANALYTICS: `${API_BASE}/analytics/summary`
};

// Debug info
console.log('🔗 API Configuration:', {
  API_BASE,
  CHAT_ENDPOINT: API_ENDPOINTS.CHAT,
  ANALYTICS_ENDPOINT: API_ENDPOINTS.ANALYTICS
});
