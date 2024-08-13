import { FetchData, SuggestTodoData } from '@/app/api/suggest/route';
import { ClientAxiosUtil } from '@/util/axios-base';
import React, { useEffect, useState } from 'react'

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
  }, []);

  return ( 
    <ul className="w-70 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white">
        {suggestTodos.map((data, index) => (
            <React.Fragment key={data.suggest_todo.id}>
                <li className="w-full border-b border-gray-200 rounded-t-lg dark:border-gray-600">
                  <div className="flex items-center ps-3">
                      <div className="flex-none w-6 mr-2">
                          <input
                              id={data.suggest_todo.id}
                              type="checkbox"
                              value=""
                              className="w-5 h-5 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500"
                          />
                      </div>
                      <div className="flex flex-col flex-grow">
                          <label htmlFor={data.suggest_todo.title} className="pt-1 text-sm font-medium text-gray-900 dark:text-gray-300">
                              {data.suggest_todo.title}
                          </label>
                          <label htmlFor={data.suggest_todo.title} className="py-1 text-sm font-medium text-gray-400 dark:text-gray-300">
                              {"推定所要時間:" + data.suggest_todo.required_time + "分"}
                          </label>
                      </div>
                  </div>
                </li>

            </React.Fragment>
        ))}
    </ul>


  )
}
