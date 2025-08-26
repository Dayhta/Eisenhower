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
