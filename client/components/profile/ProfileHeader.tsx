'use client';

import { useState } from 'react';
import Image from 'next/image';
import { LinkedinIcon, Mail, Copy, CheckCircle } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface ProfileHeaderProps {
  candidate: {
    firstName: string;
    lastName: string;
    headline: string;
    location: string;
    linkedInUrl: string;
    email: string;
    followerCount: number;
    backgroundUrl: string;
    positions: {
      positionHistory: Array<{
        title: string;
        companyName: string;
        companyLogo: string;
        startEndDate: {
          start: { month: number; year: number };
          end: { month: number; year: number } | null;
        };
      }>;
    };
  };
}

export function ProfileHeader({ candidate }: ProfileHeaderProps) {
  const [copied, setCopied] = useState(false);
  const currentPosition = candidate.positions.positionHistory[0];
  
  const copyEmail = async () => {
    await navigator.clipboard.writeText(candidate.email);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const formatDate = (date: { month: number; year: number }) => {
    return new Date(date.year, date.month - 1).toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
  };

  return (
    <div className="relative">
      {/* Background Image */}
      <div className="h-64 w-full relative">
      <div className="w-full h-full bg-gradient-to-r from-blue-500 to-purple-600" />
        {/* {candidate.backgroundUrl ? (
          <Image
            src={candidate.backgroundUrl}
            alt="Profile Background"
            fill
            className="object-cover"
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-r from-blue-500 to-purple-600" />
        )} */}
        <div className="absolute inset-0 bg-black/20" />
      </div>

      {/* Profile Content */}
      <div className="container mx-auto px-4">
        <div className="relative -mt-32 pb-8">
          <div className="bg-background rounded-xl shadow-lg p-8">
            <div className="flex flex-col md:flex-row gap-8 items-start">
              {/* Profile Picture Placeholder */}
              <div className="w-32 h-32 bg-gray-200 rounded-full flex items-center justify-center text-gray-400 text-4xl font-light border-4 border-white">
                {candidate.firstName[0]}{candidate.lastName[0]}
              </div>

              {/* Profile Info */}
              <div className="flex-1">
                <h1 className="text-3xl font-bold mb-2">
                  {candidate.firstName} {candidate.lastName}
                </h1>
                <p className="text-xl text-muted-foreground mb-4">{candidate.headline}</p>
                
                <div className="flex flex-wrap gap-4 items-center text-sm text-muted-foreground mb-6">
                  <span>{candidate.location}</span>
                  <span>•</span>
                  <span>{candidate.followerCount.toLocaleString()} followers</span>
                </div>

                {/* Current Position */}
                {currentPosition && (
                  <div className="flex items-center gap-4 mb-6">
                    {/* {currentPosition.companyLogo && (
                      <Image
                        src={currentPosition.companyLogo}
                        alt={currentPosition.companyName}
                        width={48}
                        height={48}
                        className="rounded"
                      />
                    )} */}
                    <div>
                      <p className="font-medium">{currentPosition.title}</p>
                      <p className="text-sm text-muted-foreground">
                        {currentPosition.companyName} · {formatDate(currentPosition.startEndDate.start)} - {currentPosition.startEndDate.end ? formatDate(currentPosition.startEndDate.end) : 'Present'}
                      </p>
                    </div>
                  </div>
                )}

                {/* Action Buttons */}
                <div className="flex flex-wrap gap-4">
                  <Button asChild>
                    <a href={candidate.linkedInUrl} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2">
                      <LinkedinIcon className="w-4 h-4" />
                      LinkedIn Profile
                    </a>
                  </Button>
                  <Button variant="outline" onClick={copyEmail}>
                    <Mail className="w-4 h-4 mr-2" />
                    {copied ? <CheckCircle className="w-4 h-4 mr-2 text-green-500" /> : <Copy className="w-4 h-4 mr-2" />}
                    {copied ? 'Copied!' : 'Copy Email'}
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 