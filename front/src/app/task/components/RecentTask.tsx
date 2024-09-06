'use client'

import React, { useState } from 'react'

import { TabsContent } from "../../../components/ui/tabs"
import { Checkbox } from "../../../components/ui/checkbox"
import { Button } from "../../../components/ui/button"
import { ListMinus } from "lucide-react"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "../../../components/ui/tooltip"
import { Dialog, DialogTrigger } from "../../../components/ui/dialog"
import TaskDialog from './TaskDialog'

import Task from '../../../types/Task';

export default function RecentTask() {
  const [tasks, setTasks] = useState<Task[]>([
    { id: 1, text: "プロジェクト計画を立てる", completed: false, recommended: true, forToday: true, reason: "期限が近づいているため、優先度が高いです。", createdAt: new Date() },
    { id: 2, text: "買い物リストを作成", completed: false, recommended: false, forToday: false, createdAt: new Date() },
    { id: 3, text: "ジムに行く", completed: false, recommended: true, forToday: true, reason: "定期的な運動は健康に良いです。今日は時間に余裕がありそうです。", createdAt: new Date() },
    { id: 4, text: "読書をする", completed: false, recommended: true, forToday: false, reason: "最近読書の時間が取れていないようです。今日は良い機会かもしれません。", createdAt: new Date() },
  ]);
  const todayTasks = tasks.filter(task => task.forToday && !task.completed);

  const toggleTask = (id: number) => {
    setTasks(tasks.map(task =>
      task.id === id ? { ...task, completed: !task.completed } : task
    ));
  };

  const toggleForToday = (id: number) => {
    setTasks(tasks.map(task =>
      task.id === id ? { ...task, forToday: !task.forToday } : task
    ));
  };

  return (
    <TabsContent value="recent">
      {todayTasks.length > 0 ? (
          <ul className="space-y-2">
          {todayTasks.map(task => (
              <li key={task.id} className="flex items-center space-x-2">
              <Checkbox
                  checked={task.completed}
                  onCheckedChange={() => toggleTask(task.id)}
              />
              <Dialog>
                <DialogTrigger asChild>
                  <span 
                    className={`flex-grow cursor-pointer ${task.completed ? 'line-through text-gray-500' : ''}`}
                  >
                    {task.text}
                  </span>
                </DialogTrigger>
                <TaskDialog task={task}/>
              </Dialog>
              <TooltipProvider>
                  <Tooltip>
                  <TooltipTrigger asChild>
                      <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => toggleForToday(task.id)}
                      className="text-primary"
                      aria-label="今日のタスクから外す"
                      >
                      <ListMinus className="w-4 h-4" />
                      </Button>
                  </TooltipTrigger>
                  <TooltipContent>
                      今日のタスクから外す
                  </TooltipContent>
                  </Tooltip>
              </TooltipProvider>
              </li>
          ))}
          </ul>
      ) : (
          <p className="text-center text-muted-foreground">今日のタスクはありません。</p>
      )}
      </TabsContent>
  )
}
