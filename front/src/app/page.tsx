import Timetable from '@/components/Timetable'
import Today from '@/components/Today'
import React from 'react'

import getSchedule from '../services/schedule-service'

import { getServerSession } from 'next-auth';
import { authOptions } from './api/auth/[...nextauth]/route'

export default async function Home() {
  const session = await getServerSession(authOptions);
  return (
    <>{session ? (
      <>
      <Today />
      <Timetable datas={session ? await getSchedule() : []}/>
      </>
      ) : null}
    </>
  )
}
