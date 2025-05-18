import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

interface PersonalityTrait {
  type: string;
  trait: string;
  score: number;
  description: string;
  scenario: string;
}

interface PersonalityProps {
  personality: {
    mind: PersonalityTrait;
    energy: PersonalityTrait;
    nature: PersonalityTrait;
    tactics: PersonalityTrait;
  };
}

export function PersonalitySection({ personality }: PersonalityProps) {
  const traits = [
    { key: 'mind', color: 'bg-blue-500' },
    { key: 'energy', color: 'bg-green-500' },
    { key: 'nature', color: 'bg-purple-500' },
    { key: 'tactics', color: 'bg-orange-500' }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {traits.map(({ key, color }) => {
        const trait = personality[key as keyof typeof personality];
        return (
          <Card key={key}>
            <CardHeader>
              <CardTitle className="flex justify-between items-center">
                <span>{trait.trait}</span>
                <span className="text-2xl font-bold">{trait.score}%</span>
              </CardTitle>
              <CardDescription>{trait.type}</CardDescription>
            </CardHeader>
            <CardContent>
              {/* Progress Bar */}
              <div className="h-2 w-full bg-gray-200 rounded-full mb-4">
                <div
                  className={`h-full rounded-full ${color}`}
                  style={{ width: `${trait.score}%` }}
                />
              </div>
              
              {/* Description */}
              <p className="text-sm text-muted-foreground mb-2">
                {trait.description}
              </p>
              
              {/* Scenario */}
              <div className="bg-muted/50 p-3 rounded-lg">
                <p className="text-sm italic">
                  "In practice: {trait.scenario}"
                </p>
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
} 