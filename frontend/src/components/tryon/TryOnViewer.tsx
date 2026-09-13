import React from 'react';
import { Download, Share2, Heart, RefreshCcw, ArrowLeft, ArrowRight, Sparkles, CheckCircle2 } from 'lucide-react';
import { Button } from '../ui/Button';
import BeforeAfterSlider from './BeforeAfterSlider';
import { motion } from 'framer-motion';

interface TryOnViewerProps {
  tryOnData: any;
  beforeImage?: string;
  afterImage?: string;
  isGenerating?: boolean;
  onPrevious?: () => void;
  onNext?: () => void;
  onRegenerate?: () => void;
  onSave?: () => void;
}

export default function TryOnViewer({
  tryOnData,
  beforeImage,
  afterImage,
  isGenerating,
  onPrevious,
  onNext,
  onRegenerate,
  onSave
}: TryOnViewerProps) {
  const originalPhoto = beforeImage || "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=800&q=80";
  const generatedPhoto = afterImage || tryOnData?.img || originalPhoto;

  return (
    <div className="grid lg:grid-cols-3 gap-8 items-start">
      <div className="lg:col-span-2 relative aspect-[3/4] md:aspect-[4/3] rounded-xl overflow-hidden glass border-white/20">
        {isGenerating ? (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-background/80 backdrop-blur-sm z-20">
            <Sparkles className="w-12 h-12 text-primary animate-bounce mb-4" />
            <h3 className="text-xl font-bold mb-2">Generating AI Preview with Gemini...</h3>
            <p className="text-sm text-muted-foreground max-w-xs text-center">
              Applying {tryOnData?.name || 'this hairstyle'} to your photograph.
            </p>
          </div>
        ) : (
          <BeforeAfterSlider 
            beforeImage={originalPhoto} 
            afterImage={generatedPhoto} 
          />
        )}
      </div>

      <div className="space-y-6">
        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}>
          <h1 className="text-3xl font-bold mb-2">{tryOnData?.name}</h1>
          <div className="flex gap-2 mb-6">
            <span className="px-2.5 py-1 bg-primary/10 text-primary text-sm font-medium rounded-md">
              {tryOnData?.match || 95}% Match
            </span>
            <span className="px-2.5 py-1 bg-muted text-foreground text-sm font-medium rounded-md capitalize">
              {tryOnData?.maintenance || 'Medium'} Maintenance
            </span>
          </div>

          <div className="space-y-3 mb-8">
            <h4 className="font-medium">Why it works for you:</h4>
            {[
              'Balances your face shape proportions',
              'Works naturally with your hair texture',
              'Easy to maintain with your lifestyle'
            ].map((reason, i) => (
              <div key={i} className="flex items-start gap-2 text-sm text-muted-foreground">
                <CheckCircle2 className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                <span>{reason}</span>
              </div>
            ))}
          </div>

          <div className="space-y-4">
            <Button className="w-full gap-2 h-12" size="lg" disabled={isGenerating}>
              <Download className="w-5 h-5" /> Download Result
            </Button>
            <div className="grid grid-cols-2 gap-4">
              <Button variant="outline" className="gap-2 h-12" disabled={isGenerating} onClick={onSave}>
                <Heart className="w-5 h-5" /> Save
              </Button>
              <Button variant="outline" className="gap-2 h-12" disabled={isGenerating}>
                <Share2 className="w-5 h-5" /> Share
              </Button>
            </div>
            <Button 
              variant="ghost" 
              className="w-full gap-2" 
              disabled={isGenerating} 
              onClick={onRegenerate}
            >
              <RefreshCcw className="w-4 h-4" /> Regenerate Preview
            </Button>

            <div className="flex justify-between pt-4 border-t">
              <Button variant="ghost" size="sm" onClick={onPrevious} disabled={!onPrevious}>
                <ArrowLeft className="w-4 h-4 mr-2" /> Previous Style
              </Button>
              <Button variant="ghost" size="sm" onClick={onNext} disabled={!onNext}>
                Next Style <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
