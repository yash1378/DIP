"use client";

import React, { useState, useEffect } from "react";
import { Upload, File, Video, Download, Info } from "lucide-react";

// const algorithms = [
//   {"id": 1, "name": "Bicubic Interpolation", "description": "A high-quality resampling technique using cubic splines.", "complexity": "O(n^2)", "category": "Image Processing"},
//   {"id": 2, "name": "Bilinear Interpolation", "description": "A linear resampling technique.", "complexity": "O(n)", "category": "Image Processing"},
//   {"id": 3, "name": "Fourier Transform", "description": "A method to transform a signal into its frequency components.", "complexity": "O(n log n)", "category": "Signal Processing"},
//   {"id": 4, "name": "Iterative Backprojection", "description": "An iterative algorithm for reconstructing images.", "complexity": "O(n^2)", "category": "Image Reconstruction"},
//   {"id": 5, "name": "Lanczos Resampling", "description": "A high-quality resampling technique using sinc functions.", "complexity": "O(n log n)", "category": "Image Processing"},
//   {"id": 6, "name": "Nearest Neighbor Interpolation", "description": "A simple interpolation technique.", "complexity": "O(1)", "category": "Image Processing"},
//   {"id": 7, "name": "Non-Local Means", "description": "A noise reduction algorithm.", "complexity": "O(n^2)", "category": "Image Denoising"},
//   {"id": 8, "name": "Total Variation Denoising", "description": "An image denoising technique.", "complexity": "O(n log n)", "category": "Image Denoising"},
//   {"id": 9, "name": "Wavelet Transform", "description": "A transformation technique for compression and denoising.", "complexity": "O(n)", "category": "Signal Processing"}
// ];

// TypeScript interfaces
interface Algorithm {
  id: string;
  name: string;
  description: string;
  complexity: string;
  category: string;
  performance: number;
  tags: string[];
}

