import axios, { AxiosInstance } from 'axios';
import { getServerSession } from 'next-auth';
import { authOptions } from './auth';

declare module 'next-auth' {
  interface Session {
    accessToken?: string;
    refreshToken?: string;
    accessTokenExpires?: number;
    refreshTokenExpires?: number;
    error?: string;
  }
}

declare module 'next-auth/jwt' {
  interface JWT {
    accessToken?: string;
    refreshToken?: string;
    accessTokenExpires?: number;
    refreshTokenExpires?: number;
    error?: string;
  }
}

export const HOST = process.env.REACT_API_HOST;

export class ServerAxiosUtil {
  client: AxiosInstance;

  constructor() {
      this.client = axios.create(); // デフォルトのインスタンスを作成
  }

  async initialize() {
      const session = await getServerSession(authOptions);
      let headers: { 'Content-Type': string, Authorization?: string } = {
          'Content-Type': 'application/json'
      };

      if (session) {
          headers['Authorization'] = `Bearer ${session.accessToken}`;
      }
      this.client = axios.create({
          baseURL: HOST,
          headers: headers,
          responseType: 'json',
      });
  }

  async get(url: string, config = {}) {
    await this.initialize();
    try {
        const response = await this.client.get(url, config);
        return response;
    } catch (error) {
        console.error('GETリクエストでエラーが発生:', error);
        throw error;
    }
  }

  async post(url: string, config = {}) {
    await this.initialize();
    try {
        const response = await this.client.post(url, config);
        return response;
    } catch (error) {
        console.error('POSTリクエストでエラーが発生:', error);
        throw error;
    }
  }
}

export class ClientAxiosUtil {
  client: AxiosInstance;

  constructor() {
    const headers =  {
      'Content-Type': 'application/json', 
    }
    const axiosBase = axios.create({
      baseURL: '/api',
      headers: headers,
      responseType: 'json'
    })
    this.client = axiosBase;
  }

  async get(url: string, config = {}) {
    try {
        const response = await this.client.get(url, config);
        return response;
    } catch (error) {
        console.error('GETリクエストでエラーが発生:', error);
        throw error;
    }
  }

  async post(url: string, config = {}) {
    try {
        const response = await this.client.post(url, config);
        return response;
    } catch (error) {
        console.error('POSTリクエストでエラーが発生:', error);
        throw error;
    }
  }
}