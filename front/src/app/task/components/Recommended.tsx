'use client'

import React, { useState } from 'react'

import { Button } from "../../../components/ui/button"
import { TabsContent } from "../../../components/ui/tabs"
import { Sparkles, ListPlus, ListMinus, Tag } from "lucide-react"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "../../../components/ui/tooltip"
import { Dialog, DialogTrigger } from "../../../components/ui/dialog"
import { Badge } from "../../../components/ui/badge"
import TaskDialog from './TaskDialog'

import { TaskStore } from '../task-store'

export default function Recommended() {
  const taskStore = TaskStore.useContainer();
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const recommendedTasks = taskStore.tasks.filter(task => task.recommended && !task.completed);

  return (
    <TabsContent value="recommended">
      {recommendedTasks.length > 0 ? (
        <>
        <ul className="space-y-4">
          {recommendedTasks.map(task => (
            <li key={task.id} className="bg-secondary p-4 rounded-lg">
              <div className="flex items-center space-x-2 mb-2">
                <Sparkles className="w-5 h-5 text-primary" />
                <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                  <DialogTrigger asChild>
                    <span className="font-semibold">{task.text}</span>
                  </DialogTrigger>
                  <TaskDialog task={task} dialogOpen={setIsDialogOpen} />
                </Dialog>
                
              </div>
              <div className="flex items-center space-x-2 mb-2">
                <Tag className="w-4 h-4 text-muted-foreground" />
                <Badge variant="secondary" className="text-xs">
                  {task.tag}
                </Badge>
              </div>
              <p className="text-sm text-muted-foreground">{task.reason}</p>
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => taskStore.togglePriority(task.id)}
                      className={task.priority ? 'text-primary' : ''}
                      aria-label={task.priority ? "優先のタスクから外す" : "優先のタスクに追加"}
                    >
                      {task.priority ? <ListMinus className="w-4 h-4 mr-2" /> : <ListPlus className="w-4 h-4 mr-2" />}
                      {task.priority ? '優先のタスクから外す' : '優先のタスクに追加'}
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>
                    {task.priority ? "優先のタスクから外す" : "優先のタスクに追加"}
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
            </li>
          ))}
        </ul>
        <div className="mb-[3rem]"></div>
        </>
      ) : (
        <p className="text-center text-muted-foreground">現在、AIによる推奨タスクはありません。</p>
      )}
    </TabsContent>
  )
}
