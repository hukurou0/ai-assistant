'use client'

import React, { useState } from 'react'
import { Input } from "../../../components/ui/input"
import { Checkbox } from "../../../components/ui/checkbox"
import { Button } from "../../../components/ui/button"
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "../../../components/ui/sheet"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "../../../components/ui/tooltip"
import { TabsContent } from "../../../components/ui/tabs"
import { Trash2, Plus, ListPlus, ListMinus } from "lucide-react"
import AddTaskButton from './AddTaskButton';

import Task from '@/types/Task';

export default function Todo() {
  const [tasks, setTasks] = useState<Task[]>([
    { id: 1, text: "プロジェクト計画を立てる", completed: false, recommended: true, forToday: true, reason: "期限が近づいているため、優先度が高いです。" },
    { id: 2, text: "買い物リストを作成", completed: false, recommended: false, forToday: false },
    { id: 3, text: "ジムに行く", completed: false, recommended: true, forToday: true, reason: "定期的な運動は健康に良いです。今日は時間に余裕がありそうです。" },
    { id: 4, text: "読書をする", completed: false, recommended: true, forToday: false, reason: "最近読書の時間が取れていないようです。今日は良い機会かもしれません。" },
  ]);

  const [newTask, setNewTask] = useState("");
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  const addTask = () => {
    if (newTask.trim() !== "") {
      const newTaskObj: Task = {
        id: Date.now(),
        text: newTask,
        completed: false,
        recommended: false,
        forToday: false,
      };
      setTasks([...tasks, newTaskObj]);
      setNewTask("");
      setIsDrawerOpen(false);
    }
  };

  const toggleTask = (id: number) => {
    setTasks(tasks.map(task =>
      task.id === id ? { ...task, completed: !task.completed } : task
    ));
  };

  const removeTask = (id: number) => {
    setTasks(tasks.filter(task => task.id !== id));
  };

  const toggleForToday = (id: number) => {
    setTasks(tasks.map(task =>
      task.id === id ? { ...task, forToday: !task.forToday } : task
    ));
  };

  return (
    <>
    <TabsContent value="todo">
      <ul className="space-y-2">
        {tasks.map(task => (
          <li key={task.id} className="flex items-center space-x-2">
            <Checkbox
              checked={task.completed}
              onCheckedChange={() => toggleTask(task.id)}
            />
            <span className={`flex-grow ${task.completed ? 'line-through text-gray-500' : ''}`}>
              {task.text}
            </span>
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => toggleForToday(task.id)}
                    className={task.forToday ? 'text-primary' : ''}
                    aria-label={task.forToday ? "今日のタスクから外す" : "今日のタスクに追加"}
                  >
                    {task.forToday ? <ListMinus className="w-4 h-4" /> : <ListPlus className="w-4 h-4" />}
                  </Button>
                </TooltipTrigger>
                <TooltipContent>
                  {task.forToday ? "今日のタスクから外す" : "今日のタスクに追加"}
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
            <Button variant="ghost" size="icon" onClick={() => removeTask(task.id)}>
              <Trash2 className="w-4 h-4" />
            </Button>
          </li>
        ))}
      </ul>
    </TabsContent>
    <AddTaskButton />
    </>
  )
}
