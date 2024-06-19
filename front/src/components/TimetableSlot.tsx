type TimeSlotProps = {
  start: string
  end: string
  type?: string
}

export function TimeSlot({ start, end, type }: TimeSlotProps) {
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
