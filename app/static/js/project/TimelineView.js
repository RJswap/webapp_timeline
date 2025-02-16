import React, { useState, useEffect, useRef } from 'react';
import { ChevronLeft, ChevronRight, ZoomIn, ZoomOut } from 'lucide-react';

const TimelineProject = ({ project, visibleRange, scale, onTaskClick }) => {
    const calculateTaskPosition = (task) => {
      const timelineStart = visibleRange.start.getTime();
      const timelineEnd = visibleRange.end.getTime();
      const duration = timelineEnd - timelineStart;
      
      const taskStart = new Date(task.start_date).getTime();
      const taskEnd = new Date(task.end_date).getTime();
      
      const left = ((taskStart - timelineStart) / duration) * 100;
      const width = ((taskEnd - taskStart) / duration) * 100;
      
      const style = {
        left: `${left}%`,
        width: `${width}%`,
        backgroundColor: task.color // Ajout du style de couleur
      };
      return style;
    };
  
    return (
      <div className="relative h-20 border-b bg-gray-50">
        {project.tasks.map((task, taskIndex) => {
          const position = calculateTaskPosition(task);
          return (
            <div
              key={task.id}
              className="absolute h-12 rounded-lg p-2 text-white text-sm cursor-pointer transition-all hover:-translate-y-0.5"
              style={position}
              onClick={() => onTaskClick(task)}
            >
              <span className="truncate block">{task.text}</span>
              <div className="task-tooltip hidden group-hover:block">
                <span className="dates">{task.dates}</span>
                {task.comment && <span className="comment">{task.comment}</span>}
              </div>
            </div>
          );
        })}
      </div>
    );
  };

const TimelineView = () => {
  const [scale, setScale] = useState('month');
  const [visibleRange, setVisibleRange] = useState({
    start: new Date(2025, 0, 1),
    end: new Date(2026, 0, 1)
  });
  const [projects, setProjects] = useState([]);
  const [visibleProjects, setVisibleProjects] = useState(new Set());
  const timelineRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);
  const [startX, setStartX] = useState(0);
  const [scrollLeft, setScrollLeft] = useState(0);

  useEffect(() => {
    // Récupérer les projets depuis l'API
    const fetchProjects = async () => {
      try {
        const response = await fetch('/project/api/projects');
        const data = await response.json();
        setProjects(data.data.projects);
        setVisibleProjects(new Set(data.data.projects.map(p => p.id)));
      } catch (error) {
        console.error('Error fetching projects:', error);
      }
    };
    fetchProjects();
  }, []);

  const generateTimeColumns = () => {
    const columns = [];
    let current = new Date(visibleRange.start);
    
    while (current < visibleRange.end) {
      if (scale === 'month') {
        columns.push({
          date: new Date(current),
          label: current.toLocaleString('default', { month: 'short', year: '2-digit' })
        });
        current = new Date(current.setMonth(current.getMonth() + 1));
      } else {
        const quarter = Math.floor(current.getMonth() / 3) + 1;
        columns.push({
          date: new Date(current),
          label: `Q${quarter} ${current.getFullYear()}`
        });
        current = new Date(current.setMonth(current.getMonth() + 3));
      }
    }
    return columns;
  };

  const handleMouseDown = (e) => {
    setIsDragging(true);
    setStartX(e.pageX - timelineRef.current.offsetLeft);
    setScrollLeft(timelineRef.current.scrollLeft);
  };

  const handleMouseMove = (e) => {
    if (!isDragging) return;
    e.preventDefault();
    const x = e.pageX - timelineRef.current.offsetLeft;
    const walk = (x - startX) * 2;
    timelineRef.current.scrollLeft = scrollLeft - walk;
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const moveTimeline = (direction) => {
    const monthsToMove = scale === 'month' ? 1 : 3;
    setVisibleRange(prev => ({
      start: new Date(prev.start.setMonth(prev.start.getMonth() + (direction * monthsToMove))),
      end: new Date(prev.end.setMonth(prev.end.getMonth() + (direction * monthsToMove)))
    }));
  };

  return (
    <div className="w-full h-full flex flex-col">
      {/* Controls Bar */}
      <div className="flex items-center justify-between p-4 bg-white border-b">
        <div className="flex items-center gap-2">
          <button 
            className="p-2 rounded hover:bg-gray-100"
            onClick={() => moveTimeline(-1)}
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
          <button 
            className="p-2 rounded hover:bg-gray-100"
            onClick={() => moveTimeline(1)}
          >
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>
        <div className="flex items-center gap-2">
          <button
            className="p-2 rounded hover:bg-gray-100"
            onClick={() => setScale(scale === 'month' ? 'quarter' : 'month')}
          >
            {scale === 'month' ? <ZoomOut className="w-5 h-5" /> : <ZoomIn className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Project List */}
      <div className="flex border-b">
        <div className="w-48 flex-shrink-0 bg-gray-50 border-r p-4">
          <div className="font-semibold">Projets</div>
        </div>
        <div className="flex-grow overflow-x-auto">
          <div className="flex">
            {generateTimeColumns().map((column, index) => (
              <div
                key={index}
                className="flex-shrink-0 p-4 border-r text-center"
                style={{ width: scale === 'month' ? '200px' : '300px' }}
              >
                {column.label}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Timeline Content */}
      <div className="flex-grow flex overflow-hidden">
        {/* Projects List */}
        <div className="w-48 flex-shrink-0 bg-gray-50 border-r">
          {projects.map(project => (
            <div key={project.id} className="p-4 border-b">
              <label className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={visibleProjects.has(project.id)}
                  onChange={(e) => {
                    const newVisible = new Set(visibleProjects);
                    if (e.target.checked) {
                      newVisible.add(project.id);
                    } else {
                      newVisible.delete(project.id);
                    }
                    setVisibleProjects(newVisible);
                  }}
                />
                {project.name}
              </label>
            </div>
          ))}
        </div>

        {/* Timeline Grid */}
        <div 
          className="flex-grow relative overflow-x-auto"
          ref={timelineRef}
          onMouseDown={handleMouseDown}
          onMouseMove={handleMouseMove}
          onMouseUp={handleMouseUp}
          onMouseLeave={handleMouseUp}
        >
          <div className="absolute inset-0">
            {/* Time Grid */}
            <div 
              className="absolute inset-0 grid"
              style={{
                gridTemplateColumns: `repeat(${generateTimeColumns().length}, ${scale === 'month' ? '200px' : '300px'})`
              }}
            >
              {generateTimeColumns().map((_, index) => (
                <div key={index} className="border-r h-full" />
              ))}
            </div>

            {/* Projects and Tasks */}
            {projects
              .filter(p => visibleProjects.has(p.id))
              .map(project => (
                <TimelineProject
                  key={project.id}
                  project={project}
                  visibleRange={visibleRange}
                  scale={scale}
                  onTaskClick={(task) => {
                    // Handler pour l'édition des tâches
                    if (window.ModalManager) {
                      window.ModalManager.openEditTaskModal({
                        id: task.id,
                        projectId: project.id,
                        text: task.text,
                        comment: task.comment,
                        startDate: task.raw_start_date,
                        endDate: task.raw_end_date,
                        etp: task.etp
                      });
                    }
                  }}
                />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TimelineView;