import { NextRequest, NextResponse } from 'next/server';
import { ServerAxiosUtil } from '@/util/axios-base';

export const GET = async (request: NextRequest) => {
  try {
    const axiosBase = new ServerAxiosUtil();
    await axiosBase.get('/sync/google-todo');
    return NextResponse.json({"status": "ok"});
  } catch (error) {
    console.error('Failed to sync todo', error);
    return NextResponse.json([], { status: 500 });
  }
};
