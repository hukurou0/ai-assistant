'use client'

import React, { useState } from 'react'

import { Switch } from "../../../components/ui/switch"
import { Label } from "../../../components/ui/label"
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "../../../components/ui/sheet"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../../../components/ui/select"
import { Button } from "../../../components/ui/button"
import { Input } from "../../../components/ui/input"
import { Plus } from "lucide-react"

import { TaskStore } from '../task-store'
import { TagOption, tagOptions } from '../../../types/Tag';

export default function AddTaskButton() {
  const taskStore = TaskStore.useContainer();
  const [newTask, setNewTask] = useState("");
  const [isNewTaskpriority, setIsNewTaskpriority] = useState(false);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [newTaskTag, setNewTaskTag] = useState<TagOption>("その他");

  const addTask = () => {
    taskStore.addTask(newTask, isNewTaskpriority, newTaskTag);
    setNewTask("");
    setNewTaskTag("その他");
    setIsNewTaskpriority(false);
    setIsDrawerOpen(false);
  }

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
            <div>
              <Label htmlFor="new-task" className="block mb-2">
                タスク内容
              </Label>
              <Input
                id="new-task"
                placeholder="タスクを入力"
                value={newTask}
                onChange={(e) => setNewTask(e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="new-task-tag" className="block mb-2">
                タグ設定
              </Label>
              <Select
                value={newTaskTag}
                onValueChange={(value: TagOption) => setNewTaskTag(value)}
              >
                <SelectTrigger id="new-task-tag">
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
              <p className="text-sm text-muted-foreground mt-1">
                タスクの分類に役立つタグを選択してください。
              </p>
            </div>
            <div className="flex items-center space-x-2">
              <Switch
                id="today-task"
                checked={isNewTaskpriority}
                onCheckedChange={setIsNewTaskpriority}
              />
              <Label htmlFor="today-task">優先のタスクに追加</Label>
            </div>
            <Button onClick={addTask}>タスクを追加</Button>
          </div>
        </SheetContent>
      </Sheet>
  )
}
