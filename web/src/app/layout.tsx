import './globals.css';
import { GraphVisual } from '@/components/GraphVisual';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-knowledge-gray min-h-screen">
        <header className="p-6 border-b border-gray-200">
          <div className="container mx-auto flex justify-between items-center">
            <h1 className="text-2xl font-bold text-linkai-blue">LinkAI</h1>
            <GraphVisual />
          </div>
        </header>
        <main className="container mx-auto p-6">
          {children}
        </main>
      </body>
    </html>
  );
}