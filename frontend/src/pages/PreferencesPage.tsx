import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Settings2 } from 'lucide-react';
import { Button } from '../components/ui/Button';
import PreferenceSelector from '../components/preferences/PreferenceSelector';

const preferencesConfig = [
  { id: 'preferred_length', label: 'Preferred Length', options: ['very_short', 'short', 'medium', 'long', 'no_preference'] },
  { id: 'maintenance', label: 'Maintenance Level', options: ['low', 'medium', 'high', 'no_preference'] },
  { id: 'style', label: 'Style Vibe', options: ['classic', 'modern', 'professional', 'casual', 'trendy', 'edgy', 'no_preference'] },
  { id: 'lifestyle', label: 'Lifestyle', options: ['office', 'university', 'everyday', 'formal', 'sporty', 'no_preference'] }
];

export default function PreferencesPage() {
  const navigate = useNavigate();
  const [selections, setSelections] = useState<Record<string, string[]>>({});

  const toggleSelection = (category: string, option: string) => {
    setSelections(prev => {
      const current = prev[category] || [];
      if (option === 'no_preference') {
        return { ...prev, [category]: ['no_preference'] };
      }
      
      const withoutNoPref = current.filter(o => o !== 'no_preference');
      if (withoutNoPref.includes(option)) {
        return { ...prev, [category]: withoutNoPref.filter(o => o !== option) };
      } else {
        return { ...prev, [category]: [...withoutNoPref, option] };
      }
    });
  };

  return (
    <div className="container mx-auto px-4 py-12 max-w-3xl">
      <div className="text-center mb-10">
        <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4 text-primary">
          <Settings2 className="w-8 h-8" />
        </div>
        <h1 className="text-3xl md:text-4xl font-bold mb-4">Customize Your Recommendations</h1>
        <p className="text-muted-foreground">Tell us what you're looking for to refine our AI suggestions.</p>
      </div>

      <div className="space-y-8 mb-12">
        {preferencesConfig.map((cat, idx) => (
          <motion.div key={cat.id} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: idx * 0.1 }}>
            <PreferenceSelector 
              title={cat.label} 
              options={cat.options} 
              selected={selections[cat.id] || []} 
              onChange={(opt) => toggleSelection(cat.id, opt)} 
            />
          </motion.div>
        ))}
      </div>

      <div className="flex flex-col sm:flex-row gap-4 justify-end border-t pt-8">
        <Button variant="ghost" size="lg" onClick={() => navigate('/results')}>Skip</Button>
        <Button size="lg" onClick={() => navigate('/results', { state: { preferences: selections } })}>
          Get Recommendations
        </Button>
      </div>
    </div>
  );
}
