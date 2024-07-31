'use client'

import React from 'react'

import { signOut } from 'next-auth/react';

export default function Logout() {
  return (
    <button
        onClick={() => signOut()}
        className="w-full py-2 m-5 text-white bg-red-500 rounded hover:bg-red-600"
      >
        サインアウト
      </button>
  )
}
