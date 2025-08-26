import React, { useState, useEffect } from "react";
import "./App.css";
import TaskForm from "./components/TaskForm";
import TaskList from "./components/TaskList";
import EisenhowerMatrix from "./components/EisenhowerMatrix";
import AuthPanel from "./components/AuthPanel";
import { taskService, authService } from "./services/api";

function App() {
  const [tasks, setTasks] = useState([]);
  const [matrixData, setMatrixData] = useState(null);
  const [editingTask, setEditingTask] = useState(null);
  const [activeTab, setActiveTab] = useState("list");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const checkAuth = () => {
    const token = localStorage.getItem('access_token');
    setIsAuthenticated(!!token);
    return !!token;
  };

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      setIsAuthenticated(true);
      fetchUserInfo();
      fetchTasks();
      fetchMatrixData();
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUserInfo = async () => {
    try {
      const userData = await authService.getCurrentUser();
      setUser(userData);
    } catch (err) {
      console.error("Failed to fetch user info:", err);
      handleLogout();
    }
  };

  const fetchTasks = async () => {
    try {
      const data = await taskService.getAllTasks();
      setTasks(data.tasks);
      setError("");
    } catch (err) {
      if (err.response?.status === 401) {
        handleLogout();
      } else {
        setError("Failed to fetch tasks. Please check if the backend is running.");
      }
    } finally {
      setLoading(false);
    }
  };

  const fetchMatrixData = async () => {
    try {
      const data = await taskService.getMatrixData();
      setMatrixData(data);
    } catch (err) {
      if (err.response?.status === 401) {
        handleLogout();
      } else {
        console.error("Failed to fetch matrix data:", err);
      }
    }
  };

  const handleLogin = async () => {
    setIsAuthenticated(true);
    await fetchUserInfo();
    await fetchTasks();
    await fetchMatrixData();
    setLoading(false);
  };

  const handleLogout = () => {
    authService.logout();
    setIsAuthenticated(false);
    setUser(null);
    setTasks([]);
    setMatrixData(null);
    setEditingTask(null);
    setActiveTab("list");
    setError("");
  };

  const handleTaskCreated = (newTask) => {
    setTasks((prev) => [newTask, ...prev].sort((a, b) => b.priority_score - a.priority_score));
    fetchMatrixData(); // Refresh matrix data
  };

  const handleTaskUpdated = (updatedTask) => {
    setTasks((prev) =>
      prev.map((task) => (task.id === updatedTask.id ? updatedTask : task))
        .sort((a, b) => b.priority_score - a.priority_score)
    );
    setEditingTask(null);
    fetchMatrixData(); // Refresh matrix data
  };

  const handleTasksUpdated = () => {
    fetchTasks();
    fetchMatrixData();
  };

  const handleTaskEdit = (task) => {
    setEditingTask(task);
    setActiveTab("form");
  };

  const handleCancelEdit = () => {
    setEditingTask(null);
  };

  if (loading) {
    return (
      <div className="App">
        <div className="loading">Loading...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="App">
        <header className="App-header">
          <h1>Eisenhower Matrix Todo App</h1>
          <p>Login or register to manage your tasks</p>
        </header>
        <AuthPanel onAuth={handleLogin} />
      </div>
    );
  }

  return (
      <div className="App">
        <header className="App-header">
          <h1>Eisenhower Matrix Todo App</h1>
          <p>Prioritize your tasks using the Eisenhower Decision Matrix</p>
          <div className="user-info">
            Welcome, {user?.email || 'User'}! 
            <button className="logout-btn" onClick={handleLogout}>Logout</button>
          </div>
        </header>
        {error && <div className="error-banner">{error}</div>}
        <nav className="tab-nav">
          <button className={activeTab === "form" ? "active" : ""} onClick={() => setActiveTab("form")}>{editingTask ? "Edit Task" : "Add Task"}</button>
          <button className={activeTab === "list" ? "active" : ""} onClick={() => setActiveTab("list")}>Task List ({tasks.length})</button>
          <button className={activeTab === "matrix" ? "active" : ""} onClick={() => setActiveTab("matrix")}>Matrix View</button>
        </nav>
        <main className="main-content">
          {activeTab === "form" && (
            <TaskForm onTaskCreated={handleTaskCreated} editingTask={editingTask} onTaskUpdated={handleTaskUpdated} onCancel={handleCancelEdit} />
          )}
          {activeTab === "list" && (
            <TaskList tasks={tasks} onTaskEdit={handleTaskEdit} onTasksUpdated={handleTasksUpdated} />
          )}
          {activeTab === "matrix" && (
            <EisenhowerMatrix matrixData={matrixData} />
          )}
        </main>
      </div>
  );
}

export default App;
