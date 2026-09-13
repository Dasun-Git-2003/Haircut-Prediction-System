import React from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';
import { Sparkles, CheckCircle2, Info } from 'lucide-react';

interface RecommendationCardProps {
  style: any;
  rank?: number;
  onTryOn: () => void;
}

export default function RecommendationCard({ style, rank, onTryOn }: RecommendationCardProps) {
  const isHighMatch = style.match >= 85;
  const isMedMatch = style.match >= 70 && style.match < 85;

  return (
    <Card className="overflow-hidden flex flex-col h-full hover:shadow-xl transition-all duration-300 border-white/10 relative glass group">
      {rank && (
        <div className="absolute top-4 left-4 z-20 w-8 h-8 rounded-full bg-background/80 backdrop-blur-md flex items-center justify-center font-bold text-sm shadow-md">
          #{rank}
        </div>
      )}
      <div className="absolute top-4 right-4 z-20">
        <Badge 
          variant={isHighMatch ? 'success' : isMedMatch ? 'warning' : 'default'} 
          className="shadow-lg backdrop-blur-md bg-opacity-90"
        >
          {style.match}% Match
        </Badge>
      </div>

      <div className="relative aspect-square overflow-hidden bg-muted">
        <img 
          src={style.img} 
          alt={style.name} 
          className="object-cover w-full h-full group-hover:scale-105 transition-transform duration-500" 
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-4">
          <Button className="w-full gap-2" variant="secondary" onClick={onTryOn}>
            <Sparkles className="w-4 h-4" /> Try Virtual Preview
          </Button>
        </div>
      </div>
      
      <CardContent className="p-6 flex-1 flex flex-col">
        <div className="mb-2">
          <h3 className="text-xl font-bold">{style.name}</h3>
        </div>
        
        <div className="flex flex-wrap gap-2 mb-4 mt-2">
          <Badge variant="secondary" className="text-xs capitalize">{style.maintenance} Maintenance</Badge>
          {style.tags?.map((tag: string) => (
            <Badge key={tag} variant="outline" className="text-xs capitalize">{tag}</Badge>
          ))}
        </div>

        <div className="mt-auto space-y-2 mb-6">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <CheckCircle2 className="w-4 h-4 text-green-500" /> Face shape & hair type match
          </div>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Info className="w-4 h-4 text-primary" /> Balances facial proportions
          </div>
        </div>

        <Button className="w-full mt-auto gap-2 lg:hidden" onClick={onTryOn}>
          <Sparkles className="w-4 h-4" />
          Try This Style
        </Button>
      </CardContent>
    </Card>
  );
}
