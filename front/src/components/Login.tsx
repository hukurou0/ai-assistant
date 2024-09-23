'use client'

import { signIn } from 'next-auth/react';

const Login = () => {
  return (
    <div className="max-w-sm bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
      <img className="rounded-t-lg" src="/icons/hukurou.png" alt="" />
      <div className="w-full max-w-md p-8 space-y-8 rounded shadow-md">
        <h2 className="text-2xl font-bold text-center text-gray-900">ようこそ</h2>
        <p className="text-center text-gray-600">Google連携でCalendarとTaskを連携します</p>
        <div className="mt-8 space-y-6">
          <button
            onClick={() => signIn('google')}
            className="w-full py-2 text-white bg-blue-500 rounded hover:bg-blue-600"
          >
            Googleでサインイン
          </button>
        </div>
      </div>
    </div>
  );
};

export default Login;
