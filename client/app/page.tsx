import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen p-8">
      <h1 className="text-2xl font-bold mb-6">Candidate List</h1>
      <div className="flex flex-col gap-4">
        <Link 
          href="/candidate/1" 
          className="p-4 border rounded hover:bg-gray-100 transition-colors"
        >
          View Candidate 1
        </Link>
        <Link 
          href="/candidate/2" 
          className="p-4 border rounded hover:bg-gray-100 transition-colors"
        >
          View Candidate 2
        </Link>
      </div>
    </div>
  );
}
