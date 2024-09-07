import React, { useState } from 'react'

import { DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogFooter } from "../../../components/ui/dialog"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../../../components/ui/select"
import { Button } from "@/components/ui/button"
import { Checkbox } from "../../../components/ui/checkbox"
import { Input } from "../../../components/ui/input"
import { Label } from "../../../components/ui/label"
import { Switch } from "../../../components/ui/switch"
import { Calendar, Clock, Save } from "lucide-react"

import Task from '../../../types/Task';
import { TaskStore } from '../task-store'
import { TagOption, tagOptions } from '../../../types/Tag';

export default function TaskDialog(props: { task: Task, dialogOpen: (open: boolean) => void }) {
  const [task, setTask] = useState(props.task);
  const taskStore = TaskStore.useContainer();

  const updateTaskText = (id: number, text: string) => {
    setTask((prevTask) => ({ ...prevTask, text }));
  };

  const toggleTask = (id: number) => {
    setTask((prevTask) => ({ ...prevTask, completed: !prevTask.completed }));
  };

  const togglePriority = (id: number) => {
    setTask((prevTask) => ({ ...prevTask, priority: !prevTask.priority }));
  };

  const updateTaskTag = (id: number, tag: TagOption) => {
    setTask((prevTask) => ({ ...prevTask, tag }));
  };

  const saveTaskChanges = () => {
    taskStore.saveTaskChanges(task);
    props.dialogOpen(false);
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
            value={task.text}
            onChange={(e) => updateTaskText(task.id, e.target.value)}
            className="col-span-3"
          />
        </div>
        <div className="grid grid-cols-4 items-center gap-4">
          <Label htmlFor="task-tag" className="text-right">
            タグ
          </Label>
          <Select
            value={task.tag}
            onValueChange={(value: TagOption) => updateTaskTag(task.id, value)}
          >
            <SelectTrigger className="col-span-3">
              <SelectValue placeholder="タグを選択" />
            </SelectTrigger>
            <SelectContent>
              {tagOptions.map((tag) => (
                <SelectItem key={tag} value={tag}>
                  {tag}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <div className="grid grid-cols-4 items-center gap-4">
          <Label className="text-right">状態</Label>
          <div className="col-span-3">
            <Checkbox
              checked={task.completed}
              onCheckedChange={() => toggleTask(task.id)}
            />
            <span className="ml-2">{task.completed ? '完了' : '未完了'}</span>
          </div>
        </div>
        <div className="grid grid-cols-4 items-center gap-4">
          <Label className="text-right">優先のタスク</Label>
          <div className="col-span-3">
            <Switch
              checked={task.priority}
              onCheckedChange={() => togglePriority(task.id)}
            />
          </div>
        </div>
        {task.recommended && (
          <div className="grid grid-cols-4 items-center gap-4">
            <Label className="text-right">推奨理由</Label>
            <p className="col-span-3 text-sm text-muted-foreground">{task.reason}</p>
          </div>
        )}
        <div className="grid grid-cols-4 items-center gap-4">
          <Label className="text-right">作成日時</Label>
          <div className="col-span-3 flex items-center space-x-2">
            <Calendar className="w-4 h-4" />
            <span>{task.createdAt.toLocaleDateString()}</span>
            <Clock className="w-4 h-4 ml-2" />
            <span>{task.createdAt.toLocaleTimeString()}</span>
          </div>
        </div>
      </div>
      <DialogFooter>
        <Button onClick={saveTaskChanges} className="w-full">
          <Save className="w-4 h-4 mr-2" />
          保存
        </Button>
      </DialogFooter>
    </DialogContent>
  );
}
