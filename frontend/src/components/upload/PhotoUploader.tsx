import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Upload, X, Image as ImageIcon } from 'lucide-react';
import { Button } from '../ui/Button';
import { Card } from '../ui/Card';

interface PhotoUploaderProps {
  file: File | null;
  preview: string | null;
  onFileSelect: (file: File) => void;
  onClear: () => void;
  onAnalyze: () => void;
}

export default function PhotoUploader({ file, preview, onFileSelect, onClear, onAnalyze }: PhotoUploaderProps) {
  const [isDragging, setIsDragging] = useState(false);

  const handleFile = (selectedFile: File) => {
    if (selectedFile.size > 10 * 1024 * 1024) {
      alert("File is too large. Max size is 10MB");
      return;
    }
    onFileSelect(selectedFile);
  };

  const onDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const onDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: 0.1 }}
    >
      {!preview ? (
        <div
          onDragOver={onDragOver}
          onDragLeave={onDragLeave}
          onDrop={onDrop}
          className={`border-2 border-dashed rounded-2xl p-12 text-center transition-all ${
            isDragging ? 'border-primary bg-primary/5 scale-[1.02]' : 'border-border hover:border-primary/50'
          }`}
        >
          <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-6 text-primary">
            <Upload className="w-8 h-8" />
          </div>
          <h3 className="text-xl font-semibold mb-2">Drag & drop your photo</h3>
          <p className="text-muted-foreground text-sm mb-6">or click to browse from your device</p>
          
          <input
            type="file"
            id="file-upload"
            className="hidden"
            accept="image/jpeg,image/png,image/webp"
            onChange={(e) => e.target.files && handleFile(e.target.files[0])}
          />
          <label htmlFor="file-upload">
            <Button variant="secondary" className="cursor-pointer" asChild>
              <span>Select Image</span>
            </Button>
          </label>
          
          <p className="text-xs text-muted-foreground mt-4">JPEG, PNG, WebP up to 10MB.</p>
        </div>
      ) : (
        <Card className="overflow-hidden glass relative group max-w-md mx-auto">
          <div className="relative aspect-[3/4] w-full overflow-hidden bg-black/5">
            <img src={preview} alt="Preview" className="object-cover w-full h-full" />
            <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-4">
              <Button variant="destructive" size="icon" onClick={onClear} className="rounded-full">
                <X className="w-4 h-4" />
              </Button>
            </div>
          </div>
          <div className="p-4 bg-background">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2 text-sm font-medium truncate">
                <ImageIcon className="w-4 h-4 text-muted-foreground" />
                <span className="truncate">{file?.name}</span>
              </div>
              <span className="text-xs text-muted-foreground">{file ? (file.size / 1024 / 1024).toFixed(2) : 0} MB</span>
            </div>
            <Button className="w-full" size="lg" onClick={onAnalyze}>
              Analyze My Photo
            </Button>
          </div>
        </Card>
      )}
    </motion.div>
  );
}
