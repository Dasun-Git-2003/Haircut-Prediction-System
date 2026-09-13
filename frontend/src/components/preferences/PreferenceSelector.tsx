import React from 'react';
import { motion } from 'framer-motion';

interface PreferenceSelectorProps {
  title: string;
  options: string[];
  selected: string[];
  onChange: (option: string) => void;
  multiSelect?: boolean;
}

const formatLabel = (str: string) => {
  if (str === 'no_preference') return 'No Preference';
  return str.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
};

export default function PreferenceSelector({ title, options, selected, onChange, multiSelect = true }: PreferenceSelectorProps) {
  return (
    <div className="mb-8">
      <h3 className="text-lg font-semibold mb-3">{title}</h3>
      <div className="flex flex-wrap gap-2">
        {options.map(opt => {
          const isSelected = selected.includes(opt);
          return (
            <button
              key={opt}
              onClick={() => onChange(opt)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 border ${
                isSelected
                  ? 'bg-primary border-primary text-primary-foreground shadow-md scale-105'
                  : 'bg-background border-border text-foreground hover:border-primary/50 hover:bg-primary/5'
              }`}
            >
              {formatLabel(opt)}
              {isSelected && multiSelect && opt !== 'no_preference' && (
                <span className="ml-2 text-[10px] opacity-70">✕</span>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}
