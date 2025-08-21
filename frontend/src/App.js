import React, { useState, useEffect } from "react";
import "./App.css";
import TaskForm from "./components/TaskForm";
import TaskList from "./components/TaskList";
import EisenhowerMatrix from "./components/EisenhowerMatrix";
import { taskService } from "./services/api";

function App() {
  const [tasks, setTasks] = useState([]);
  const [matrixData, setMatrixData] = useState(null);
  const [editingTask, setEditingTask] = useState(null);
  const [activeTab, setActiveTab] = useState("list");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchTasks();
    fetchMatrixData();
  }, []);

  const fetchTasks = async () => {
    try {
      const data = await taskService.getAllTasks();
      setTasks(data.tasks);
      setError("");
    } catch (err) {
      setError("Failed to fetch tasks. Please check if the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const fetchMatrixData = async () => {
    try {
      const data = await taskService.getMatrixData();
      setMatrixData(data);
    } catch (err) {
      console.error("Failed to fetch matrix data:", err);
    }
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
        <div className="loading">Loading tasks...</div>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Eisenhower Matrix Todo App</h1>
        <p>Prioritize your tasks using the Eisenhower Decision Matrix</p>
      </header>

      {error && <div className="error-banner">{error}</div>}

      <nav className="tab-nav">
        <button
          className={activeTab === "form" ? "active" : ""}
          onClick={() => setActiveTab("form")}
        >
          {editingTask ? "Edit Task" : "Add Task"}
        </button>
        <button
          className={activeTab === "list" ? "active" : ""}
          onClick={() => setActiveTab("list")}
        >
          Task List ({tasks.length})
        </button>
        <button
          className={activeTab === "matrix" ? "active" : ""}
          onClick={() => setActiveTab("matrix")}
        >
          Matrix View
        </button>
      </nav>

      <main className="main-content">
        {activeTab === "form" && (
          <TaskForm
            onTaskCreated={handleTaskCreated}
            editingTask={editingTask}
            onTaskUpdated={handleTaskUpdated}
            onCancel={handleCancelEdit}
          />
        )}

        {activeTab === "list" && (
          <TaskList
            tasks={tasks}
            onTaskEdit={handleTaskEdit}
            onTasksUpdated={handleTasksUpdated}
          />
        )}

        {activeTab === "matrix" && (
          <EisenhowerMatrix matrixData={matrixData} />
        )}
      </main>
    </div>
  );
}

export default App;
