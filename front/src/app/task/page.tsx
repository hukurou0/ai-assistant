'use client'

import React from 'react'

import { useSession } from "next-auth/react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"

import Login from '@/components/Login';
import AllTask from './components/AllTask';
import PriorityTask from './components/PriorityTask';
import Recommended from './components/Recommended';
import Box from '../../components/Box';

import { TaskStore } from './task-store'

export default function Home() {
  const { data: session } = useSession();

  return (
    <>
    {false ? (
      <Box>
        <Login />
      </Box>
    ) : (
      <>
        <TaskStore.Provider>
          <Card className="w-full max-w-2xl mx-auto">
            <CardHeader>
              <CardTitle className="text-2xl font-bold text-center">AI推奨TODOリスト</CardTitle>
            </CardHeader>
            <CardContent>
              <Tabs defaultValue="todo" className="w-full">
                <TabsList className="grid w-full grid-cols-3">
                  <TabsTrigger value="todo">全て</TabsTrigger>
                  <TabsTrigger value="recent">優先</TabsTrigger>
                  <TabsTrigger value="recommended">AI推奨</TabsTrigger>
                </TabsList>
                <AllTask />
                <PriorityTask />
                <Recommended />
              </Tabs>
            </CardContent>
          </Card>
        </TaskStore.Provider>
    </>
    )}
    </>
  );
}
