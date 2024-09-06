import React from 'react'

import { getServerSession } from 'next-auth';
import { authOptions } from '@/util/auth';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"

import Login from '@/components/Login';
import Todo from './components/Todo';
import RecentTask from './components/RecentTask';
import Recommended from './components/Recommended';
import Box from '../../components/Box';

export default async function Home() {
  const session = await getServerSession(authOptions);

  return (
    <>
    {session?.error === 'RefreshTokenExpiredError' || !session ? (
      <Box>
        <Login />
      </Box>
    ) : (
      <>
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-center">AI推奨TODOリスト</CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="todo" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="todo">全て</TabsTrigger>
            <TabsTrigger value="recent">直近</TabsTrigger>
            <TabsTrigger value="recommended">AI推奨</TabsTrigger>
          </TabsList>
          <Todo />
          <RecentTask />
          <Recommended />
        </Tabs>
      </CardContent>
    </Card>
    </>
    )}
    </>
  );
}
