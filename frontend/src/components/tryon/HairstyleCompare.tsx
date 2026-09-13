import React from 'react';
import { motion } from 'framer-motion';

interface HairstyleCompareProps {
  tryOnResults: any[];
  originalImage: string;
  onSelect: (result: any) => void;
  activeId: string;
}

export default function HairstyleCompare({ tryOnResults, originalImage, onSelect, activeId }: HairstyleCompareProps) {
  if (!tryOnResults || tryOnResults.length === 0) return null;

  return (
    <div className="w-full mt-8">
      <h4 className="text-sm font-medium mb-3">Compare Styles</h4>
      <div className="flex gap-4 overflow-x-auto pb-4 hide-scrollbar snap-x">
        {/* Original */}
        <div className="snap-start shrink-0 flex flex-col items-center gap-2">
          <div className="w-20 h-20 rounded-lg overflow-hidden border-2 border-transparent bg-muted">
            <img src={originalImage} alt="Original" className="w-full h-full object-cover grayscale opacity-80" />
          </div>
          <span className="text-xs text-muted-foreground font-medium">Original</span>
        </div>
        
        {/* Generated Results */}
        {tryOnResults.map((result) => {
          const isActive = result.id === activeId;
          return (
            <div 
              key={result.id} 
              className="snap-start shrink-0 flex flex-col items-center gap-2 cursor-pointer"
              onClick={() => onSelect(result)}
            >
              <div className={`w-20 h-20 rounded-lg overflow-hidden border-2 transition-colors ${
                isActive ? 'border-primary shadow-[0_0_10px_rgba(124,58,237,0.5)]' : 'border-transparent hover:border-primary/50'
              }`}>
                <img src={result.img} alt={result.name} className="w-full h-full object-cover" />
              </div>
              <span className={`text-xs font-medium max-w-[80px] text-center truncate ${isActive ? 'text-primary' : 'text-muted-foreground'}`}>
                {result.name}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
