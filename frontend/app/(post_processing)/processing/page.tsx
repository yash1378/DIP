"use client"
import React from 'react';
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
  impact: 'High' | 'Medium' | 'Low';
  category: string;
  timeRequired: string;
  features: string[];
  qualityScore: number;
}

const PostProcessingDisplay = () => {
  const steps: ProcessingStep[] = [
    {
      id: "1",
      name: "Color Enhancement & Balancing",
      description: "Advanced color correction with AI-powered tone mapping",
      impact: "High",
      category: "Color Correction",
      timeRequired: "2-3 seconds",
      features: ["Auto Balance", "HDR", "Vibrance"],
      qualityScore: 96
    },
    {
      id: "2",
      name: "Noise Reduction & Sharpening",
      description: "Intelligent noise reduction while preserving edge details",
      impact: "Medium",
      category: "Detail Enhancement",
      timeRequired: "4-5 seconds",
      features: ["Smart Sharpen", "Denoise", "Detail Preserve"],
      qualityScore: 92
    },
    {
      id: "3",
      name: "Contrast & Brightness Optimization",
      description: "Dynamic range adjustment with local contrast enhancement",
      impact: "High",
      category: "Tone Adjustment",
      timeRequired: "1-2 seconds",
      features: ["Auto Contrast", "Shadow Lift", "Highlight Recovery"],
      qualityScore: 94
    },
    {
      id: "4",
      name: "Artifact Removal & Cleanup",
      description: "Advanced algorithms to remove compression artifacts",
      impact: "Medium",
      category: "Image Cleanup",
      timeRequired: "3-4 seconds",
      features: ["JPEG Fix", "Smooth Edges", "Pattern Remove"],
      qualityScore: 88
    },
    {
      id: "5",
      name: "Final Image Optimization",
      description: "Smart compression and format optimization",
      impact: "High",
      category: "Optimization",
      timeRequired: "2-3 seconds",
      features: ["Smart Compress", "Format Select", "Metadata Clean"],
      qualityScore: 95
    }
  ];

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
                    <div className={`p-2 rounded-lg ${getImpactColor(step.impact)} text-white`}>
                      {getCategoryIcon(step.category)}
                    </div>
                    <div>
                      <span className="text-sm font-medium text-gray-500">
                        {step.category}
                      </span>
                      <Badge 
                        variant="secondary"
                        className={`ml-3 ${
                          step.impact === 'High' 
                            ? 'bg-emerald-100 text-emerald-700' 
                            : step.impact === 'Medium'
                            ? 'bg-amber-100 text-amber-700'
                            : 'bg-blue-100 text-blue-700'
                        }`}
                      >
                        {step.impact} Impact
                      </Badge>
                    </div>
                  </div>
                  
                  <h3 className="text-xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                    {step.name}
                  </h3>
                  
                  <p className="text-gray-600">
                    {step.description}
                  </p>
                  
                  <div className="flex flex-wrap gap-2">
                    {step.features.map((feature, index) => (
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
                        {step.timeRequired}
                      </span>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Quality Score:</span>
                      <div className="flex items-center gap-2">
                        <Contrast className="w-4 h-4 text-purple-500" />
                        <span className="text-lg font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                          {step.qualityScore}%
                        </span>
                      </div>
                    </div>
                  </div>

                  <Button
                    onClick={() => navigate.push(`/process/${step.id}`)}
                    className="group w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white transition-all duration-300 shadow-lg hover:shadow-xl"
                  >
                    Configure Step
                    <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
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

export default PostProcessingDisplay;