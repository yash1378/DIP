"use client"
import React from 'react';
import { 
  ChevronRight, 
  Sparkles, 
  Code2, 
  Cpu, 
  BarChart2,
  ArrowRight
} from 'lucide-react';
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useRouter } from 'next/navigation';
import { useEffect,useState } from 'react';
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

const AlgorithmsDisplay = () => {
  // Mock data - replace with API call
  const [algorithms,setAlgorithms] = useState<Algorithm[]>([]);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:5000/api/list_super_resolution_methods");
        const data = await response.json();
        console.log(data);
        setAlgorithms(data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
  
    fetchData();
  }, []);

  // const algorithms: Algorithm[] = [
  //   {
  //     id: "1",
  //     name: "Enhanced Bicubic Interpolation",
  //     description: "Advanced image scaling using cubic splines with edge preservation",
  //     complexity: "O(n²)",
  //     category: "Image Processing",
  //     performance: 92,
  //     tags: ["Scaling", "High Quality", "Interpolation"]
  //   },
  //   {
  //     id: "2",
  //     name: "Neural Super Resolution",
  //     description: "Deep learning-based upscaling with detail enhancement",
  //     complexity: "O(n³)",
  //     category: "Machine Learning",
  //     performance: 98,
  //     tags: ["AI", "Deep Learning", "GPU Accelerated"]
  //   },
  //   {
  //     id: "3",
  //     name: "Adaptive Lanczos Algorithm",
  //     description: "Context-aware image resizing with artifact reduction",
  //     complexity: "O(n log n)",
  //     category: "Image Processing",
  //     performance: 85,
  //     tags: ["Fast", "Quality", "Adaptive"]
  //   },
  //   {
  //     id: "4",
  //     name: "Quantum Image Magnification",
  //     description: "Next-gen image processing using quantum computing principles",
  //     complexity: "O(log n)",
  //     category: "Quantum Computing",
  //     performance: 95,
  //     tags: ["Experimental", "Quantum", "High Speed"]
  //   },
  //   {
  //     id: "5",
  //     name: "Multi-Frame Synthesis",
  //     description: "Combines multiple frames for enhanced resolution output",
  //     complexity: "O(n²)",
  //     category: "Video Processing",
  //     performance: 88,
  //     tags: ["Video", "Real-time", "Multi-frame"]
  //   }
  // ];

  const Router = useRouter();

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
                  <p className="text-gray-600">
                    {algo.description}
                  </p>
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
                      <span className={`text-lg font-bold ${getPerformanceColor(algo.performance)}`}>
                        {algo.performance}%
                      </span>
                    </div>
                  </div>

                  <Button
                    onClick={() => Router.push(`/algorithm/${algo.id}`)}
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
      </div>
    </div>
  );
};

export default AlgorithmsDisplay;