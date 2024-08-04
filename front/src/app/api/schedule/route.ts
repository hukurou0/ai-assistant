import { NextRequest, NextResponse } from 'next/server';
import { AxiosUtil } from '@/util/axios-base';
import { AxiosResponse } from 'axios';

export interface EventData {
  type: string;
  id: string;
  summary: string;
  description: string;
  time: string;
  now: boolean;
}

export interface FreeTimeData {
  type: string;
  id: string;
  time: string;
  now: boolean;
}

export type ScheduleData = EventData | FreeTimeData;
export type ScheduleDataList = ScheduleData[];

export type FetchData = {
    schedule: ScheduleDataList;
};

export const GET = async (request: NextRequest) => {
  const { searchParams } = new URL(request.url);
  const needSync = searchParams.get('need_sync') === 'true';

  try {
    const axios = await AxiosUtil.server.createBase();
    const response: AxiosResponse<FetchData> = await axios.get('/schedule', {
      params: {
        need_sync: needSync,
      },
    });
    return NextResponse.json(response.data);
  } catch (error) {
    console.error('Failed to fetch schedule:', error);
    return NextResponse.json([], { status: 500 });
  }
};
