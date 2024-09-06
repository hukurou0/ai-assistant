import React from 'react'

import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "../../../components/ui/dialog"
import { Checkbox } from "../../../components/ui/checkbox"
import { Input } from "../../../components/ui/input"
import { Label } from "../../../components/ui/label"
import { Switch } from "../../../components/ui/switch"
import { Calendar, Clock } from "lucide-react"

import Task from '../../../types/Task';

export default function TaskDialog(props: { task:Task }) {
  const updateTaskText = (id: number, text: string) => {
    // Update task text
  };
  const toggleTask = (id: number) => {
    // Toggle task completion status
  };
  const toggleForToday = (id: number) => {
    // Toggle task forToday status
  };
  return (
        <DialogContent className="w-full max-w-[90%] md:max-w-[600px]">
          <DialogHeader>
            <DialogTitle>タスクの詳細</DialogTitle>
            <DialogDescription>
              タスクの詳細情報を確認・編集できます。
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="task-text" className="text-right">
                タスク
              </Label>
              <Input
                id="task-text"
                value={props.task.text}
                onChange={(e) => updateTaskText(props.task.id, e.target.value)}
                className="col-span-3"
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label className="text-right">状態</Label>
              <div className="col-span-3">
                <Checkbox
                  checked={props.task.completed}
                  onCheckedChange={() => toggleTask(props.task.id)}
                />
                <span className="ml-2">{props.task.completed ? '完了' : '未完了'}</span>
              </div>
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label className="text-right">今日のタスク</Label>
              <div className="col-span-3">
                <Switch
                  checked={props.task.forToday}
                  onCheckedChange={() => toggleForToday(props.task.id)}
                />
              </div>
            </div>
            {props.task.recommended && (
              <div className="grid grid-cols-4 items-center gap-4">
                <Label className="text-right">推奨理由</Label>
                <p className="col-span-3 text-sm text-muted-foreground">{props.task.reason}</p>
              </div>
            )}
            <div className="grid grid-cols-4 items-center gap-4">
              <Label className="text-right">作成日時</Label>
              <div className="col-span-3 flex items-center space-x-2">
                <Calendar className="w-4 h-4" />
                <span>{props.task.createdAt.toLocaleDateString()}</span>
                <Clock className="w-4 h-4 ml-2" />
                <span>{props.task.createdAt.toLocaleTimeString()}</span>
              </div>
            </div>
          </div>
        </DialogContent>
  )
}
