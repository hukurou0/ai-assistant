'use client'

import Event from './Event'
import FreeTime from './FreeTime';

interface EventData {
  type: string,
  id: string,
  now: boolean,
  summary: string,
  time: string,
  description: string,
}

interface FreeTimeData {
  type: string,
  id: string,
  now: boolean,
  time: string,
  selectedTodos: string[],
}

type ScheduleData = EventData | FreeTimeData
type ScheduleDataList = ScheduleData[]

type Props = { //仮の型
  datas: ScheduleDataList
}

export default function Timetable(props: Props) {
  const initialSchedule = [
    {
      type: 'event',
      id: '1',
      now: true,
      summary: 'FastLabel 出勤',
      time: '07:00 - 08:00',
      description: '3件のミーティングと開発',
    },
    {
      type: 'free_time',
      id: '2',
      now: false,
      time: '08:00 - 09:00',
      selectedTodos: ['Individual configuration', 'No setup, or hidden fees'],
    },
    {
      type: 'free_time',
      id: '3',
      now: false,
      time: '08:00 - 09:00',
      selectedTodos: ['Individual configuration', 'No setup, or hidden fees'],
    },
    {
      type: 'free_time',
      id: '4',
      now: false,
      time: '08:00 - 09:00',
      selectedTodos: ['Individual configuration', 'No setup, or hidden fees'],
    },
    {
      type: 'free_time',
      id: '5',
      now: false,
      time: '08:00 - 09:00',
      selectedTodos: ['Individual configuration', 'No setup, or hidden fees'],
    },
  ]

  function isEventData(data: ScheduleData): data is EventData {
    return data.type === 'event';
  }
  
  function isFreeTimeData(data: ScheduleData): data is FreeTimeData {
    return data.type === 'free_time';
  }

  return (
      <ol className="relative border-s border-gray-200 dark:border-gray-700"> 
        {initialSchedule.map((schedule) => {
          if (isEventData(schedule)) {
            return <Event data={schedule} key={schedule.id}/>;
          } else if (isFreeTimeData(schedule)) {
            return <FreeTime data={schedule} key={schedule.id}/>;
          }
        })}              
      </ol>
    )
}
