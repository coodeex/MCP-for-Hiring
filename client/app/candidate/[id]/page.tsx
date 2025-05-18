import { notFound } from "next/navigation";
import fs from "fs";
import path from "path";
import Link from "next/link";
import { CandidateData } from "../types";
import { ProfileHeader } from "@/components/profile/ProfileHeader";
import { PersonalitySection } from "@/components/profile/PersonalitySection";
import { SummaryTabs } from "@/components/profile/SummaryTabs";
import { ExperienceTimeline } from "@/components/profile/ExperienceTimeline";
import { EducationCards } from "@/components/profile/EducationCards";
import { SkillsCloud } from "@/components/profile/SkillsCloud";
import { CertificationsList } from "@/components/profile/CertificationsList";
import { LanguagesGrid } from "@/components/profile/LanguagesGrid";
import { VolunteeringCards } from "@/components/profile/VolunteeringCards";
import { CompanyCard } from "@/components/profile/CompanyCard";
import { ContactFooter } from "@/components/profile/ContactFooter";

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
  const data = await getCandidateData(params.id);
  
  if (!data) {
    notFound();
  }

  const candidateData = data.data.person;
  const companyData = data.data.company;

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <ProfileHeader candidate={candidateData} />

      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            <PersonalitySection personality={candidateData.personality} />
            <SummaryTabs summary={candidateData.summary} profileSummary={candidateData.profile_summary} />
            <ExperienceTimeline positions={candidateData.positions} />
            <EducationCards education={candidateData.schools} />
            <SkillsCloud skills={candidateData.skills} />
            <LanguagesGrid languages={candidateData.languagesWithProficiency} />
            <VolunteeringCards volunteering={candidateData.volunteeringExperiences} />
          </div>

          {/* Sidebar */}
          <div className="space-y-8">
            <CompanyCard company={companyData} />
            <CertificationsList certifications={candidateData.certifications} />
          </div>
        </div>
      </div>

      <ContactFooter candidate={candidateData} />
    </div>
  );
} 