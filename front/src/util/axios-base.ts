import axios, { AxiosInstance } from 'axios';
import { getServerSession } from 'next-auth';
import { authOptions } from './auth';

declare module 'next-auth' {
  interface Session {
    accessToken?: string;
    refreshToken?: string;
  }
}

declare module 'next-auth/jwt' {
  interface JWT {
    accessToken?: string;
    refreshToken?: string;
  }
}

export const HOST = 'http://api:8000/';

export const AxiosUtil = {
    async createBase(): Promise<AxiosInstance> {
        const session = await getServerSession(authOptions)
        let headers = {}
        if (session) {
          headers = {
            'Content-Type': 'application/json', 
            'Authorization': `Bearer ${session.accessToken}`
          }
        } else {
          headers =  {
            'Content-Type': 'application/json', 
          }
        }
        
        const axiosBase = axios.create({
          baseURL: HOST,
          headers: headers,
          responseType: 'json'
        })
        return axiosBase;
    }
}