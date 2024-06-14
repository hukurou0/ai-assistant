'use client'

import Link from 'next/link'
import HomeFillIcon from './ui/icons/HomeFillIcon'
import HomeIcon from './ui/icons/HomeIcon'
import { usePathname } from 'next/navigation'
import ColorButton from './ui/ColorButton'

import { useSession, signIn, signOut } from 'next-auth/react'
import ProfileIcon from './ui/icons/ProfileIcon'
import ProfileFillIcon from './ui/icons/ProfileFillIcon'

const menu = [
  {
    href: '/',
    icon: <HomeIcon />,
    clickerIcon: <HomeFillIcon />,
  },
  {
    href: '/profile',
    icon: <ProfileIcon />,
    clickerIcon: <ProfileFillIcon />,
  },
]

export default function Navbar() {
  const pathName = usePathname()
  const { data: session } = useSession()
  return (
    <div className='flex justify-between items-center px-6'>
      <Link href='/'>
        <h1 className='text-3xl font-bold'>title</h1>
      </Link>
      <nav>
        <ul className='flex gap-4 items-center p-4'>
          {menu.map(item => (
            <li key={item.href}>
              <Link href={item.href}>
                {pathName === item.href ? item.clickerIcon : item.icon}
              </Link>
            </li>
          ))}
          {session ? (
            <ColorButton text='Sign out' onClick={() => signOut()} />
          ) : (
            <ColorButton text='Sign in' onClick={() => signIn()} />
          )}
        </ul>
      </nav>
    </div>
  )
}
