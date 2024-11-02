"use client";
import React from "react";
import { Upload, Image as ImageIcon, Camera, Settings2, Download, Home, ArrowRight } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

const ImageUploadPage: React.FC = () => {
  const [selectedImage, setSelectedImage] = React.useState<string | ArrayBuffer | null>(null);
  const [imageName, setImageName] = React.useState<string>("");
  const [activeButton, setActiveButton] = React.useState<string>("home");
  const fileInputRef = React.useRef<HTMLInputElement | null>(null);

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setSelectedImage(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const navButtons = [
    { id: "home", label: "Home", icon: <Home className="w-4 h-4" /> },
    { id: "resize", label: "Change Size", icon: <Settings2 className="w-4 h-4" /> },
    { id: "resolution", label: "Super Resolution", icon: <Camera className="w-4 h-4" /> },
    { id: "processing", label: "Processing", icon: <ArrowRight className="w-4 h-4" /> },
    { id: "download", label: "Download", icon: <Download className="w-4 h-4" /> },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-900 dark:to-gray-800">
      {/* Navigation Bar */}
      <nav className="sticky top-0 z-50 backdrop-blur-lg bg-white/70 dark:bg-gray-900/70 border-b border-gray-200 dark:border-gray-700">
        <div className="container mx-auto py-4">
          <div className="flex items-center justify-center gap-2 overflow-x-auto">
            {navButtons.map((button) => (
              <Button
                key={button.id}
                variant={activeButton === button.id ? "default" : "ghost"}
                className={cn(
                  "relative group px-6 py-2 transition-all duration-300",
                  activeButton === button.id && "bg-primary text-primary-foreground"
                )}
                onClick={() => setActiveButton(button.id)}
              >
                <div className="flex items-center gap-2">
                  {button.icon}
                  <span>{button.label}</span>
                </div>
                {activeButton === button.id && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary"
                  />
                )}
              </Button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="container mx-auto p-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="grid grid-cols-1 md:grid-cols-2 gap-8 h-[700px]"
        >
          {/* Left Panel - Upload Controls */}
          <Card className="backdrop-blur-xl bg-white/50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-700 shadow-xl">
            <CardContent className="p-8 h-full flex flex-col justify-center gap-8">
              <input
                type="file"
                ref={fileInputRef}
                className="hidden"
                onChange={handleImageUpload}
                accept="image/*"
              />

              <motion.div
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <Button
                  variant="outline"
                  className="w-full h-32 text-lg relative overflow-hidden group border-2 border-dashed"
                  onClick={() => fileInputRef.current?.click()}
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-100 to-purple-100 dark:from-blue-900/20 dark:to-purple-900/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                  <div className="relative flex flex-col items-center gap-2">
                    <Upload className="h-8 w-8 group-hover:scale-110 transition-transform duration-300" />
                    <span className="font-semibold">Upload Image</span>
                    <span className="text-sm text-muted-foreground">Click to browse files</span>
                  </div>
                </Button>
              </motion.div>

              <motion.div
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <div className="relative">
                  <Input
                    placeholder="Name your masterpiece..."
                    value={imageName}
                    onChange={(e) => setImageName(e.target.value)}
                    className="w-full h-32 text-lg text-center bg-white/50 dark:bg-gray-900/50 border-2 placeholder:text-gray-400"
                  />
                </div>
              </motion.div>
            </CardContent>
          </Card>

          {/* Right Panel - Image Preview */}
          <Card className="backdrop-blur-xl bg-white/50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-700 shadow-xl overflow-hidden">
            <CardContent className="p-8 h-full flex items-center justify-center relative">
              {selectedImage ? (
                <motion.img
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  src={selectedImage as string}
                  alt="Preview"
                  className="max-w-full max-h-full object-contain rounded-lg shadow-lg"
                />
              ) : (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex flex-col items-center justify-center text-muted-foreground"
                >
                  <div className="relative">
                    <div className="absolute inset-0 bg-gradient-to-r from-blue-200 to-purple-200 dark:from-blue-700 dark:to-purple-700 blur-2xl opacity-20 animate-pulse" />
                    <ImageIcon className="h-24 w-24 mb-4 relative" />
                  </div>
                  <p className="text-lg font-medium mt-4">Image preview after uploading</p>
                  <p className="text-sm text-muted-foreground mt-2">Supported formats: PNG, JPG, WEBP</p>
                </motion.div>
              )}
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  );
};

export default ImageUploadPage;