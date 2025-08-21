import React, { useState } from "react";
import { taskService } from "../services/api";

const TaskForm = ({ onTaskCreated, editingTask, onTaskUpdated, onCancel }) => {
  const [task, setTask] = useState({
    title: editingTask?.title || "",
    description: editingTask?.description || "",
    urgency: editingTask?.urgency || 5,
    importance: editingTask?.importance || 5,
    impact: editingTask?.impact || 5,
    value_alignment: editingTask?.value_alignment || 5,
    effort: editingTask?.effort || 5,
    due_date: editingTask?.due_date ? editingTask.due_date.slice(0,16) : "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      if (editingTask) {
        const updatedTask = await taskService.updateTask(editingTask.id, task);
        onTaskUpdated(updatedTask);
      } else {
  const payload = { ...task, due_date: task.due_date ? new Date(task.due_date).toISOString() : null };
  const newTask = await taskService.createTask(payload);
        onTaskCreated(newTask);
  setTask({ title: "", description: "", urgency: 5, importance: 5, impact:5, value_alignment:5, effort:5, due_date: "" });
      }
    } catch (err) {
      setError("Failed to save task. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    const numeric = ["urgency","importance","impact","value_alignment","effort"];
    setTask((prev) => ({
      ...prev,
      [name]: numeric.includes(name) ? parseInt(value) : value,
    }));
  };

  return (
    <div className="task-form">
      <h3>{editingTask ? "Edit Task" : "Add New Task"}</h3>
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Task Title *</label>
          <input
            type="text"
            id="title"
            name="title"
            value={task.title}
            onChange={handleChange}
            required
            maxLength="200"
            placeholder="Enter task title"
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            name="description"
            value={task.description}
            onChange={handleChange}
            placeholder="Enter task description (optional)"
            rows="3"
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="urgency">
              Urgency: {task.urgency}/10
            </label>
            <input
              type="range"
              id="urgency"
              name="urgency"
              min="1"
              max="10"
              value={task.urgency}
              onChange={handleChange}
            />
            <div className="scale-labels">
              <span>Not Urgent</span>
              <span>Very Urgent</span>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="importance">
              Importance: {task.importance}/10
            </label>
            <input
              type="range"
              id="importance"
              name="importance"
              min="1"
              max="10"
              value={task.importance}
              onChange={handleChange}
            />
            <div className="scale-labels">
              <span>Not Important</span>
              <span>Very Important</span>
            </div>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="impact">Impact: {task.impact}/10</label>
            <input type="range" id="impact" name="impact" min="1" max="10" value={task.impact} onChange={handleChange} />
            <div className="scale-labels"><span>Low</span><span>High</span></div>
          </div>
          <div className="form-group">
            <label htmlFor="value_alignment">Value Alignment: {task.value_alignment}/10</label>
            <input type="range" id="value_alignment" name="value_alignment" min="1" max="10" value={task.value_alignment} onChange={handleChange} />
            <div className="scale-labels"><span>Low</span><span>High</span></div>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="effort">Effort (Cost): {task.effort}/10</label>
            <input type="range" id="effort" name="effort" min="1" max="10" value={task.effort} onChange={handleChange} />
            <div className="scale-labels"><span>Low</span><span>High</span></div>
          </div>
          <div className="form-group">
            <label htmlFor="due_date">Due Date</label>
            <input type="datetime-local" id="due_date" name="due_date" value={task.due_date} onChange={handleChange} />
          </div>
        </div>

        <div className="form-actions">
          <button type="submit" disabled={loading || !task.title.trim()}>
            {loading ? "Saving..." : editingTask ? "Update Task" : "Add Task"}
          </button>
          {editingTask && (
            <button type="button" onClick={onCancel}>
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default TaskForm;
