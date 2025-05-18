import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Heart } from 'lucide-react';

interface Volunteering {
  organizationName: string;
  role: string;
  cause?: string;
  period: string;
}

interface VolunteeringCardsProps {
  volunteering: {
    volunteeringExperienceHistory: Volunteering[];
  };
}

export function VolunteeringCards({ volunteering }: VolunteeringCardsProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Heart className="h-5 w-5 text-red-500" />
          Volunteering
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid gap-6">
          {volunteering.volunteeringExperienceHistory.map((vol, index) => (
            <div key={index} className="group relative">
              <div className="flex flex-col gap-2">
                <h3 className="font-semibold group-hover:text-primary transition-colors">
                  {vol.role}
                </h3>
                <div className="flex flex-wrap items-center gap-x-2 gap-y-1">
                  <span className="text-sm text-muted-foreground">
                    {vol.organizationName}
                  </span>
                  {vol.cause && (
                    <>
                      <span className="text-muted-foreground">•</span>
                      <Badge variant="outline" className="text-xs">
                        {vol.cause}
                      </Badge>
                    </>
                  )}
                </div>
                <p className="text-sm text-muted-foreground">
                  {vol.period}
                </p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
} 