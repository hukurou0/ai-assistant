'use client'

import { useEffect, useState } from 'react'
import data from '../../data/mock.json'

type Event = {
  type: string
  id: string
  summary?: string
  description?: string
  start: string
  end: string
}

type TimeSlotProps = {
  start: string
  end: string
  type?: string
}

export default function Timetable() {
  const [schedule, setSchedule] = useState<Event[]>([])

  useEffect(() => {
    setSchedule(data)
  }, [])

  const hours = Array.from({ length: 16 }, (v, i) => ({
    start: `${(i + 7).toString().padStart(2, '0')}:00`,
    end: `${(i + 8).toString().padStart(2, '0')}:00`,
    type: 'free_time',
  }))

  const mappedSchedule = hours.map(hour => {
    const event = schedule.find(event => {
      const eventStart = parseInt(event.start.split(':')[0])
      const eventEnd = parseInt(event.end.split(':')[0])
      const hourStart = parseInt(hour.start.split(':')[0])

      return hourStart >= eventStart && hourStart < eventEnd
    })

    return event ? { ...hour, type: event.type } : hour
  })

  return (
    <div className='flex flex-col items-center justify-center'>
      {mappedSchedule.map((item, index) => (
        <TimeSlot
          key={index}
          start={item.start}
          end={item.end}
          type={item.type}
        />
      ))}
    </div>
  )
}
function TimeSlot({ start, end, type }: TimeSlotProps) {
  return (
    <div
      className={`w-full border-b border-gray-300 py-2 h-24 ${
        type === 'event' ? 'bg-blue-500' : 'bg-white-100'
      }`}
    >
      <p className='text-xl'>{start}</p>
    </div>
  )
}
