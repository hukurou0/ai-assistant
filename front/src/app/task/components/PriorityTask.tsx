'use client'

import React, { useState } from 'react'

import { TabsContent } from "../../../components/ui/tabs"

import { TaskStore } from '../task-store'
import TaskItem from './TaskItem'

export default function PriorityTask() {
  const taskStore = TaskStore.useContainer();
  const priorityTasks = taskStore.tasks.filter(task => task.priority && !task.completed);

  return (
    <>
    <TabsContent value="recent">
      {priorityTasks.length > 0 ? (
        <>
        <ul className="space-y-2">
          {priorityTasks.map((task, index) => (
            <TaskItem key={index} task={task} />
          ))}
        </ul>
        <div className="mb-[3rem]"></div>
        </>
      ) : (
        <p className="text-center text-muted-foreground">優先のタスクはありません。</p>
      )}
    </TabsContent>
    </>
  )
}
