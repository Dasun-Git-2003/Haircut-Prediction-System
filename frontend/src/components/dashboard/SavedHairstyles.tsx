import React from 'react';
import { Card, CardContent } from '../ui/Card';
import { Button } from '../ui/Button';
import { Trash2 } from 'lucide-react';

interface SavedHairstylesProps {
  hairstyles: any[]; // Using any for mock
}

export default function SavedHairstyles({ hairstyles }: SavedHairstylesProps) {
  if (!hairstyles || hairstyles.length === 0) {
    return (
      <div className="text-center py-12 text-muted-foreground border border-dashed rounded-xl">
        <p>No saved hairstyles yet</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
      {hairstyles.map((style, i) => (
        <Card key={i} className="overflow-hidden group relative">
          <div className="absolute top-2 right-2 z-10 opacity-0 group-hover:opacity-100 transition-opacity">
            <Button variant="destructive" size="icon" className="h-8 w-8 rounded-full shadow-md">
              <Trash2 className="w-4 h-4" />
            </Button>
          </div>
          <div className="relative aspect-square overflow-hidden bg-muted">
            <img 
              src={`https://images.unsplash.com/photo-1593702275687-f8b402bf1fb5?w=400&q=80&random=${i}`} 
              alt="Saved style" 
              className="object-cover w-full h-full group-hover:scale-110 transition-transform duration-500"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent opacity-80" />
            <div className="absolute bottom-3 left-3 right-3 text-white">
              <h4 className="font-bold text-sm leading-tight mb-1">{style.name || 'Textured Crop'}</h4>
              <p className="text-xs text-white/70">Saved on {new Date().toLocaleDateString()}</p>
            </div>
            <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
              <span className="text-white text-xs font-medium backdrop-blur-md bg-white/20 px-3 py-1.5 rounded-full border border-white/30 cursor-pointer">
                View Try-On
              </span>
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
}
