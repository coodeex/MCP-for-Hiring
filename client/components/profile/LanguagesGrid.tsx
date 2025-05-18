import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

interface Language {
  language: string;
  proficiency: string;
}

interface LanguagesGridProps {
  languages: Language[];
}

const proficiencyToScore = (proficiency: string): number => {
  const scores: { [key: string]: number } = {
    'Native or bilingual proficiency': 100,
    'Professional working proficiency': 80,
    'Limited working proficiency': 60,
    'Elementary proficiency': 40,
    'Beginner': 20
  };
  return scores[proficiency] || 0;
};

const getLanguageEmoji = (language: string): string => {
  const emojiMap: { [key: string]: string } = {
    'English': '🇬🇧',
    'Spanish': '🇪🇸',
    'French': '🇫🇷',
    'German': '🇩🇪',
    'Italian': '🇮🇹',
    'Portuguese': '🇵🇹',
    'Russian': '🇷🇺',
    'Chinese': '🇨🇳',
    'Japanese': '🇯🇵',
    'Korean': '🇰🇷',
    'Arabic': '🇸🇦',
    'Hindi': '🇮🇳',
    'Bengali': '🇧🇩',
    'Dutch': '🇳🇱',
    'Greek': '🇬🇷',
    'Turkish': '🇹🇷',
    'Vietnamese': '🇻🇳',
    'Thai': '🇹🇭',
    'Indonesian': '🇮🇩',
    'Malay': '🇲🇾',
    'Mandarin': '🇨🇳'
  };
  return emojiMap[language] || '🌐';
};

export function LanguagesGrid({ languages }: LanguagesGridProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Languages</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid gap-4">
          {languages.map((lang, index) => (
            <div key={index} className="flex items-center gap-4">
              <div className="w-8 text-2xl">
                {getLanguageEmoji(lang.language)}
              </div>
              <div className="flex-1">
                <div className="flex justify-between items-center mb-1">
                  <span className="font-medium">{lang.language}</span>
                  <span className="text-sm text-muted-foreground">
                    {lang.proficiency}
                  </span>
                </div>
                <Progress value={proficiencyToScore(lang.proficiency)} className="h-2" />
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
} 