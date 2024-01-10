import Header from "./Header";

export default function Layout({ currentPage, children }: { currentPage?: string, children: React.ReactNode }) {
    return (
      <div className="relative z-10 flex flex-col" role="dialog" aria-modal="true">
        <div className="flex flex-col fixed inset-0">
          <div className="flex w-full">
            <Header currentPage={currentPage}/>
          </div>
          <div className="flex w-full h-full">
            <div className="flex-1 flex flex-col items-center overflow-scroll">
              {children}
            </div>
          </div>
        </div>
      </div>
    )
  }