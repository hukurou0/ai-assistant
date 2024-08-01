'use client'

import Link from 'next/link'
import ScheduleIcon from './ui/icons/ScheduleIcon'
import ScheduleFillIcon from './ui/icons/ScheduleFillIcon'
import { usePathname } from 'next/navigation'

import SettingIcon from './ui/icons/Setting'
import SettingFillIcon from './ui/icons/SettingFill'

const menu = [
  {
    href: '/',
    icon: <ScheduleIcon />,
    clickerIcon: <ScheduleFillIcon />,
  },
  {
    href: '/setting',
    icon: <SettingIcon />,
    clickerIcon: <SettingFillIcon />,
  },
]

export default function Footer() {
  const pathName = usePathname()
  return (
    <div className="fixed bottom-0 w-full bg-slate-300 text-white p-4 text-center">
      <nav className='flex justify-center'>
        <ul className='flex gap-4 items-center'>
          {menu.map(item => (
            <li key={item.href}>
              <Link href={item.href}>
                {pathName === item.href ? item.clickerIcon : item.icon}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </div>
      )
    }
