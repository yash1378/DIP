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
  const [send_images, set_sendImages] = useState<ImageData>();
  const [data, setData] = useState<string>("");
  const Router = useRouter();


  // Fetch images from local storage

  const handleViewDetails = (algo: Algorithm) => {
    setSelectedAlgo(algo);
    console.log("Algorithm details:", JSON.stringify(algo, null, 2)); // Clear and formatted output
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
    const storedImages = localStorage.getItem("images");
    if (storedImages) {
      setImages(JSON.parse(storedImages));
    }

    fetchData();
  }, []);

  // New useEffect to handle updates to selectedAlgo
  useEffect(() => {
    if (selectedAlgo) {
      handleImageClick(send_images); // Call handleImageClick with updated state
      console.log(
        "Updated selectedAlgo:",
        JSON.stringify(selectedAlgo, null, 2)
      );
    }
  }, [selectedAlgo]); // Triggered whenever `selectedAlgo` changes

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

  const handleImageClick = async (image: ImageData | undefined) => {
    // Send the request to the backend with the image data and algorithm ID
    console.log(image);
    console.log("yes:" + selectedAlgo?.id);
    try {
      console.log(selectedAlgo);
      const response = await fetch(
        "http://localhost:5000/api/apply-algorithm",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            imageData: image?.data,
            algoId: selectedAlgo?.id,
          }),
        }
      );
      const data = await response.json();
      console.log("Response from backend:", data);

      // Save the data in localStorage using algoId as the key
      if (selectedAlgo?.id) {
        // Save the data in localStorage using algoId as the key
        const imageData = {
          processedImage: data.processedImage,  // The Base64 encoded image
          width: data.new_width,           // New width
          height: data.new_height         // New height
        };
    
        // Saving the object in localStorage with a unique key (selectedAlgo.id)
        localStorage.setItem(selectedAlgo.id, JSON.stringify(imageData));
    
        console.log(`Data saved to localStorage with key: ${selectedAlgo.id}`);
      } else {
        console.error("Algorithm ID (algoId) is missing in the response data.");
      }

      console.log("Data saved to localStorage");
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
                    onClick={() => {
                      console.log("Algorithm clicked:", algo); // Log the algorithm details here
                      Router.push(`/number?id=${algo.id}`);

                    }}
                    className="group flex items-center gap-2 bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white transition-all duration-300"
                  >
                    See the Processed Image
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </Button>
                  <Button
                    onClick={() => {
                      console.log("Algorithm clicked:", algo); // Log the algorithm details here
                      handleViewDetails(algo); // Call the function
                    }}
                    className="group flex items-center gap-2 bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white transition-all duration-300"
                  >
                    Apply this Algorithm
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}

        {/* Display Images if an algorithm is selected */}
        {/* {selectedAlgo && ( */}
        <div className="mt-8 space-y-4">
          <h2 className="text-2xl font-semibold text-gray-800">
            Images for {selectedAlgo?.name}
          </h2>
          <div className="grid grid-cols-3 gap-4">
            {images.map((image, index) => (
              <div
                key={index}
                className="cursor-pointer border-2 border-gray-200 rounded-lg overflow-hidden"
                onClick={() => {
                  set_sendImages((prev) => {
                    const updatedState = {
                      ...prev, // Spread the previous state to retain any other properties
                      data: image.data,
                      dimensions: image.dimensions,
                      name: image.name,
                    };

                    console.log("Updated send_images state:", updatedState); // Log the updated state
                    return updatedState; // Return the updated state
                  });
                }}
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
        {/* )} */}
      </div>
    </div>
  );
};

export default AlgorithmsDisplay;
