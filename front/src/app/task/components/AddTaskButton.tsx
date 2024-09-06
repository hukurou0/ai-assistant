'use client'

import React, { useState } from 'react'

import { Switch } from "../../../components/ui/switch"
import { Label } from "../../../components/ui/label"
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "../../../components/ui/sheet"
import { Button } from "../../../components/ui/button"
import { Input } from "../../../components/ui/input"
import { Plus } from "lucide-react"

import Task from '../../../types/Task';

export default function AddTaskButton() {
  const [tasks, setTasks] = useState<Task[]>([
    { id: 1, text: "プロジェクト計画を立てる", completed: false, recommended: true, forToday: true, reason: "期限が近づいているため、優先度が高いです。", createdAt: new Date() },
    { id: 2, text: "買い物リストを作成", completed: false, recommended: false, forToday: false, createdAt: new Date() },
    { id: 3, text: "ジムに行く", completed: false, recommended: true, forToday: true, reason: "定期的な運動は健康に良いです。今日は時間に余裕がありそうです。", createdAt: new Date() },
    { id: 4, text: "読書をする", completed: false, recommended: true, forToday: false, reason: "最近読書の時間が取れていないようです。今日は良い機会かもしれません。", createdAt: new Date() },
  ]);
  const [newTask, setNewTask] = useState("");
  const [isNewTaskForToday, setIsNewTaskForToday] = useState(false);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  const addTask = () => {
    if (newTask.trim() !== "") {
      const newTaskObj: Task = {
        id: Date.now(),
        text: newTask,
        completed: false,
        recommended: false,
        forToday: isNewTaskForToday,
        createdAt: new Date(),
      };
      setTasks([...tasks, newTaskObj]);
      setNewTask("");
      setIsNewTaskForToday(false);
      setIsDrawerOpen(false);
    }
  };

  return (
    <Sheet open={isDrawerOpen} onOpenChange={setIsDrawerOpen}>
        <SheetTrigger asChild>
          <Button
            className="fixed bottom-[4.7rem] right-4 w-14 h-14 rounded-full shadow-lg hover:shadow-xl transition-shadow duration-300 flex items-center justify-center"
            size="icon"
            aria-label="新しいタスクを追加"
          >
            <Plus className="w-6 h-6" />
          </Button>
        </SheetTrigger>
        <SheetContent>
          <SheetHeader>
            <SheetTitle>新しいタスクを追加</SheetTitle>
            <SheetDescription>
              新しいタスクの詳細を入力してください。
            </SheetDescription>
          </SheetHeader>
          <div className="grid gap-4 py-4">
            <Input
              placeholder="タスクを入力"
              value={newTask}
              onChange={(e) => setNewTask(e.target.value)}
            />
            <div className="flex items-center space-x-2">
              <Switch
                id="today-task"
                checked={isNewTaskForToday}
                onCheckedChange={setIsNewTaskForToday}
              />
              <Label htmlFor="today-task">今日のタスクに追加</Label>
            </div>
            <Button onClick={addTask}>タスクを追加</Button>
          </div>
        </SheetContent>
      </Sheet>
  )
}
