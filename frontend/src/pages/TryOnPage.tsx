import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { Button } from '../components/ui/Button';
import TryOnViewer from '../components/tryon/TryOnViewer';
import HairstyleCompare from '../components/tryon/HairstyleCompare';

export default function TryOnPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const initialStyle = location.state?.style;
  const allStyles = location.state?.allStyles || [initialStyle];

  const [currentStyle, setCurrentStyle] = useState(initialStyle);
  const [isGenerating, setIsGenerating] = useState(true);

  useEffect(() => {
    if (!currentStyle) {
      navigate('/results');
      return;
    }
    setIsGenerating(true);
    const timer = setTimeout(() => setIsGenerating(false), 2000);
    return () => clearTimeout(timer);
  }, [currentStyle, navigate]);

  if (!currentStyle) return null;

  const currentIndex = allStyles.findIndex((s: any) => s.id === currentStyle.id);
  
  const handlePrevious = currentIndex > 0 ? () => setCurrentStyle(allStyles[currentIndex - 1]) : undefined;
  const handleNext = currentIndex < allStyles.length - 1 ? () => setCurrentStyle(allStyles[currentIndex + 1]) : undefined;

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl flex flex-col h-full">
      <Button variant="ghost" className="mb-6 gap-2 w-fit" onClick={() => navigate('/results')}>
        <ArrowLeft className="w-4 h-4" /> Back to Results
      </Button>

      <TryOnViewer 
        tryOnData={currentStyle} 
        isGenerating={isGenerating}
        onPrevious={handlePrevious}
        onNext={handleNext}
        onRegenerate={() => {
          setIsGenerating(true);
          setTimeout(() => setIsGenerating(false), 2000);
        }}
      />
      
      <HairstyleCompare 
        tryOnResults={allStyles}
        originalImage="https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=800&q=80"
        onSelect={(style) => setCurrentStyle(style)}
        activeId={currentStyle.id}
      />
    </div>
  );
}
