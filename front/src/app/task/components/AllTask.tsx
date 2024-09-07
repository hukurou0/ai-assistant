'use client'

import React from 'react'
import { TabsContent } from "../../../components/ui/tabs"
import AddTaskButton from './AddTaskButton';

import TaskItem from './TaskItem';
import { TaskStore } from '../task-store'

export default function AllTask() {
  const taskStore = TaskStore.useContainer();

  return (
    <>
    <TabsContent value="todo">
      <ul className="space-y-2">
        {taskStore.tasks.map((task, index) => (
          <TaskItem key={index} task={task} />
        ))}
      </ul>
      <div className="mb-[3rem]"></div>
    </TabsContent>
    <AddTaskButton />
    </>
  )
}
