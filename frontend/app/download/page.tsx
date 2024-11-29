'use client';

import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { CheckCircle2, XCircle } from 'lucide-react';

interface ImageData {
  data: string; // base64 string
  dimensions: string; 
  name: string;
}

export default function ImageProcessingPage() {
  const [images, setImages] = useState<ImageData[]>([]);
  const [selectedImages, setSelectedImages] = useState<ImageData[]>([]);
  const [processingResult, setProcessingResult] = useState<string | null>(null);

  useEffect(() => {
    // Retrieve images from localStorage
    const storedImages = localStorage.getItem('images');
    if (storedImages) {
      setImages(JSON.parse(storedImages));
    }
  }, []);

  const handleImageSelect = (image: ImageData) => {
    // If image already selected, deselect it
    if (selectedImages.some(selected => selected.data === image.data)) {
      setSelectedImages(selectedImages.filter(selected => selected.data !== image.data));
      return;
    }

    // If less than 2 images selected, add the image
    if (selectedImages.length < 2) {
      setSelectedImages([...selectedImages, image]);
    } else {
      // If already 2 images selected, replace the first one
      setSelectedImages([selectedImages[1], image]);
    }
  };

  const processImage = async (processType: 'contrast' | 'entropy' | 'snr') => {
    if (selectedImages.length !== 2) {
      alert('Please select two images');
      return;
    }

    console.log(selectedImages)
    console.log(processType)
    // return

    try {
      const response = await fetch('http://localhost:5000/api/apply-metrics', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          images: selectedImages.map(img => img.data),
          processType: processType
        })
      });

      const data = await response.json();
      console.log(data)
      alert("value for first image = "+data.a+" value for second image = "+data.b)
      // Store the processed image in localStorage with a unique key
    //   const processedImageKey = `processed-${processType}-${Date.now()}`;
    //   localStorage.setItem(processedImageKey, JSON.stringify({
    //     processedImage: data.processedImage,
    //     processType: processType
    //   }));

    //   setProcessingResult(data.processedImage);
    } catch (error) {
      console.error('Error processing images:', error);
      alert('Failed to process images');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-8">
      <div className="max-w-6xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">
          Image Processing Studio
        </h1>

        {/* Selected Images Display */}
        <div className="flex justify-center space-x-4 mb-8">
          {selectedImages.map((image, index) => (
            <Card key={index} className="w-1/3 shadow-lg">
              <CardContent className="p-4">
                <img 
                  src={image.data} 
                  alt={image.name} 
                  className="w-full h-64 object-cover rounded-lg"
                />
                <div className="mt-2 text-center">
                  <p className="text-sm text-gray-600">{image.name}</p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Processing Buttons */}
        <div className="flex justify-center space-x-4 mb-8">
          <Button 
            onClick={() => processImage('contrast')}
            disabled={selectedImages.length !== 2}
            className="bg-green-500 hover:bg-green-600"
          >
            Compare the Contrast
          </Button>
          <Button 
            onClick={() => processImage('entropy')}
            disabled={selectedImages.length !== 2}
            className="bg-blue-500 hover:bg-blue-600"
          >
            Compare the Entropy
          </Button>
          <Button 
            onClick={() => processImage('snr')}
            disabled={selectedImages.length !== 2}
            className="bg-purple-500 hover:bg-purple-600"
          >
            Compare the SNR
          </Button>
        </div>

        {/* Image Gallery */}
        <div className="grid grid-cols-4 gap-4">
          {images.map((image, index) => (
            <div 
              key={index} 
              onClick={() => handleImageSelect(image)}
              className={`relative cursor-pointer transition-all duration-300 ${
                selectedImages.some(selected => selected.data === image.data) 
                  ? 'border-4 border-green-500 scale-105' 
                  : 'hover:scale-105'
              }`}
            >
              <img 
                src={image.data} 
                alt={image.name} 
                className="w-full h-48 object-cover rounded-lg"
              />
              <div className="absolute top-2 right-2">
                {selectedImages.some(selected => selected.data === image.data) ? (
                  <CheckCircle2 className="text-green-500 w-6 h-6" />
                ) : null}
              </div>
              <p className="text-center mt-2 text-sm text-gray-600">{image.name}</p>
            </div>
          ))}
        </div>

        {/* Processed Image Result */}
        {processingResult && (
          <div className="mt-8">
            <h2 className="text-2xl font-semibold text-center mb-4">Processed Result</h2>
            <div className="flex justify-center">
              <img 
                src={processingResult} 
                alt="Processed Result" 
                className="max-w-full max-h-[500px] rounded-lg shadow-xl"
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}