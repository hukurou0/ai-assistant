import { getServerSession } from 'next-auth'
import { authOptions } from '@/util/auth'
import { redirect } from 'next/navigation'
import { getProviders } from 'next-auth/react'
import Signin from '@/components/Signin'

type Props = {
  searchParams: {
    callbackUrl: string
  }
}

export default async function SigninPage({
  searchParams: { callbackUrl },
}: Props) {
  const session = await getServerSession(authOptions)

  if (session) {
    redirect('/')
  }

  const providers = (await getProviders()) ?? {}

  return (
    <section className='flex justify-center mt-[30%]'>
      <Signin providers={providers} callbackUrl={callbackUrl ?? '/'} />
    </section>
  )
}
