import React from "react";

const EisenhowerMatrix = ({ matrixData }) => {
  const quadrants = [
    {
      key: "quadrant_1",
      title: "Do First",
      subtitle: "Urgent + Important",
      color: "#ff4757",
      tasks: matrixData?.quadrant_1 || [],
    },
    {
      key: "quadrant_2",
      title: "Schedule",
      subtitle: "Important + Not Urgent",
      color: "#ffa726",
      tasks: matrixData?.quadrant_2 || [],
    },
    {
      key: "quadrant_3",
      title: "Delegate",
      subtitle: "Urgent + Not Important",
      color: "#ffeb3b",
      tasks: matrixData?.quadrant_3 || [],
    },
    {
      key: "quadrant_4",
      title: "Eliminate",
      subtitle: "Not Urgent + Not Important",
      color: "#4caf50",
      tasks: matrixData?.quadrant_4 || [],
    },
  ];

  return (
    <div className="eisenhower-matrix">
      <h3>Eisenhower Matrix</h3>
      
      <div className="matrix-labels">
        <div className="y-axis-label">Important</div>
        <div className="x-axis-label">Urgent</div>
      </div>
      
      <div className="matrix-grid">
        {quadrants.map((quadrant) => (
          <div
            key={quadrant.key}
            className="quadrant"
            style={{ borderColor: quadrant.color }}
          >
            <div 
              className="quadrant-header"
              style={{ backgroundColor: quadrant.color }}
            >
              <h4>{quadrant.title}</h4>
              <p>{quadrant.subtitle}</p>
              <span className="task-count">({quadrant.tasks.length} tasks)</span>
            </div>
            
            <div className="quadrant-tasks">
              {quadrant.tasks.length === 0 ? (
                <p className="no-tasks">No tasks in this quadrant</p>
              ) : (
                quadrant.tasks.map((task) => (
                  <div key={task.id} className="matrix-task">
                    <div className="task-title">{task.title}</div>
                    <div className="task-score">{task.priority_score}</div>
                    <div className="mini-metrics">
                      U{task.urgency} I{task.importance} Im{task.impact ?? '-'} V{task.value_alignment ?? '-'} E{task.effort ?? '-'}
                    </div>
                    {task.due_date && (
                      <div className="mini-due">Due: {new Date(task.due_date).toLocaleDateString()}</div>
                    )}
                  </div>
                ))
              )}
            </div>
          </div>
        ))}
      </div>
      
      <div className="matrix-legend">
        <div className="legend-item">
          <strong>Do First:</strong> Urgent and important tasks that need immediate attention
        </div>
        <div className="legend-item">
          <strong>Schedule:</strong> Important but not urgent tasks to plan for
        </div>
        <div className="legend-item">
          <strong>Delegate:</strong> Urgent but not important tasks to assign to others
        </div>
        <div className="legend-item">
          <strong>Eliminate:</strong> Neither urgent nor important tasks to remove
        </div>
      </div>
    </div>
  );
};

export default EisenhowerMatrix;
