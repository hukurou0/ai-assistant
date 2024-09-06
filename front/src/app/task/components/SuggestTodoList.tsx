import { FetchData, SuggestTodoData } from '@/app/api/suggest/route';
import { ClientAxiosUtil } from '@/util/axios-base';
import React, { useEffect, useState } from 'react'
import SuggestTodo from './SuggestTodo';
//import { suggestTodoDataSample } from '@/mockData/sampleSuggestTodo';

export default function SuggestTodoList(props: {id:string}) {
  const [suggestTodos, setSuggestTodos] = useState<SuggestTodoData[]>([]);

  const fetchSuggestTodos = async (freeTimeId:string) => {
    try {
      const axiosBase = new ClientAxiosUtil();
      const response = await axiosBase.get('/suggest',{
        params: {
          free_time_id: freeTimeId
        }
      }).catch((error) => {
        console.error('Error:', error);
      });
      if (!response) {
        console.error('Failed to fetch schedule');
        return {} as FetchData;
      }
      return response.data as FetchData;
    } catch (error) {
      console.error('Failed to fetch schedule:', error);
      return {} as FetchData;
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      const data = await fetchSuggestTodos(props.id);
      if (typeof data !== 'undefined' && 'suggest_todos' in data) {
        setSuggestTodos(data.suggest_todos);
      }
    }
    fetchData();
    //setSuggestTodos(suggestTodoDataSample);
  }, []);

  return ( 
    <ul className="w-70 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white">
        {suggestTodos.map((data, index) => (
            <SuggestTodo key={data.suggest_todo.id} data={data} />
        ))}
    </ul>


  )
}
