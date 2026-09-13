import React from 'react';
import { Card, CardContent } from '../ui/Card';
import { Sparkles, ChevronRight } from 'lucide-react';

interface AnalysisHistoryProps {
  history: any[]; // Using any for mock
}

export default function AnalysisHistory({ history }: AnalysisHistoryProps) {
  if (!history || history.length === 0) {
    return (
      <div className="text-center py-12 text-muted-foreground border border-dashed rounded-xl">
        <p>No past analyses found</p>
      </div>
    );
  }

  return (
    <div className="space-y-4 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-border before:to-transparent">
      {history.map((item, i) => (
        <div key={i} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
          <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-background bg-secondary/10 text-secondary shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow-sm z-10">
            <Sparkles className="w-4 h-4" />
          </div>
          
          <Card className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] hover:shadow-md transition-shadow cursor-pointer glass">
            <CardContent className="p-4 flex items-center gap-4">
              <div className="w-16 h-16 rounded-md bg-muted overflow-hidden shrink-0">
                <img 
                  src={`https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=100&q=80&random=${i}`} 
                  alt="Original" 
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between mb-1">
                  <h4 className="font-semibold text-sm truncate">Analysis #{history.length - i}</h4>
                  <span className="text-xs text-muted-foreground">{new Date().toLocaleDateString()}</span>
                </div>
                <p className="text-xs text-muted-foreground truncate mb-1">
                  {item.face_shape || 'Oval'} Face • {item.hair_type || 'Wavy'} Hair
                </p>
                <div className="text-xs text-primary font-medium flex items-center">
                  View Results <ChevronRight className="w-3 h-3 ml-0.5" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      ))}
    </div>
  );
}
