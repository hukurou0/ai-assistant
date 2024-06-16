import NextAuth from 'next-auth'
import GoogleProvider from 'next-auth/providers/google'
import axios from 'axios'

const authOptions = {
  providers: [
    GoogleProvider(
      {
        clientId: process.env.GOOGLE_OAUTH_ID || '',
        clientSecret: process.env.GOOGLE_OAUTH_SECRET || '',
        authorization: {
          params: {
            scope: 'openid profile email https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/tasks',
            access_type: 'offline',
            prompt: 'consent',
          },
        },
      },   
    ),
  ],
  callbacks: {
    async signIn({ account }: { account: any }) {
      if (account && account.provider === 'google') {
        const data = {
          access_token: account.access_token,
          refresh_token: account.refresh_token,
        }
        try {
          const response = await axios.post('http://localhost:8000/signup', data,
          {
            headers: {
              'Content-Type': 'application/json'
            }
          })
          return response.data
        } catch (error) {
          console.error('Error sending token:', error)
          return false
        }
      }
    },
  },
  pages: {
    signIn: '/auth/signin', // SignInページのカスタマイズ
  },
}

const handler = NextAuth(authOptions)

export { authOptions, handler as GET, handler as POST }
