import React from "react";
import { taskService } from "../services/api";

const TaskList = ({ tasks, onTaskEdit, onTasksUpdated }) => {
  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this task?")) {
      try {
        await taskService.deleteTask(id);
        onTasksUpdated();
      } catch (error) {
        alert("Failed to delete task. Please try again.");
      }
    }
  };

  const getPriorityColor = (score) => {
    if (score >= 80) return "#ff4757"; // High priority - red
    if (score >= 60) return "#ffa726"; // Medium-high priority - orange
    if (score >= 40) return "#ffeb3b"; // Medium priority - yellow
    return "#4caf50"; // Low priority - green
  };

  const getQuadrantLabel = (urgency, importance) => {
    if (urgency >= 6 && importance >= 6) return "Do First";
    if (urgency < 6 && importance >= 6) return "Schedule";
    if (urgency >= 6 && importance < 6) return "Delegate";
    return "Eliminate";
  };

  if (tasks.length === 0) {
    return (
      <div className="task-list empty">
        <p>No tasks yet. Add your first task above!</p>
      </div>
    );
  }

  return (
    <div className="task-list">
      <h3>Your Tasks (Ranked by Priority)</h3>
      <div className="tasks">
        {tasks.map((task, index) => (
          <div key={task.id} className="task-item">
            <div className="task-header">
              <div className="task-rank">#{index + 1}</div>
              <div 
                className="priority-indicator"
                style={{ backgroundColor: getPriorityColor(task.priority_score) }}
              >
                {task.priority_score}
              </div>
            </div>
            
            <div className="task-content">
              <h4>{task.title}</h4>
              {task.description && <p>{task.description}</p>}
              
              <div className="task-metrics">
                {[["Urgency", task.urgency],["Importance", task.importance],["Impact", task.impact],["Value", task.value_alignment],["Effort", task.effort]].map(([label,val]) => (
                  <div className="metric" key={label}>
                    <span className="label">{label}:</span>
                    <span className="value">{val ?? '-'} /10</span>
                  </div>
                ))}
                {task.due_date && (
                  <div className="metric">
                    <span className="label">Due:</span>
                    <span className="value">{new Date(task.due_date).toLocaleString()}</span>
                  </div>
                )}
                <div className="metric">
                  <span className="label">Quadrant:</span>
                  <span className="value">{getQuadrantLabel(task.urgency, task.importance)}</span>
                </div>
              </div>
            </div>
            
            <div className="task-actions">
              <button onClick={() => onTaskEdit(task)} className="edit-btn">
                Edit
              </button>
              <button onClick={() => handleDelete(task.id)} className="delete-btn">
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TaskList;
