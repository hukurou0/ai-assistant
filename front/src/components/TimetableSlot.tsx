type TimeSlotProps = {
  start: string
  end: string
  type?: string
  description?: string
  id?: string
  summary: string
  onClick?: () => void
}

export function TimeSlot({
  start,
  end,
  summary,
  type,
  id,
  onClick,
}: TimeSlotProps) {
  return (
    <div
      onClick={onClick}
      className={`w-full border-b border-gray-300 py-2 h-24 ${
        type === 'event' ? 'bg-blue-500' : 'bg-white-100'
      }`}
    >
      <p className='text-xl'>{start}</p>
      <p> {summary}</p>
    </div>
  )
}
