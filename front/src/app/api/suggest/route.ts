import { NextRequest, NextResponse } from 'next/server';
import { ServerAxiosUtil } from '@/util/axios-base';

export interface SuggestTodoData {
  free_time_id: string;
  suggest_todo: {
      id: string;
      title: string;
      required_time: number;
      note: string;
  },
  selected: boolean;
}

export type FetchData = {
  free_time_id: string;
  suggest_todos: SuggestTodoData[];
};

export const GET = async (request: NextRequest) => {
  const { searchParams } = new URL(request.url);
  const freeTimeId = searchParams.get('free_time_id');

  try {
    const axiosBase = new ServerAxiosUtil();
    const response = await axiosBase.get('suggest', {
      params: {
        free_time_id: freeTimeId
      }
    });
    return NextResponse.json(response.data);
  } catch (error) {
    console.error('Failed to fetch schedule:', error);
    return NextResponse.json([], { status: 500 });
  }
};
