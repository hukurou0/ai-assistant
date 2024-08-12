import React from 'react'
import Box from './Box'
import Logout from './Logout'

export default function Setting() {
  return (
    <Box>
    <div className="h-screen flex flex-col items-center">
      <div className="w-full max-w-md mx-auto mt-10">
        {/* Header */}
        <div className="flex items-center justify-between border-b pb-3 mb-5">
          <h1 className="text-2xl font-bold">設定</h1>
        </div>

        {/* Data Section */}
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-2">データ</h2>
          <div className="flex items-center justify-between py-2">
            <span className="text-lg">カレンダー連携</span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              className="w-5 h-5"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5l7 7-7 7"
              />
            </svg>
          </div>
          <div className="flex items-center justify-between py-2">
            <span className="text-lg">TODO連携</span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              className="w-5 h-5"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5l7 7-7 7"
              />
            </svg>
          </div>
        </div>

        {/* Details and Support Section */}
        <div>
          <h2 className="text-xl font-semibold mb-2">詳細とサポート</h2>
          <div className="flex items-center justify-between py-2">
            <span className="text-lg">お問い合わせ</span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              className="w-5 h-5"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5l7 7-7 7"
              />
            </svg>
          </div>
          <div className="flex items-center justify-between py-2">
            <span className="text-lg">利用規約</span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              className="w-5 h-5"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5l7 7-7 7"
              />
            </svg>
          </div>
          <div className="flex items-center justify-between py-2">
            <span className="text-lg">プライバシーポリシー</span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              className="w-5 h-5"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5l7 7-7 7"
              />
            </svg>
          </div>
        </div>
      </div>

      {/* Bottom Navigation */}
      <div className="fixed bottom-0 w-full max-w-md mx-auto flex justify-around border-t py-2 bg-white">
        <div className="text-2xl">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            className="w-6 h-6"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 12h14M12 5l7 7-7 7"
            />
          </svg>
        </div>
        <div className="text-2xl">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            className="w-6 h-6"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M15 12H9m12-9l-6 6-6-6"
            />
          </svg>
        </div>
        <div className="text-2xl">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            className="w-6 h-6"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 12h14M12 5l7 7-7 7"
            />
          </svg>
        </div>
      </div>
      <Logout />
    </div>
    </Box>
  )
}
