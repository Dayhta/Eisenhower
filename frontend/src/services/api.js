import axios from "axios";

// Determine API base dynamically:
// 1. Use build-time env (REACT_APP_API_BASE) if provided.
// 2. Fallback to relative '/api' so nginx reverse proxy works in prod.
// 3. Last resort explicit dev default 'http://localhost:8000/api'.
const API_BASE_URL =
  process.env.REACT_APP_API_BASE ||
  (window?.location?.port === "3000" ? "http://localhost:8000/api" : "/api");

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token expiration and authentication failures
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid - clear it
      localStorage.removeItem('access_token');
      // Don't reload - let the app handle the auth state change
      // The app will detect missing token and show login form
    }
    return Promise.reject(error);
  }
);

// Authentication utilities
export const setAccessToken = (token) => {
  if (token) {
    localStorage.setItem('access_token', token);
  } else {
    localStorage.removeItem('access_token');
  }
};

export const getAccessToken = () => {
  return localStorage.getItem('access_token');
};

export const authService = {
  // Login
  login: async (email, password) => {
    // FastAPI OAuth2 expects form data, not JSON
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await api.post("/auth/login", formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },

  // Register
  register: async (email, password) => {
    const response = await api.post("/auth/register", {
      email: email,
      password: password,
    });
    return response.data;
  },

  // Logout
  logout: () => {
    setAccessToken(null);
  },

  // Get current user info
  getCurrentUser: async () => {
    const response = await api.get("/auth/me");
    return response.data;
  },
};

export const taskService = {
  // Get all tasks
  getAllTasks: async () => {
    const response = await api.get("/tasks/");
    return response.data;
  },

  // Create a new task
  createTask: async (task) => {
    const response = await api.post("/tasks/", task);
    return response.data;
  },

  // Update a task
  updateTask: async (id, task) => {
    const response = await api.put(`/tasks/${id}`, task);
    return response.data;
  },

  // Delete a task
  deleteTask: async (id) => {
    const response = await api.delete(`/tasks/${id}`);
    return response.data;
  },

  // Get matrix data
  getMatrixData: async () => {
    const response = await api.get("/tasks/matrix/data");
    return response.data;
  },
};
