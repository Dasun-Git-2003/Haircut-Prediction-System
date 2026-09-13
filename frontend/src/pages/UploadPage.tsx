import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import PhotoUploader from '../components/upload/PhotoUploader';

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleFileSelect = (selectedFile: File) => {
    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));
  };

  const handleClear = () => {
    setFile(null);
    setPreview(null);
  };

  const handleAnalyze = () => {
    if (!file) return;
    navigate('/analysis', { state: { file } });
  };

  return (
    <div className="container mx-auto px-4 py-12 max-w-4xl">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-10"
      >
        <h1 className="text-3xl md:text-4xl font-bold mb-4">Let's Get Started</h1>
        <p className="text-muted-foreground">Upload a clear photo of your face to begin the analysis.</p>
      </motion.div>

      <PhotoUploader 
        file={file}
        preview={preview}
        onFileSelect={handleFileSelect}
        onClear={handleClear}
        onAnalyze={handleAnalyze}
      />
    </div>
  );
}
