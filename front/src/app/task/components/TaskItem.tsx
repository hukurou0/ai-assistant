import React, { useState } from 'react'

import { Button } from "../../../components/ui/button"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "../../../components/ui/tooltip"
import { Dialog, DialogTrigger } from "../../../components/ui/dialog"
import { Badge } from "../../../components/ui/badge"
import { Trash2, Star, StarOff, Tag } from "lucide-react"
import TaskDialog from './TaskDialog';

import { TaskStore } from '../task-store'
import Task from '../../../types/Task'
import { Checkbox } from '@/components/ui/checkbox'

export default function TaskItem(props: {task:Task}) {
  const taskStore = TaskStore.useContainer();
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  return (
    <li key={props.task.id} className="flex flex-col space-y-2 py-2">
      <div className="flex items-center space-x-2">
      <Checkbox
                  checked={props.task.completed}
                  onCheckedChange={() => taskStore.toggleTask(props.task.id)}
       />
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogTrigger asChild>
          <span 
            className={`flex-grow cursor-pointer ${props.task.completed ? 'line-through text-gray-500' : ''}`}
          >
            {props.task.text}
          </span>
        </DialogTrigger>
        <TaskDialog task={props.task} dialogOpen={setIsDialogOpen}/>
      </Dialog>
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild>
            <Button
            variant="ghost"
            size="sm"
            onClick={() => taskStore.togglePriority(props.task.id)}
            className={props.task.priority ? 'text-yellow-600 fill-current' : 'text-muted-foreground'}
            aria-label={props.task.priority ? "優先タスクから外す" : "優先タスクに追加"}
          >
              {props.task.priority ? <Star className="w-4 h-4" /> : <StarOff className="w-4 h-4" />}
            </Button>
          </TooltipTrigger>
          <TooltipContent>
            {props.task.priority ? "優先のタスクから外す" : "優先のタスクに追加"}
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
      <Button variant="ghost" size="icon" onClick={() => taskStore.deleteTask(props.task.id)}>
        <Trash2 className="w-4 h-4" />
      </Button>
      </div>
      <div className="flex items-center space-x-2 ml-6">
          <Tag className="w-4 h-4 text-muted-foreground" />
          <Badge variant="secondary" className="text-xs">
            {props.task.tag}
          </Badge>
        </div>
    </li>
  )
}
