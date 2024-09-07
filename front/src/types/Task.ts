type Task = {
    id: number;
    text: string;
    completed: boolean;
    recommended: boolean;
    priority: boolean;
    reason?: string;
    createdAt: Date;
    tag: string;
  }

export default Task;