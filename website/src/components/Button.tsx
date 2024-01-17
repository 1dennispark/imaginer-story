import classNames from "classnames";
import { LoadingCircle } from "./Icons";

type Props = {
    label: string;
    onClick?: () => void;
    loading?: boolean;
    disabled?: boolean;
}

export default function Button({label, onClick, loading, disabled} : Props) {
    const btnClassName = classNames("rounded-md px-4 py-[5px] text-sm font-semibold shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600",
        {
            "text-white bg-indigo-600 hover:bg-indigo-500": !disabled,
            "text-gray-400 bg-gray-200": disabled,
            "hover:cursor-not-allowed": disabled || loading,
        }
    );

    return (
      <>
        <button
          type="button"
          disabled={disabled || loading}
          className={btnClassName}
          onClick={onClick}
        >
          {!loading ?
            label :
            <div className="flex items-center justify-center px-0.5">
                <LoadingCircle width="20" height="20" />
            </div>
          }
        </button>
      </>
    )
  }