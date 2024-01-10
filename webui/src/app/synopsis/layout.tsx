import Layout from "@/components/Layout";

export default function PageLayout({ children }: { children: React.ReactNode }) {
  return (
    <Layout currentPage="synopsis">
      {children}
    </Layout>
  );
}