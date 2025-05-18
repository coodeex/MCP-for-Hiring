import Image from 'next/image';
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Building2, Users, MapPin, Globe, TrendingUp } from 'lucide-react';

interface Company {
  name: string;
  logo: string;
  tagline: string;
  industry: string;
  employeeCount: number;
  followerCount: number;
  headquarter: {
    city: string;
    country: string;
  };
  websiteUrl: string;
  specialities: string[];
  fundingData?: {
    lastFundingRound?: {
      fundingType: string;
      moneyRaised: {
        amount: string;
        currencyCode: string;
      };
      announcedOn: string;
    };
  };
}

interface CompanyCardProps {
  company: Company;
}

export function CompanyCard({ company }: CompanyCardProps) {
  const formatMoney = (amount: string) => {
    const num = parseInt(amount);
    if (num >= 1000000000) {
      return `$${(num / 1000000000).toFixed(1)}B`;
    }
    if (num >= 1000000) {
      return `$${(num / 1000000).toFixed(1)}M`;
    }
    return `$${(num / 1000).toFixed(1)}K`;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'long',
      year: 'numeric'
    });
  };

  return (
    <Card>
      <CardHeader className="flex flex-row items-center gap-4 pb-2">
        {company.logo && (
          <Image
            src={company.logo}
            alt={company.name}
            width={48}
            height={48}
            className="rounded-lg"
          />
        )}
        <div>
          <h3 className="font-semibold">{company.name}</h3>
          <p className="text-sm text-muted-foreground">{company.tagline}</p>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Company Details */}
          <div className="space-y-3">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Building2 className="h-4 w-4" />
              {company.industry}
            </div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Users className="h-4 w-4" />
              {company.employeeCount.toLocaleString()} employees
            </div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <MapPin className="h-4 w-4" />
              {company.headquarter.city}, {company.headquarter.country}
            </div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Globe className="h-4 w-4" />
              <a
                href={company.websiteUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-primary transition-colors"
              >
                {new URL(company.websiteUrl).hostname}
              </a>
            </div>
          </div>

          {/* Specialities */}
          <div>
            <h4 className="text-sm font-medium mb-2">Specialities</h4>
            <div className="flex flex-wrap gap-2">
              {company.specialities.map((spec, index) => (
                <Badge key={index} variant="secondary">
                  {spec}
                </Badge>
              ))}
            </div>
          </div>

          {/* Funding Info */}
          {company.fundingData?.lastFundingRound && (
            <div className="border-t pt-4 mt-4">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="h-4 w-4 text-green-500" />
                <h4 className="text-sm font-medium">Latest Funding</h4>
              </div>
              <div className="space-y-1">
                <p className="text-sm">
                  <span className="font-medium">{company.fundingData.lastFundingRound.fundingType}</span>
                </p>
                <p className="text-sm text-muted-foreground">
                  {formatMoney(company.fundingData.lastFundingRound.moneyRaised.amount)}
                  <span className="mx-1">•</span>
                  {formatDate(company.fundingData.lastFundingRound.announcedOn)}
                </p>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
} 