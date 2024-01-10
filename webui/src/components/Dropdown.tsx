import { Fragment } from 'react'
import { Menu, Transition } from '@headlessui/react'
import { ChevronDownIcon, ChevronUpIcon } from '@heroicons/react/20/solid'

export type DropdownItem = {
  label: string;
  value: string;
}

type Props = {
  items: DropdownItem[];
  placeholder?: string;
  selectedValue?: string;
  onSelected?: (item: DropdownItem) => void;
  disabled?: boolean;
}

export default function Dropdown({ items, placeholder, selectedValue, onSelected, disabled }: Props) {
  return (
    <Menu as="div" className="relative inline-block text-left">
      {({ open }) => (
        <>
          <div>
            <Menu.Button className="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-white px-3 py-2 text-sm shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50" disabled={disabled}>
              {!selectedValue || !items.find(item => item.value == selectedValue) ?
                <div className='font-normal text-gray-400'>{placeholder}</div> : <div className='font-normal text-gray-900'>{items.find(item => item.value == selectedValue)?.label}</div>
              }
              {open ?
                <ChevronUpIcon className="-mr-1 h-5 w-5 text-gray-400" aria-hidden="true" />
                : <ChevronDownIcon className="-mr-1 h-5 w-5 text-gray-400" aria-hidden="true" />
              }
            </Menu.Button>
          </div>

          <Transition
            as={Fragment}
            enter="transition ease-out duration-100"
            enterFrom="transform opacity-0 scale-95"
            enterTo="transform opacity-100 scale-100"
            leave="transition ease-in duration-75"
            leaveFrom="transform opacity-100 scale-100"
            leaveTo="transform opacity-0 scale-95"
          >
            <Menu.Items className="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none max-h-52 overflow-auto">
              <div className="py-1">
                {items.map((item) => (
                  <Menu.Item key={`dropdown_item_${item.label}`}>
                    <button
                      onClick={(e) => { onSelected?.(item); e.stopPropagation(); }}
                      className={`${selectedValue == item.value ? 'bg-gray-100 text-gray-900 font-semibold' : 'text-gray-700'} block w-full px-4 py-2 text-left text-sm hover:bg-gray-100`}>
                      {item.label}
                    </button>
                  </Menu.Item>
                ))}
              </div>
            </Menu.Items>
          </Transition>
        </>
      )}

    </Menu>
  )
}
