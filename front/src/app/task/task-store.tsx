'use client'

import Task from "@/types/Task";
import { useState } from "react";
import { createContainer } from "unstated-next";
import { TagOption } from '@/types/Tag';

export const useTaskStore = () => {
    const [tasks, setTasks] = useState<Task[]>([
        { id: 1, text: "プロジェクト計画を立てる", completed: false, recommended: true, priority: true, reason: "期限が近づいているため、優先度が高いです。", createdAt: new Date(), tag: "仕事" },
        { id: 2, text: "買い物リストを作成", completed: false, recommended: false, priority: false, createdAt: new Date(), tag: "個人" },
        { id: 3, text: "ジムに行く", completed: false, recommended: true, priority: true, reason: "定期的な運動は健康に良いです。今日は時間に余裕がありそうです。", createdAt: new Date(), tag: "健康" },
        { id: 4, text: "読書をする", completed: false, recommended: true, priority: false, reason: "最近読書の時間が取れていないようです。今日は良い機会かもしれません。", createdAt: new Date(), tag: "自己啓発" },
      ]);

    const toggleTask = (id: number) => {
      setTasks(tasks.map(task =>
        task.id === id ? { ...task, completed: !task.completed } : task
      ));
    };
  
    const togglePriority = (id: number) => {
      setTasks(tasks.map(task =>
        task.id === id ? { ...task, priority: !task.priority } : task
      ));
    };

    const addTask = (newTask:string, isNewTaskpriority:boolean, newTaskTag:TagOption) => {
      if (newTask.trim() !== "") {
        const newTaskObj: Task = {
          id: Date.now(),
          text: newTask,
          completed: false,
          recommended: false,
          priority: isNewTaskpriority,
          createdAt: new Date(),
          tag: newTaskTag,
        };
        setTasks([...tasks, newTaskObj]);
      };
    }

    const deleteTask = (id: number) => {
      setTasks(tasks.filter(task => task.id !== id));
    }

    const saveTaskChanges = (task: Task) => {
      setTasks(tasks.map(t =>
        t.id === task.id ? task : t
      ));
    }

    return {
        tasks,
        setTasks,
        toggleTask,
        togglePriority,
        addTask,
        deleteTask,
        saveTaskChanges
    };
}

export const TaskStore = createContainer(useTaskStore);