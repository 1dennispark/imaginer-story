'use client';

import { Disclosure } from '@headlessui/react'
import { LogoIcon } from './Icons';

export default function Header({currentPage = ''} : {currentPage?: string}) {
  return (
    <Disclosure as="nav" className="w-full bg-white shadow">
      {({ open }) => (
        <>
          <div className="w-full px-8">
            <div className="flex h-16 justify-between">
              <div className="flex">
                <div className="flex flex-shrink-0 items-center">
                  <div className='w-10 h-8'>
                    <LogoIcon />
                  </div>
                  <div className='text-base ml-2'>스토리 창작 API Demo</div>
                </div>
                <div className="ml-6 flex space-x-8">
                  <a
                    href="/character"
                    className={`inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium ${currentPage == 'character' ? "border-indigo-500 text-gray-900" : "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700" }`}
                  >
                    캐릭터
                  </a>
                  <a
                    href="/synopsis"
                    className={`inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium ${currentPage == 'synopsis' ? "border-indigo-500 text-gray-900" : "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700" }`}
                  >
                    시놉시스
                  </a>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </Disclosure>
  )
}
