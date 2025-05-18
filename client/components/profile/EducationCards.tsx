import Image from 'next/image';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface Education {
  degreeName: string;
  fieldOfStudy: string | null;
  description: string | null;
  schoolName: string;
  schoolLogo: string | null;
  startEndDate: {
    start: { month: number; year: number };
    end: { month: number; year: number } | null;
  };
}

interface EducationCardsProps {
  education: {
    educationHistory: Education[];
  };
}

export function EducationCards({ education }: EducationCardsProps) {
  const formatDate = (date: { month: number; year: number }) => {
    return new Date(date.year, date.month - 1).toLocaleDateString('en-US', { 
      month: 'short',
      year: 'numeric'
    });
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Education</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {education.educationHistory.map((edu, index) => (
            <div key={index} className="flex gap-4">
              {/* School Logo */}
              <div className="flex-shrink-0">
                {edu.schoolLogo ? (
                  <Image
                    src={edu.schoolLogo}
                    alt={edu.schoolName}
                    width={56}
                    height={56}
                    className="rounded-lg border bg-background"
                  />
                ) : (
                  <div className="w-14 h-14 rounded-lg bg-muted flex items-center justify-center text-xl font-semibold">
                    {edu.schoolName[0]}
                  </div>
                )}
              </div>

              {/* Education Details */}
              <div className="flex-1">
                <h3 className="font-semibold">{edu.schoolName}</h3>
                <div className="flex flex-wrap gap-2 my-2">
                  <Badge variant="secondary">{edu.degreeName}</Badge>
                  {edu.fieldOfStudy && (
                    <Badge variant="outline">{edu.fieldOfStudy}</Badge>
                  )}
                </div>
                <p className="text-sm text-muted-foreground mb-2">
                  {formatDate(edu.startEndDate.start)} - {edu.startEndDate.end ? formatDate(edu.startEndDate.end) : 'Present'}
                </p>
                {edu.description && (
                  <p className="text-sm text-muted-foreground mt-2">
                    {edu.description}
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
} 