import { notFound } from "next/navigation";
import fs from "fs";
import path from "path";
import Link from "next/link";
import { CandidateData } from "../types";

async function getCandidateData(id: string) {
  const filePath = path.join(process.cwd(), "db", `p${id}.json`);
  
  try {
    const fileContents = await fs.promises.readFile(filePath, 'utf8');
    return JSON.parse(fileContents);
  } catch (error) {
    return null;
  }
}

export default async function CandidatePage({ params }: { params: { id: string } }) {
  const candidateData: CandidateData = (await getCandidateData(params.id)).data.person;

  if (!candidateData) {
    notFound();
  }

  return (
    <div className="min-h-screen p-8">      
      <div className="mt-6">
        <h1 className="text-2xl font-bold mb-4">
        {candidateData.firstName} {candidateData.lastName}
        </h1>
        <div className="bg-white shadow rounded-lg p-6">
          <p className="text-gray-600">ID: {params.id}</p>
          {/* You can add more candidate details here as needed */}
        </div>
      </div>
    </div>
  );
} 