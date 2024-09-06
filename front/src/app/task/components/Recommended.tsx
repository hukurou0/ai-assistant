'use client'

import React, { useState } from 'react'

import { Button } from "../../../components/ui/button"
import { TabsContent } from "../../../components/ui/tabs"
import { Sparkles, ListPlus, ListMinus } from "lucide-react"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "../../../components/ui/tooltip"
import { Dialog, DialogTrigger } from "../../../components/ui/dialog"
import TaskDialog from './TaskDialog'

import Task from '@/types/Task';

export default function Recommended() {
  const [tasks, setTasks] = useState<Task[]>([
    { id: 1, text: "プロジェクト計画を立てる", completed: false, recommended: true, forToday: true, reason: "期限が近づいているため、優先度が高いです。", createdAt: new Date() },
    { id: 2, text: "買い物リストを作成", completed: false, recommended: false, forToday: false, createdAt: new Date() },
    { id: 3, text: "ジムに行く", completed: false, recommended: true, forToday: true, reason: "定期的な運動は健康に良いです。今日は時間に余裕がありそうです。", createdAt: new Date() },
    { id: 4, text: "読書をする", completed: false, recommended: true, forToday: false, reason: "最近読書の時間が取れていないようです。今日は良い機会かもしれません。", createdAt: new Date() },
  ]);

  const recommendedTasks = tasks.filter(task => task.recommended && !task.completed);

  const toggleForToday = (id: number) => {
    setTasks(tasks.map(task =>
      task.id === id ? { ...task, forToday: !task.forToday } : task
    ));
  };
  return (
    <TabsContent value="recommended">
      {recommendedTasks.length > 0 ? (
        <ul className="space-y-4">
          {recommendedTasks.map(task => (
            <li key={task.id} className="bg-secondary p-4 rounded-lg">
              <div className="flex items-center space-x-2 mb-2">
                <Sparkles className="w-5 h-5 text-primary" />
                <Dialog>
                  <DialogTrigger asChild>
                    <span className="font-semibold">{task.text}</span>
                  </DialogTrigger>
                  <TaskDialog task={task}/>
                </Dialog>
                
              </div>
              <p className="text-sm text-muted-foreground">{task.reason}</p>
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => toggleForToday(task.id)}
                      className={task.forToday ? 'text-primary' : ''}
                      aria-label={task.forToday ? "直近のタスクから外す" : "直近のタスクに追加"}
                    >
                      {task.forToday ? <ListMinus className="w-4 h-4 mr-2" /> : <ListPlus className="w-4 h-4 mr-2" />}
                      {task.forToday ? '直近のタスクから外す' : '直近のタスクに追加'}
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>
                    {task.forToday ? "直近のタスクから外す" : "直近のタスクに追加"}
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-center text-muted-foreground">現在、AIによる推奨タスクはありません。</p>
      )}
    </TabsContent>
  )
}
