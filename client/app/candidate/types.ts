interface CandidateData {
  id: string;
  publicIdentifier: string;
  linkedInIdentifier: string;
  memberIdentifier: string;
  linkedInUrl: string;
  email: string;
  firstName: string;
  lastName: string;
  headline: string;
  location: string;
  summary: string;
  profile_summary: string;
  personality: PersonalityProfile;
  backgroundUrl: string;
  followerCount: number;
  positions: Positions;
  schools: Schools;
  skills: string[];
  languages: string[];
  languagesWithProficiency: LanguageProficiency[];
  recommendations: Recommendations;
  certifications: Certifications;
  testScores: TestScores;
  volunteeringExperiences: VolunteeringExperiences;
  interests: Record<string, unknown>;
}

interface PersonalityProfile {
  mind: PersonalityTrait;
  energy: PersonalityTrait;
  nature: PersonalityTrait;
  tactics: PersonalityTrait;
}

interface PersonalityTrait {
  type: string;
  trait: string;
  score: number;
  description: string;
  scenario: string;
}

interface Positions {
  positionsCount: number;
  positionHistory: Position[];
}

interface Position {
  title: string;
  companyName: string;
  companyLocation?: string;
  description?: string;
  startEndDate: DateRange;
  contractType?: string;
  companyLogo?: string;
  linkedInUrl?: string;
  linkedInId?: string;
}

interface DateRange {
  start: DateInfo;
  end: DateInfo | null;
}

interface DateInfo {
  month: number;
  year: number;
}

interface Schools {
  educationsCount: number;
  educationHistory: Education[];
}

interface Education {
  degreeName: string;
  fieldOfStudy: string | null;
  description?: string;
  linkedInUrl: string;
  schoolLogo: string | null;
  schoolName: string;
  startEndDate: DateRange;
}

interface LanguageProficiency {
  language: string;
  proficiency: string;
}

interface Recommendations {
  recommendationsCount: number;
  recommendationHistory: any[]; // Can be typed more specifically if needed
}

interface Certifications {
  certificationsCount: number;
  certificationHistory: Certification[];
}

interface Certification {
  name: string;
  organizationName: string;
  organizationUrl: string;
  issuedDate: string;
}

interface TestScores {
  testScoresCount: number;
  testScoreHistory: any[]; // Can be typed more specifically if needed
}

interface VolunteeringExperiences {
  volunteeringExperiencesCount: number;
  volunteeringExperienceHistory: VolunteeringExperience[];
}

interface VolunteeringExperience {
  organizationName: string;
  role: string;
  cause?: string;
  period: string;
}

export type { CandidateData };
  