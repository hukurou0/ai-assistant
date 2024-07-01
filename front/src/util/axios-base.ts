import axios, { AxiosInstance } from 'axios';

export const AxiosUtil = {
    async createBase(accessToken:string): Promise<AxiosInstance> {
        const axiosBase = axios.create({
            baseURL: 'http://localhost:8000/',
            headers: { 
                'Content-Type': 'application/json', 
                'Authorization': `Bearer ${accessToken}`
            },
            responseType: 'json'
        });
        return axiosBase;
    }
}