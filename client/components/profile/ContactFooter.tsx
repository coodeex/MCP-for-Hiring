'use client';

import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Mail, Copy, CheckCircle, Linkedin } from 'lucide-react';

interface ContactFooterProps {
  candidate: {
    email: string;
    linkedInUrl: string;
  };
}

export function ContactFooter({ candidate }: ContactFooterProps) {
  const [copied, setCopied] = useState(false);

  const copyEmail = async () => {
    await navigator.clipboard.writeText(candidate.email);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <footer className="border-t bg-muted/50">
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          {/* Contact Actions */}
          <div className="flex flex-wrap gap-4">
            <Button variant="outline" onClick={copyEmail}>
              <Mail className="w-4 h-4 mr-2" />
              {copied ? <CheckCircle className="w-4 h-4 mr-2 text-green-500" /> : <Copy className="w-4 h-4 mr-2" />}
              {copied ? 'Copied!' : 'Copy Email'}
            </Button>
            <Button asChild>
              <a href={candidate.linkedInUrl} target="_blank" rel="noopener noreferrer" className="flex items-center">
                <Linkedin className="w-4 h-4 mr-2" />
                View on LinkedIn
              </a>
            </Button>
          </div>

          {/* Legal Links */}
          <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
            <a href="#" className="hover:text-foreground transition-colors">Privacy Policy</a>
            <span>•</span>
            <a href="#" className="hover:text-foreground transition-colors">Terms of Service</a>
            <span>•</span>
            <a href="#" className="hover:text-foreground transition-colors">Data Source</a>
          </div>
        </div>
      </div>
    </footer>
  );
} 