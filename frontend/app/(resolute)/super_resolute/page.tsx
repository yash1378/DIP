"use client";
import React, { useEffect, useState } from "react";
import {
  ChevronRight,
  Sparkles,
  Code2,
  Cpu,
  BarChart2,
  ArrowRight,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useRouter } from "next/navigation";

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

interface ImageData {
  data: string; // base64 string
  dimensions: string; // e.g., "1920x1080"
  name: string; // image name
}

const AlgorithmsDisplay = () => {
  const [algorithms, setAlgorithms] = useState<Algorithm[]>([]);
  const [selectedAlgo, setSelectedAlgo] = useState<Algorithm | null>(null);
  const [images, setImages] = useState<ImageData[]>([]);
  const Router = useRouter();

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

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case "Image Processing":
        return <Sparkles className="w-5 h-5" />;
      case "Machine Learning":
        return <Cpu className="w-5 h-5" />;
      case "Quantum Computing":
        return <Code2 className="w-5 h-5" />;
      default:
        return <BarChart2 className="w-5 h-5" />;
    }
  };

  const getPerformanceColor = (performance: number) => {
    if (performance >= 95) return "text-green-500";
    if (performance >= 85) return "text-blue-500";
    return "text-yellow-500";
  };

  const handleViewDetails = (algo: Algorithm) => {
    setSelectedAlgo(algo);
    // Fetch images from local storage
    const storedImages = localStorage.getItem("images");
    if (storedImages) {
      setImages(JSON.parse(storedImages));
    }
  };

  const handleImageClick = async (image: ImageData) => {
    // Send the request to the backend with the image data and algorithm ID
    try {
      const response = await fetch("http://localhost:5000/api/apply-algorithm", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          imageData: image.data,
          algoId: selectedAlgo?.id,
        }),
      });
      const data = await response.json();
      console.log("Response from backend:", data);
    } catch (error) {
      console.error("Error sending image to backend:", error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-8">
      <div className="max-w-5xl mx-auto space-y-6">
        {algorithms.map((algo) => (
          <Card
            key={algo.id}
            className="hover:shadow-xl transition-all duration-300 border-0 backdrop-blur-sm bg-white/90"
          >
            <CardContent className="p-6">
              <div className="grid grid-cols-2 gap-6">
                {/* Left Column */}
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    {getCategoryIcon(algo.category)}
                    <span className="text-sm font-medium text-gray-500">
                      {algo.category}
                    </span>
                  </div>
                  <h3 className="text-xl font-semibold text-gray-800">
                    {algo.name}
                  </h3>
                  <p className="text-gray-600">{algo.description}</p>
                  <div className="flex flex-wrap gap-2">
                    {algo.tags.map((tag, index) => (
                      <Badge
                        key={index}
                        variant="secondary"
                        className="bg-blue-50 hover:bg-blue-100 text-blue-700"
                      >
                        {tag}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Right Column */}
                <div className="flex flex-col justify-between items-end">
                  <div className="space-y-2 text-right">
                    <div className="text-sm text-gray-500">
                      Time Complexity:
                      <span className="ml-2 font-mono font-medium">
                        {algo.complexity}
                      </span>
                    </div>
                    <div className="flex items-center gap-2 justify-end">
                      <span className="text-sm text-gray-500">
                        Performance Score:
                      </span>
                      <span
                        className={`text-lg font-bold ${getPerformanceColor(
                          algo.performance
                        )}`}
                      >
                        {algo.performance}%
                      </span>
                    </div>
                  </div>

                  <Button
                    onClick={() => handleViewDetails(algo)}
                    className="group flex items-center gap-2 bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white transition-all duration-300"
                  >
                    View Details
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}

        {/* Display Images if an algorithm is selected */}
        {selectedAlgo && (
          <div className="mt-8 space-y-4">
            <h2 className="text-2xl font-semibold text-gray-800">
              Images for {selectedAlgo.name}
            </h2>
            <div className="grid grid-cols-3 gap-4">
              {images.map((image, index) => (
                <div
                  key={index}
                  className="cursor-pointer border-2 border-gray-200 rounded-lg overflow-hidden"
                  onClick={() => handleImageClick(image)}
                >
                  <img
                    src={image.data}
                    alt={image.name}
                    className="w-full h-auto"
                  />
                  <div className="p-2 text-center text-gray-600">
                    <span>{image.name}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AlgorithmsDisplay;
