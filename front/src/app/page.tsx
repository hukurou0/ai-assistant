import Timetable from '@/components/Timetable'
import React from 'react'

import { getServerSession } from 'next-auth';
import { authOptions } from '@/util/auth';
import Box from '@/components/Box';
import Login from '@/components/Login';


export default async function Home() {
  const session = await getServerSession(authOptions);
  return (
    <>
    {session ? (
      <>
      <h1 className='text-2xl font-semibold text-center mt-5'>今日のスケジュール</h1>
      <hr className="border-t border-gray-300 my-4" />
      <Box className='mx-2 mb-10'>
        <Timetable />
      </Box>

      </>
      ) : 
      <Box>
        <Login />
      </Box>
      }
    </>
  )
}
