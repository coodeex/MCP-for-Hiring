'use client';

import Image from 'next/image';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface Position {
  title: string;
  companyName: string;
  companyLocation: string;
  description: string;
  startEndDate: {
    start: { month: number; year: number };
    end: { month: number; year: number } | null;
  };
  companyLogo: string;
}

interface ExperienceTimelineProps {
  positions: {
    positionHistory: Position[];
  };
}

export function ExperienceTimeline({ positions }: ExperienceTimelineProps) {
  const formatDate = (date: { month: number; year: number }) => {
    return new Date(date.year, date.month - 1).toLocaleDateString('en-US', { 
      month: 'short',
      year: 'numeric'
    });
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Professional Experience</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="relative">
          {/* Timeline Line */}
          <div className="absolute left-8 top-0 bottom-0 w-px bg-border" />

          {/* Timeline Items */}
          <div className="space-y-8">
            {positions.positionHistory.map((position, index) => (
              <div key={index} className="relative grid grid-cols-[72px_1fr] gap-6">
                {/* Company Logo */}
                <div className="relative z-10">
                  {position.companyLogo ? (
                    <Image
                      src={position.companyLogo}
                      alt={position.companyName}
                      width={40}
                      height={40}
                      className="rounded-lg border bg-background"
                    />
                  ) : (
                    <div className="w-10 h-10 rounded-lg bg-muted flex items-center justify-center">
                      {position.companyName[0]}
                    </div>
                  )}
                </div>

                {/* Position Details */}
                <div>
                  <h3 className="font-semibold">{position.title}</h3>
                  <p className="text-sm text-muted-foreground mb-1">
                    {position.companyName} · {position.companyLocation}
                  </p>
                  <p className="text-sm text-muted-foreground mb-4">
                    {formatDate(position.startEndDate.start)} - {position.startEndDate.end ? formatDate(position.startEndDate.end) : 'Present'}
                  </p>
                  
                  {/* Description */}
                  <div className="text-sm text-muted-foreground whitespace-pre-line">
                    {position.description}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
} 