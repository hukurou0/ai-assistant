type Task = {
    id: number;
    text: string;
    completed: boolean;
    recommended: boolean;
    forToday: boolean;
    reason?: string;
  }

export default Task;