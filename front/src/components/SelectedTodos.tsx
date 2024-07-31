import Link from 'next/link'
import React from 'react'

export default function SelectedTodos() {

    const selectedTodos = [
        {
            id:"1",
            name:"Vue JS",
            requiredTime:5,
        },
        {
            id:"2",
            name:"React",
            requiredTime:5,
        },
        {
            id:"3",
            name:"Angular",
            requiredTime:5,
        },
    ]

  return ( 
    <ul className="w-48 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white">
        {selectedTodos.map((todo, index) => (
            <React.Fragment key={todo.id}>
                <li className="w-full border-b border-gray-200 rounded-t-lg dark:border-gray-600">
                    <div className="flex items-center ps-3">
                        <input
                        id={todo.id}
                        type="checkbox"
                        value=""
                        className="w-5 h-5 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500"
                        />
                        <div className="flex flex-col ms-3">
                        <label htmlFor={todo.name} className="pt-1 text-sm font-medium text-gray-900 dark:text-gray-300">
                            {todo.name}
                        </label>
                        <label htmlFor={todo.name} className="py-1 text-sm font-medium text-gray-400 dark:text-gray-300">
                            {"推定所要時間:" + todo.requiredTime + "分"}
                        </label>
                        </div>
                    </div>
                </li>
            </React.Fragment>
        ))}
    </ul>


  )
}
