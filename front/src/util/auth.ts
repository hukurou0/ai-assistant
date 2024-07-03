import { NextAuthOptions } from 'next-auth'
import GoogleProvider from 'next-auth/providers/google'
import axios from 'axios'
import { HOST } from './axios-base'

export const authOptions: NextAuthOptions = {
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
      async jwt({ token, account }: { token: any, account: any }) {
        // 初回サインイン時
        if (account) {
          token.accessToken = account.access_token
          token.refreshToken = account.refresh_token
        }
        return token
      },
      async session({ session, token }: { session: any, token: any }) {
        const data = {
          access_token: token.accessToken,
          refresh_token: token.refreshToken,
        }
        let response = null
        try {
          response = await axios.post(HOST + 'signup', data,
          {
            headers: {
              'Content-Type': 'application/json'
            }
          })
        } catch (error) {
          console.error('Error sending token:', error)
        }
        const appToken = response?.data
        session.accessToken = appToken["access_token"]
        session.refreshToken = appToken["refresh_token"]
        return session
      },
      async signIn({ account }: { account: any}) {
        if (account && account.provider === 'google') {
          return true
        } else {
          return false
        }
      },
    },
    pages: {
      signIn: '/auth/signin', // SignInページのカスタマイズ
    },
  }