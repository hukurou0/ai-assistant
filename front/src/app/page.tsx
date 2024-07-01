'use client'

import Timetable from '@/components/Timetable'
import Today from '@/components/Today'
import React from 'react'

import getSchedule from '../services/schedule-service'

import { useSession } from "next-auth/react"
import { Session } from 'next-auth';

declare module 'next-auth' {
  interface Session {
    accessToken?: string;
  }
}

export default async function Home() { 
  const { data } = useSession() || {}
  return (
    <>
      <Today />
      <Timetable datas={data ? await getSchedule(data) : []}/>
    </>
  )
}
