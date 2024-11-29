'use client'
import React, { useEffect, useState } from 'react';
import { 
  ArrowRight,
  Wand2,
  Sliders,
  Palette,
  Layers,
  SunMoon,
  Binary,
  Contrast
} from 'lucide-react';
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useRouter } from 'next/navigation';

interface ProcessingStep {
  id: string;
  name: string;
  description: string;
  category: string;
  complexity:string;
  tags: string[];
}

interface ImageData {
  data: string; // base64 string
  dimensions: string; // e.g., "1920x1080"
  name: string; // image name
}

const PostProcessingDisplay = () => {
  const[ProcessStep, setProcessStep] = useState<ProcessingStep | null>(null);
  const [steps, setSteps] = useState<ProcessingStep[]>([]);
  const [images, setImages] = useState<ImageData[]>([]);
  const [send_images, set_sendImages] = useState<ImageData>();
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:5000/api/list_post_processing_steps");
        const data = await response.json();
        console.log(data); // To inspect the structure and data
        setSteps(data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    console.log("clicked")
    if (ProcessStep) {
      handleImageClick(send_images); // Call handleImageClick with updated state
      console.log(
        "Updated selectedAlgo:",
        JSON.stringify(ProcessStep, null, 2)
      );
    }
  }, [ProcessStep])

  const handleViewDetails = (algo: ProcessingStep) => {
    setProcessStep(algo);
    console.log("Algorithm details:", JSON.stringify(algo, null, 2)); // Clear and formatted output
  };
 
  const navigate = useRouter();

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case "Color Correction":
        return <Palette className="w-5 h-5" />;
      case "Detail Enhancement":
        return <Wand2 className="w-5 h-5" />;
      case "Tone Adjustment":
        return <SunMoon className="w-5 h-5" />;
      case "Image Cleanup":
        return <Layers className="w-5 h-5" />;
      default:
        return <Binary className="w-5 h-5" />;
    }
  };
  const convertToBase64Format = (base64String:string)=>{
    // Prefix the Base64 string with the data URI scheme
    const mimeType = 'data:image/png;base64,';
  
    // Concatenate the MIME type and the Base64 string
    const formattedBase64String = mimeType + base64String;
  
    return formattedBase64String;
  }
  
  const getImpactColor = (impact: string) => {
    switch (impact) {
      case "High":
        return "bg-gradient-to-r from-emerald-400 to-teal-400";
      case "Medium":
        return "bg-gradient-to-r from-amber-400 to-orange-400";
      case "Low":
        return "bg-gradient-to-r from-blue-400 to-indigo-400";
    }
  };

  useEffect(()=>{
    const storedImages = localStorage.getItem("images");
    if (storedImages) {
      setImages(JSON.parse(storedImages));
    }
  },[])

  const handleImageClick = async (image: ImageData | undefined) => {
    // Send the request to the backend with the image data and algorithm ID
    console.log(image);
    console.log("yes:" + ProcessStep?.id);
    try {
      console.log(ProcessStep);
      const response = await fetch(
        "http://localhost:5000/api/apply-processing",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            imageData: image?.data,
            processId: ProcessStep?.id,
          }),
        }
      );
      const data = await response.json();
      console.log("Response from backend:", data);

      // Save the data in localStorage using algoId as the key
      if (ProcessStep?.id) {
        // Save the data in localStorage using algoId as the key
        // const imageData = {
        //   processedImage: data.processed_image,  // The Base64 encoded image
        // };
        const formattedBase64 = convertToBase64Format(data.processed_image);
        // Saving the object in localStorage with a unique key (selectedAlgo.id)
        localStorage.setItem("process"+ProcessStep.id, formattedBase64)    
        console.log(`Data saved to localStorage with key: ${ProcessStep.id}`);
      } else {
        console.error("Algorithm ID (algoId) is missing in the response data.");
      }

      console.log("Data saved to localStorage");
    } catch (error) {
      console.error("Error sending image to backend:", error);
    }
  };

  const Router = useRouter();



  return (
    <div className="min-h-screen bg-gradient-to-br from-violet-50 via-fuchsia-50 to-rose-50 p-8">
      <div className="max-w-5xl mx-auto space-y-6">
        {steps.map((step) => (
          <Card 
            key={step.id}
            className="hover:shadow-2xl transition-all duration-500 border-0 backdrop-blur-md bg-white/80 overflow-hidden"
          >
            <CardContent className="p-0">
              <div className="grid grid-cols-2 gap-6">
                {/* Left Column */}
                <div className="p-6 space-y-4">
                  <div className="flex items-center gap-3">
                    <div>
                      <span className="text-sm font-medium text-gray-500">
                        {step.category}
                      </span>
                    </div>
                  </div>
                  
                  <h3 className="text-xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                    {step.name}
                  </h3>
                  
                  <p className="text-gray-600">
                    {step.description}
                  </p>
                  
                  <div className="flex flex-wrap gap-2">
                    {step.tags.map((feature, index) => (
                      <Badge 
                        key={index}
                        variant="secondary"
                        className="bg-purple-50 hover:bg-purple-100 text-purple-700 transition-colors duration-300"
                      >
                        {feature}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Right Column */}
                <div className="bg-gradient-to-br from-purple-50 to-pink-50 p-6 flex flex-col justify-between">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Processing Time:</span>
                      <span className="font-mono text-purple-600 font-medium">
                        {step.complexity}
                      </span>
                    </div>
                    
                  </div>

                  <Button
                    onClick={() => {
                      console.log("Algorithm clicked:", step); // Log the algorithm details here
                      handleViewDetails(step); // Call the function
                    }}
                    className="group flex items-center gap-2 bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white transition-all duration-300"
                  >
                    Apply this Algorithm
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </Button>
                  <Button
                    onClick={() => {
                      console.log("Algorithm clicked:", step); // Log the algorithm details here
                      Router.push(`/process?id=${step.id}`);

                    }}
                    className="group flex items-center gap-2 bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white transition-all duration-300"
                  >
                    See the Processed Image
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
        {/* Display Images if an algorithm is selected */}
        {/* {selectedAlgo && ( */}
        <div className="mt-8 space-y-4">
          <h2 className="text-2xl font-semibold text-gray-800">
            Images for Post Processing
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


  );
};

export default PostProcessingDisplay;
