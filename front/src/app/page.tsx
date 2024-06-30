import Timetable from '@/components/Timetable'
import Today from '@/components/Today'
import React from 'react'

import getSchedule from '../services/schedule-service'

export default async function Home() { 
  return (
    <>
      <Today />
      <Timetable datas={await getSchedule()}/>
    </>
  )
}
