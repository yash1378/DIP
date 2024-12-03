'use client'
import React, { useState, useRef, ChangeEvent } from 'react';
import { 
  Button, 
  Typography, 
  Paper, 
  CircularProgress 
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import DownloadIcon from '@mui/icons-material/Download';
import { motion } from 'framer-motion';

const ImageUploadPage: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [processedImage, setProcessedImage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://localhost:5000/api/dlbased', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to upload image');
      }

      const data = await response.json();
      if (data.processed_image) {
        setProcessedImage(data.processed_image);  // Expecting base64 data in the response
      }
    } catch (error) {
      console.error('Upload failed', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = () => {
    if (processedImage) {
      // Convert base64 string to a Blob
      const byteCharacters = atob(processedImage.split(',')[1]);
      const byteArrays = [];
      for (let offset = 0; offset < byteCharacters.length; offset += 1024) {
        const slice = byteCharacters.slice(offset, offset + 1024);
        const byteNumbers = new Array(slice.length);
        for (let i = 0; i < slice.length; i++) {
          byteNumbers[i] = slice.charCodeAt(i);
        }
        byteArrays.push(new Uint8Array(byteNumbers));
      }

      // Create a Blob from the byte arrays
      const blob = new Blob(byteArrays, { type: 'image/png' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = 'processed-image.png';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 to-purple-200 flex items-center justify-center p-6">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md"
      >
        <Paper 
          elevation={12} 
          className="p-6 rounded-2xl bg-white/90 backdrop-blur-lg shadow-2xl"
        >
          <Typography 
            variant="h4" 
            component="h1" 
            className="text-center mb-6 text-gray-800 font-bold"
          >
            Image Processor
          </Typography>

          <input 
            type="file" 
            ref={fileInputRef}
            onChange={handleFileChange}
            accept="image/*"
            className="hidden"
          />

          <Button 
            variant="contained" 
            color="primary"
            startIcon={<CloudUploadIcon />}
            onClick={() => fileInputRef.current?.click()}
            className="w-full mb-4"
          >
            Select Image
          </Button>

          {selectedFile && (
            <div className="mb-4 text-center">
              <Typography variant="body2" color="textSecondary" className="mb-2">
                {selectedFile.name}
              </Typography>

              <Button 
                variant="contained" 
                color="success"
                onClick={handleUpload}
                disabled={isLoading}
                className="w-full mb-4"
              >
                {isLoading ? <CircularProgress size={24} /> : 'Process Image'}
              </Button>
            </div>
          )}

          {processedImage && (
            <div className="text-center">
              <img 
                src={`data:image/png;base64,${processedImage}`} 
                alt="Processed Image" 
                className="w-full max-h-64 object-contain mb-4"
              />

              <Button 
                variant="contained" 
                color="secondary"
                startIcon={<DownloadIcon />}
                onClick={handleDownload}
                className="w-full"
              >
                Download Processed Image
              </Button>
            </div>
          )}
        </Paper>
      </motion.div>
    </div>
  );
};

export default ImageUploadPage;
