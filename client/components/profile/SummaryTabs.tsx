'use client';

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent } from "@/components/ui/card";

interface SummaryTabsProps {
  summary: string;
  profileSummary: string;
}

export function SummaryTabs({ summary, profileSummary }: SummaryTabsProps) {
  return (
    <Tabs defaultValue="summary" className="w-full">
      <TabsList className="grid w-full grid-cols-2">
        <TabsTrigger value="summary">Personal Summary</TabsTrigger>
        <TabsTrigger value="profile">Profile Analysis</TabsTrigger>
      </TabsList>
      
      <TabsContent value="summary">
        <Card>
          <CardContent className="pt-6">
            <div className="prose max-w-none">
              <p className="text-muted-foreground whitespace-pre-line">
                {summary}
              </p>
            </div>
          </CardContent>
        </Card>
      </TabsContent>
      
      <TabsContent value="profile">
        <Card>
          <CardContent className="pt-6">
            <div className="prose max-w-none">
              <p className="text-muted-foreground whitespace-pre-line">
                {profileSummary}
              </p>
            </div>
          </CardContent>
        </Card>
      </TabsContent>
    </Tabs>
  );
} 