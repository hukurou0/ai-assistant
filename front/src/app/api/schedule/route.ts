import { NextRequest, NextResponse } from 'next/server';
import { ServerAxiosUtil } from '@/util/axios-base';

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
    const axiosBase = new ServerAxiosUtil();
    const response = await axiosBase.get('schedule', {
      params: {
        need_sync: needSync
      }
    });
    return NextResponse.json(response.data);
  } catch (error) {
    console.error('Failed to fetch schedule:', error);
    return NextResponse.json([], { status: 500 });
  }
};
