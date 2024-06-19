'use client'

export default function Today() {
  const today = new Date()
  const options = { weekday: 'short', day: 'numeric' }
  return (
    <div className='font-bold mb-2 w-full text-2xl bg-blue-400 flex justify-center'>
      {today.toLocaleDateString('jr-JP', options)}
    </div>
  )
}
