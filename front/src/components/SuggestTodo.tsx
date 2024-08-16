import React, { useEffect, useState } from 'react'
import { SuggestTodoData } from '@/app/api/suggest/route';

export default function SuggestTodo(props: {data: SuggestTodoData}) {
  const [isChecked, setIsChecked] = useState(false);

  useEffect(() => {
    if (props.data) {
      console.log(props.data.selected);
      setIsChecked(props.data.selected);
    }
  }, [props.data.selected]);
  
  const handleCheckboxChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setIsChecked(event.target.checked);
  };

  return (
    <li className="w-full border-b border-gray-200 rounded-t-lg dark:border-gray-600">
        <div className="flex items-center ps-3">
            <div className="flex-none w-6 mr-2">
                <input
                    id={props.data.suggest_todo.id}
                    type="checkbox"
                    value=""
                    onChange={handleCheckboxChange}
                    checked={isChecked}
                    className="w-5 h-5 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500"
                />
            </div>
            <div className="flex flex-col flex-grow">
                <label htmlFor={props.data.suggest_todo.title} className="pt-1 text-sm font-medium text-gray-900 dark:text-gray-300">
                    {props.data.suggest_todo.title}
                </label>
                <label htmlFor={props.data.suggest_todo.title} className="py-1 text-sm font-medium text-gray-400 dark:text-gray-300">
                    {"推定所要時間:" + props.data.suggest_todo.required_time + "分"}
                </label>
            </div>
        </div>
    </li>
  )
}
