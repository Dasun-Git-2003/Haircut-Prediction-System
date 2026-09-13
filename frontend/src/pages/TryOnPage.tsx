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
  const allStyles = location.state?.allStyles || (initialStyle ? [initialStyle] : []);
  const userPhotoUrl = location.state?.userPhotoUrl;

  const [currentStyle, setCurrentStyle] = useState(initialStyle);
  const [isGenerating, setIsGenerating] = useState(true);
  const [generatedPreviewUrl, setGeneratedPreviewUrl] = useState<string | null>(null);

  const fetchTryOnPreview = async (styleToTry: any) => {
    setIsGenerating(true);
    try {
      // If we have a valid recommendation ID from backend
      if (styleToTry?.id && styleToTry.id.length > 5) {
        const response = await fetch(`/api/tryon/generate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ recommendation_id: styleToTry.id })
        });
        if (response.ok) {
          const data = await response.json();
          if (data.generated_image_url) {
            setGeneratedPreviewUrl(data.generated_image_url);
            setIsGenerating(false);
            return;
          }
        }
      }
    } catch (err) {
      console.warn('Backend try-on API call failed, using style reference:', err);
    }

    // Smooth UI timer fallback
    setTimeout(() => {
      setGeneratedPreviewUrl(styleToTry?.img || null);
      setIsGenerating(false);
    }, 1800);
  };

  useEffect(() => {
    if (!currentStyle) {
      navigate('/results');
      return;
    }
    fetchTryOnPreview(currentStyle);
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
        beforeImage={userPhotoUrl}
        afterImage={generatedPreviewUrl || currentStyle?.img}
        isGenerating={isGenerating}
        onPrevious={handlePrevious}
        onNext={handleNext}
        onRegenerate={() => fetchTryOnPreview(currentStyle)}
      />
      
      <HairstyleCompare 
        tryOnResults={allStyles}
        originalImage={userPhotoUrl || "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=800&q=80"}
        onSelect={(style) => setCurrentStyle(style)}
        activeId={currentStyle.id}
      />
    </div>
  );
}
