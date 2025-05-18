'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Search } from 'lucide-react';

interface SkillsCloudProps {
  skills: string[];
}

export function SkillsCloud({ skills }: SkillsCloudProps) {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredSkills = skills.filter(skill =>
    skill.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Skills</span>
          <span className="text-sm font-normal text-muted-foreground">
            {skills.length} skills
          </span>
        </CardTitle>
        
        {/* Search Input */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search skills..."
            className="pl-9"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </CardHeader>
      <CardContent>
        <div className="flex flex-wrap gap-2">
          {filteredSkills.map((skill, index) => (
            <Badge
              key={index}
              variant="secondary"
              className="cursor-default transition-colors hover:bg-secondary/80"
            >
              {skill}
            </Badge>
          ))}
          {filteredSkills.length === 0 && (
            <p className="text-sm text-muted-foreground">
              No skills found matching "{searchTerm}"
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
} 