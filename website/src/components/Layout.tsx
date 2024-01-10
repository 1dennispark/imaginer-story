import Header from "./Header";

export default function Layout({currentPage, children}: { currentPage?: string, children: React.ReactNode }) {
  return (
    <>
      <div className="flex flex-col fixed inset-0">
        <div className="flex w-full">
          <Header currentPage={currentPage}/>
        </div>
      </div>
      <main className="relative flex flex-col mt-16 w-full items-center">
        {children}
      </main>
    </>
  );
}