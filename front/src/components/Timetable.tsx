'use client'

import { useEffect, useState } from 'react'
import { TimeSlot } from './TimetableSlot'
import data from '../../data/mock.json'
import suggest from '../../data/mock_suggest.json'

type Event = {
  type: string
  id: string
  description?: string
  summary?: string
  start: string
  end: string
}

type Props = { //仮の型
  datas: Event[]
}

export default function Timetable(props: Props) {
  const [schedule, setSchedule] = useState<Event[]>([])
  const [isModalOpen, setIsModalOpen] = useState(false)

  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null)
  const [suggestions, setSuggestions] = useState([])

  useEffect(() => {
    setSchedule(data)
  }, [])

  const { suggest_todos } = suggest
  //console.log(suggest)
  //console.log(data)

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

    if (event) {
      return {
        ...hour,
        type: event.type,
        description: event.description,
        summary: event.summary || 'Free time',
      }
    } else {
      // 프리타임인 경우, suggest_todos에서 랜덤하게 선택하여 표시
      const suggestions = suggest_todos
        .map(todo => `${todo.title}: ${todo.notes}`)
        .join(', ')

      return {
        ...hour,
        summary: 'Free time',
      }
    }
  })

  return (
    <div className='flex flex-col items-center justify-center'>
      {mappedSchedule.map((item, index) => (
        <TimeSlot
          key={index}
          start={item.start}
          end={item.end}
          type={item.type}
          summary={item.summary}
          // onClick 핸들러 수정
          onClick={() => {
            setIsModalOpen(true)
            setSelectedEvent(item)
          }}
        />
      ))}
      {/* Add these lines */}
      {isModalOpen && (
        <div className='modal fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50'>
          <div className='modal-content bg-white p-6 rounded-lg shadow-xl'>
            {/* 선택된 이벤트 정보 표시 */}
            {selectedEvent && (
              <div>
                <h2 className='text-xl font-semibold'>{selectedEvent.type}</h2>
                <p className='mt-2'>{selectedEvent.summary}</p>
                {selectedEvent.type === 'free_time' ? (
                  <>
                    <h3 className='text-lg font-semibold mt-4'>Suggestions:</h3>
                    <ul className='list-disc list-inside'>
                      {suggestions.map((suggestion, index) => (
                        <li key={index}>{suggestion}</li>
                      ))}
                    </ul>
                  </>
                ) : (
                  <>
                    <p className='mt-2'>{selectedEvent.description}</p>
                    <p className='mt-2'>
                      <span className='font-semibold'>Start:</span>{' '}
                      {selectedEvent.start} <br />
                      <span className='font-semibold'>End:</span>{' '}
                      {selectedEvent.end}
                    </p>
                  </>
                )}
              </div>
            )}
            <button
              className='close mt-4 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-700 transition duration-150 ease-in-out'
              onClick={() => {
                setIsModalOpen(false)
                setSelectedEvent(null) // 모달 닫을 때 선택된 이벤트 상태 초기화
              }}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
