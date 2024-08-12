import { Account, NextAuthOptions, Session } from 'next-auth'
import GoogleProvider from 'next-auth/providers/google'
import { JWT } from 'next-auth/jwt'
import { HOST, ServerAxiosUtil } from './axios-base'
import axios from 'axios'

const fetchAppTokenFromGoogleToken = async (token:JWT, googleAccessToken: string, googleRefreshToken: string) => {
  const data = {
    access_token: googleAccessToken,
    refresh_token: googleRefreshToken,
  }
  let response = null
  try {
    const axiosBase = new ServerAxiosUtil()
    response = await axiosBase.post('signup', data)
  } catch (error) {
    console.error('Error sending token:', error)
  }
  const appToken = response?.data
  token.accessToken = appToken["access_token"]
  token.refreshToken = appToken["refresh_token"]
  token.accessTokenExpires = Date.now() + appToken["access_token_expires_in"] * 1000
  token.refreshTokenExpires = Date.now() +  appToken["refresh_token_expires_in"] * 1000
  return token
}

const refreshAccessToken = async (token: JWT) => {
  let response = null
  try {
    const headers = {
      'Content-Type': 'application/json'
    }
    const data = {
      refresh_token: token.refreshToken
    }
    // ServerAxiosUtilを使うと、getServerSessionにより無限ループが発生するため、axiosを直接使用
    response = await axios.post(HOST + 'refresh', data, { headers: headers })
  } catch (error) {
    console.error('Error sending token:', error)
  }

  if (!response) {
    console.error('Failed to refresh access token')
    return {
      ...token,
      error: 'RefreshFailedError'
    }
  }

  const refreshedTokens = response.data

  if (!refreshedTokens || !refreshedTokens.access_token) {
    console.error('Failed to refresh access token')
    return {
      ...token,
      error: 'RefreshFailedError'
    }
  }

  return {
    ...token,
    accessToken: refreshedTokens.access_token,
    accessTokenExpires: Date.now() + refreshedTokens.access_token_expires_in * 1000,
  }
}

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
          if (googleAccessToken && googleRefreshToken){
            token = await fetchAppTokenFromGoogleToken(token, googleAccessToken, googleRefreshToken)
          }
          else {
            console.error('No google access token or refresh token')
          }
        }

        // リフレッシュトークンの有効期限が切れていたらsessionをクリア
        if (token.refreshTokenExpires && Date.now() > token.refreshTokenExpires) {
          return {
            ...token,
            error: 'RefreshTokenExpiredError'
          }
        }

        // アクセストークンの有効期限が切れていたらリフレッシュ
        if (token.accessTokenExpires && Date.now() > token.accessTokenExpires) {
          const new_token = await refreshAccessToken(token)         
          return new_token
        }

        return token
      },
      async session({ session, token }: { session: Session, token: JWT }) {
        session.accessToken = token.accessToken
        session.refreshToken = token.refreshToken
        session.error = token.error
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