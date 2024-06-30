'use client'

export default function Today() {
  const today = new Date()
  const options: Intl.DateTimeFormatOptions = {
    weekday: 'short',
    day: 'numeric',
  }
  return (
    <div className='font-bold mb-2 w-full text-2xl p-4 flex justify-center'>
      {today.toLocaleDateString('jr-JP', options)}
    </div>
  )
}
