import React from 'react';
import { Card, CardContent } from '../ui/Card';
import { UserCheck } from 'lucide-react';

interface StyleProfileProps {
  profile: {
    face_shape: string;
    hair_type: string;
    hair_density: string;
    hair_length?: string;
  };
}

export default function StyleProfile({ profile }: StyleProfileProps) {
  return (
    <div className="mb-12">
      <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
        <UserCheck className="text-primary" /> Your Style Profile
      </h2>
      <p className="text-muted-foreground mb-6">Based on your analysis</p>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Face Shape', value: profile.face_shape },
          { label: 'Hair Type', value: profile.hair_type },
          { label: 'Density', value: profile.hair_density },
          { label: 'Length', value: profile.hair_length || 'Medium' },
        ].map((item, i) => (
          <Card key={i} className="bg-gradient-to-br from-primary/5 to-secondary/5 border-white/20 glass hover:scale-[1.02] transition-transform">
            <CardContent className="p-4 flex flex-col items-center justify-center text-center h-full">
              <span className="text-sm text-muted-foreground mb-1">{item.label}</span>
              <span className="text-lg font-semibold text-foreground">{item.value}</span>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
