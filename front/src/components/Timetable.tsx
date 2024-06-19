'use client'

import React, { useEffect, useState } from 'react'
// import { Today } from './Today' // Assuming Today is a component

type Event = {
  id: string
  start: string
  end: string
  type: string
}

type TimeSlotProps = {
  start: string
  end: string
  type: string
}

export default function Timetable() {
  const [schedule, setSchedule] = useState<Event[]>([])

  useEffect(() => {
    const mockData = {
      schedule: [
        {
          type: 'event',
          id: '1',
          summary: 'Event 1',
          description: 'Description for Event 1',
          start: '10:00',
          end: '11:00',
        },
        {
          type: 'free_time',
          id: '2',
          start: '11:00',
          end: '14:00',
        },
        {
          type: 'event',
          id: '3',
          summary: 'Event 2',
          description: 'Description for Event 2',
          start: '14:00',
          end: '16:30',
        },
      ],
    }
    setSchedule(mockData.schedule)
  }, [])

  const hours = Array.from({ length: 16 }, (_, i) => i + 7) // 7시부터 22시까지

  const timeSlots = hours.map(hour => ({
    start: `${hour}:00`,
    end: `${hour + 1}:00`,
    type: 'empty',
  }))

  const mappedSchedule = timeSlots.map(slot => {
    const event = schedule.find(event => {
      const eventStart = parseInt(event.start.split(':')[0])
      const eventEnd = parseInt(event.end.split(':')[0])
      const slotHour = parseInt(slot.start.split(':')[0])

      return slotHour >= eventStart && slotHour < eventEnd
    })

    return event ? { ...slot, ...event } : slot
  })

  return (
    <div className='flex flex-col items-center justify-center'>
      {/* <Today /> */}

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
      className={`w-full border-b border-gray-300 py-2 ${
        type === 'event' ? 'bg-blue-500' : 'bg-gray-200'
      }`}
    >
      {start} - {end}
    </div>
  )
}
