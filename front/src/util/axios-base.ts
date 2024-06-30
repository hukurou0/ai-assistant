import axios, { AxiosInstance } from 'axios';

export const AxiosUtil = {
    async createBase(): Promise<AxiosInstance> {
        const axiosBase = axios.create({
            baseURL: 'http://localhost:8000/',
            headers: { 'Content-Type': 'application/json' },
            responseType: 'json'
        });
        return axiosBase;
    }
}