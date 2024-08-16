import { NextRequest, NextResponse } from 'next/server';
import { ServerAxiosUtil } from '@/util/axios-base';

export const POST = async (request: NextRequest) => {
  const body = await request.json();
  const { suggest_todo_id, selected } = body;

  try {
    const axiosBase = new ServerAxiosUtil();
    const response = await axiosBase.post('suggest/select', {
      suggest_todo_id: suggest_todo_id,
      selected: selected
    });
    return NextResponse.json(response.data);
  } catch (error) {
    console.error('Failed to fetch schedule:', error);
    return NextResponse.json([], { status: 500 });
  }
};