const UploadVideo: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [algorithms, setAlgorithms] = useState<Algorithm[]>([]);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState<string | null>(
    null
  );
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);
  const [processedVideo, setProcessedVideo] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          "http://localhost:5000/api/list_super_resolution_methods"
        );
        const data = await response.json();
        console.log(data);
        setAlgorithms(data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  const handleAlgorithmSelect = (algorithmId: string) => {
    setSelectedAlgorithm(algorithmId);
  };

  const handleUpload = async () => {
    if (!selectedFile || !selectedAlgorithm) {
      alert("Please select both a video file and a processing algorithm.");
      return;
    }
  
    setUploadStatus("Uploading...");
  
    try {
      const videoBase64 = await fileToBase64(selectedFile);
      
      const response = await fetch("http://localhost:5000/api/video", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ 
          video: videoBase64,
          algorithm: selectedAlgorithm 
        }),
      });
  
      const responseData = await response.json();
  
      if (response.ok) {
        setUploadStatus("Upload successful!");
        if (responseData.processed_video) {
          // If it's a base64 string, append it to the source in the correct format
          if (responseData.processed_video.startsWith('data:video/mp4;base64')) {
            setProcessedVideo(responseData.processed_video);  // Directly use the base64 string
          } else {
            setProcessedVideo(responseData.processed_video);  // Assume it's a URL
          }
        }
      } else {
        setUploadStatus(`Upload failed: ${responseData.error}`);
      }
    } catch (error) {
      console.error("Error uploading video:", error);
      setUploadStatus("Upload failed due to a network error.");
    }
  };
  

  const fileToBase64 = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result as string);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 to-purple-200 flex items-center justify-center p-6">
      <div className="bg-white shadow-2xl rounded-2xl p-8 w-full max-w-xl transform transition-all hover:scale-105 duration-300">
        <h1 className="text-3xl font-bold text-center text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-600 mb-6">
          Video Processor
        </h1>

        <div className="flex flex-col items-center space-y-4">
          <label htmlFor="videoUpload" className="w-full cursor-pointer">
            <input
              id="videoUpload"
              type="file"
              accept="video/*"
              onChange={handleFileChange}
              className="hidden"
            />
            <div
              className={`
              w-full 
              border-2 border-dashed 
              ${
                selectedFile
                  ? "border-green-500 bg-green-50"
                  : "border-gray-300 hover:border-blue-500"
              } 
              rounded-lg 
              p-6 
              text-center 
              transition-all 
              duration-300 
              group
            `}
            >
              <File
                className={`
                  mx-auto 
                  mb-4 
                  ${
                    selectedFile
                      ? "text-green-500"
                      : "text-gray-400 group-hover:text-blue-500"
                  } 
                  transition-colors 
                  duration-300
                `}
                size={48}
              />
              <p className="text-sm text-gray-600">
                {selectedFile
                  ? `Selected: ${selectedFile.name}`
                  : "Click to select a video file"}
              </p>
            </div>
          </label>

          <div className="w-full">
            <h2 className="text-lg font-semibold mb-3 text-gray-700">
              Select Processing Algorithm
            </h2>
            <div className="grid grid-cols-2 gap-4">
              {algorithms.map((algo) => (
                <button
                  key={algo.id}
                  onClick={() => handleAlgorithmSelect(algo.id)}
                  className={`
                    p-4 
                    rounded-lg 
                    border-2 
                    text-left 
                    transition-all 
                    duration-300 
                    relative
                    ${
                      selectedAlgorithm === algo.id
                        ? "border-blue-500 bg-blue-50 ring-2 ring-blue-300"
                        : "border-gray-200 hover:border-blue-300"
                    }
                  `}
                >
                  {selectedAlgorithm === algo.id && (
                    <div className="absolute top-2 right-2 text-blue-500">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-6 w-6"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M5 13l4 4L19 7"
                        />
                      </svg>
                    </div>
                  )}
                  <h3 className="font-bold text-sm mb-1">{algo.name}</h3>
                  <p className="text-xs text-gray-500">{algo.description}</p>
                  <div className="mt-2 flex justify-between text-xs">
                    <span className="bg-gray-100 px-2 py-1 rounded">
                      {algo.complexity}
                    </span>
                    <span className="text-gray-500">{algo.category}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>

          <button
            onClick={handleUpload}
            disabled={!selectedFile || !selectedAlgorithm}
            className={`
              w-full 
              flex 
              items-center 
              justify-center 
              gap-2 
              py-3 
              rounded-lg 
              text-white 
              font-semibold 
              transition-all 
              duration-300 
              ${
                selectedFile && selectedAlgorithm
                  ? "bg-gradient-to-r from-blue-500 to-purple-600 hover:scale-105 shadow-lg"
                  : "bg-gray-300 cursor-not-allowed"
              }
            `}
          >
            <Upload size={20} />
            Upload and Process
          </button>

          {uploadStatus && (
            <div
              className={`
              w-full 
              p-3 
              rounded-lg 
              text-center 
              ${
                uploadStatus.includes("successful")
                  ? "bg-green-100 text-green-700"
                  : "bg-red-100 text-red-700"
              }
            `}
            >
              {uploadStatus}
            </div>
          )}

          {processedVideo && (
            <div className="w-full space-y-4">
              <div className="bg-gray-100 rounded-lg p-4">
                <video
                  src={processedVideo}
                  controls
                  className="w-full rounded-lg shadow-md"
                />
              </div>
              <a
                href={processedVideo}
                download="processed_video.mp4"
                className="block"
              >
                <button
                  className="
        w-full 
        flex 
        items-center 
        justify-center 
        gap-2 
        py-3 
        rounded-lg 
        bg-gradient-to-r 
        from-green-500 
        to-teal-600 
        text-white 
        font-semibold 
        hover:scale-105 
        transition-all 
        duration-300 
        shadow-lg
      "
                >
                  <Download size={20} />
                  Download Processed Video
                </button>
              </a>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UploadVideo;
