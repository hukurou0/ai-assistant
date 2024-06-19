export default function Today() {
  const today = new Date()
  const options = { weekday: 'short', day: 'numeric' }
  return (
    <div className='font-bold mb-2 w-full text-2xl bg-blue-400 flex justify-center'>
      {today.toLocaleDateString('jr-JP', options)}
    </div>
  )
}
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
        end: '12:00',
      },
      {
        type: 'event',
        id: '3',
        summary: 'Event 2',
        description: 'Description for Event 2',
        start: '14:00',
        end: '16:00',
      },
    ],
  }
  setSchedule(mockData.schedule)
}, [])
