import { ChangeEventHandler } from "react";

type Props = {
  placeholder?: string;
  value?: string;
  onChange?: (ChangeEventHandler<HTMLInputElement | HTMLTextAreaElement> | undefined);
  textArea?: boolean;
  disabled?: boolean;
}

export default function Input({ placeholder, value, onChange, textArea, disabled }: Props) {
  return (
    <div>
      {!textArea ?
        <input
          className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          disabled={disabled}
        /> :
        <textarea
          className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          disabled={disabled}
        />
      }
    </div>
  )
}
