import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Award } from 'lucide-react';

interface Certification {
  name: string;
  organizationName: string;
  organizationUrl: string;
  issuedDate: string;
}

interface CertificationsListProps {
  certifications: {
    certificationHistory: Certification[];
  };
}

export function CertificationsList({ certifications }: CertificationsListProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Award className="h-5 w-5 text-yellow-500" />
          Certifications
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {certifications.certificationHistory.map((cert, index) => (
            <div key={index} className="group">
              <h3 className="font-medium group-hover:text-primary transition-colors">
                {cert.name}
              </h3>
              <div className="mt-1 space-y-1">
                <a
                  href={cert.organizationUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-muted-foreground hover:text-primary transition-colors"
                >
                  {cert.organizationName}
                </a>
                <p className="text-sm text-muted-foreground">
                  {cert.issuedDate}
                </p>
              </div>
            </div>
          ))}

          {certifications.certificationHistory.length === 0 && (
            <p className="text-sm text-muted-foreground">
              No certifications listed
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
} 