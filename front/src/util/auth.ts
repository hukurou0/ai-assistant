import { Account, NextAuthOptions, Session } from 'next-auth'
import GoogleProvider from 'next-auth/providers/google'
import axios from 'axios'
import { HOST } from './axios-base'
import { JWT } from 'next-auth/jwt'

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
      async jwt({ token, account }: { token:JWT, account: Account | null }) {
        // 初回サインイン時
        if (account) {
          const googleAccessToken = account.access_token
          const googleRefreshToken = account.refresh_token
          const data = {
            access_token: googleAccessToken,
            refresh_token: googleRefreshToken,
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
          token.accessToken = appToken["access_token"]
          token.refreshToken = appToken["refresh_token"]
        }
        return token
      },
      async session({ session, token }: { session: Session, token: JWT }) {
        session.accessToken = token.accessToken
        session.refreshToken = token.refreshToken
        return session
      },
      async signIn({ account }: { account: Account | null}) {
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