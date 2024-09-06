'use client'

import { usePathname } from 'next/navigation'

import { AiOutlineSetting, AiFillSetting } from "react-icons/ai";
import { AiOutlineCheckSquare, AiFillCheckSquare } from "react-icons/ai";
import Link from 'next/link'

const menu = [
  {
    href: '/task',
    name: 'Task',
    icon: <AiOutlineCheckSquare className='w-7 h-7' />,
    clickerIcon: <AiFillCheckSquare className='w-7 h-7' />,
  },
  {
    href: '/setting',
    name: 'Setting',
    icon: <AiOutlineSetting className='w-7 h-7' />,
    clickerIcon: <AiFillSetting className='w-7 h-7' />,
  },
]

export default function Footer() {
  const pathName = usePathname()
  return (
    <> 
    <div className="fixed bottom-0 left-0 z-50 w-full bg-white border-t border-gray-200 dark:bg-gray-700 dark:border-gray-600">
      <div className="flex items-center justify-center h-16">
        <div className="grid grid-cols-2 gap-4">
          {menu.map((item, index) => (
            <Link href={item.href} key={index}>
              <button type="button" className="flex flex-col items-center justify-center px-5 py-2 hover:bg-gray-50 dark:hover:bg-gray-800 group">
                {pathName === item.href ? item.clickerIcon : item.icon}
                <span className="text-sm text-gray-500 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-500">{item.name}</span>
              </button>
            </Link>
          ))}
        </div>
      </div>
    </div>


    </>

  )
}
