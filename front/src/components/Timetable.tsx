'use client'

import { useEffect, useState } from 'react';
import Event from './Event'
import FreeTime from './FreeTime';
import { ScheduleDataList, ScheduleData, EventData, FreeTimeData, FetchData} from '@/app/api/schedule/route';
import { AxiosUtil } from '@/util/axios-base';

export default function Timetable() {
  const [schedule, setSchedule] = useState<ScheduleDataList | null>(null);

  const fetchSchedule = async (needSync:boolean) => {
    try {
      const axios = await AxiosUtil.client.createBase();
      const response = await axios.get('/schedule',{
        params: {
          "need_sync": needSync
        }
      }).catch((error) => {
        console.error('Error:', error);
      });
      if (!response) {
        console.error('Failed to fetch schedule');
        return {schedule: []} as FetchData;
      }
      console.log('response:', response.data);
      return response.data as FetchData;
    } catch (error) {
      console.error('Failed to fetch schedule:', error);
      return {schedule: []} as FetchData;
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      let data = await fetchSchedule(false);
      if (!data.schedule || data.schedule.length === 0) {
        data =  await fetchSchedule(true);
      }
      console.log('data:', data);
      setSchedule(data.schedule);
    }
    fetchData();
  }, []);

  function isEventData(data: ScheduleData): data is EventData {
    return data.type === 'event';
  }
  
  function isFreeTimeData(data: ScheduleData): data is FreeTimeData {
    return data.type === 'free_time';
  }

  if (!schedule) {
    return <div>Loading...</div>;
  }

  return (
      <ol className="relative border-s border-gray-200 dark:border-gray-700"> 
        {schedule.map((schedule) => {
          if (isEventData(schedule)) {
            return <Event key={schedule.id} data={schedule}/>;
          } else if (isFreeTimeData(schedule)) {
            return <FreeTime key={schedule.id} data={schedule}/>;
          }
        })}              
      </ol>
    )
}
