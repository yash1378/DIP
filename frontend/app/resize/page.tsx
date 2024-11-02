"use client";
import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Image as ImageIcon } from "lucide-react";

const LocalStorageImageResizer = () => {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [selectedImageName, setSelectedImageName] = useState<string>("");
  const [displayDimensions, setDisplayDimensions] = useState({
    width: 800,
    height: 600,
  });
  const [originalDimensions, setOriginalDimensions] = useState<{
    width: 800;
    height: 600;
  } | null>(null);
  const [savedImages, setSavedImages] = useState<
    {
      name: string;
      data: string;
      dimensions?: { width: number; height: number };
    }[]
  >([]);

  useEffect(() => {
    const loadSavedImages = () => {
      const images = JSON.parse(localStorage.getItem("images") || "[]");
      setSavedImages(images);

      if (images.length > 0 && !selectedImage) {
        console.log(images);
        setSelectedImage(images[0].data);
        setSelectedImageName(images[0].name);
        if (images[0].dimensions) {
          setDisplayDimensions(images[0].dimensions);
          //   setOriginalDimensions(images[0].dimensions);
        }
      }
    };
    loadSavedImages();
  }, []);

  const resizeImage = (
    base64Image: string,
    newWidth: number,
    newHeight: number
  ): Promise<string> => {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.src = base64Image;

      img.onload = () => {
        const canvas = document.createElement("canvas");
        canvas.width = newWidth;
        canvas.height = newHeight;

        const ctx = canvas.getContext("2d");
        ctx?.drawImage(img, 0, 0, newWidth, newHeight);

        const resizedBase64Image = canvas.toDataURL("image/png");
        resolve(resizedBase64Image);
      };

      img.onerror = (error) => {
        reject(error);
      };
    });
  };

  const handleResizeAndSave = async () => {
    const newWidth = displayDimensions.width;
    const newHeight = displayDimensions.height;

    if (selectedImage) {
      const updatedImages = savedImages.map((img) => {
        if (img.data === selectedImage) {
          return {
            ...img,
            dimensions: { width: newWidth, height: newHeight },
          };
        }
        return img;
      });

      localStorage.setItem("images", JSON.stringify(updatedImages));
      setSavedImages(updatedImages);
    }
  };

  const handleImageSelect = (img: {
    name: string;
    data: string;
    dimensions?: { width: number; height: number };
  }) => {
    setSelectedImage(img.data);
    setSelectedImageName(img.name);

    console.log("clicked");
    if (img.dimensions) {
      setDisplayDimensions({
        width: img.dimensions.width,
        height: img.dimensions.height,
      });
    } else {
      const image = new Image();
      image.src = img.data;
      image.onload = () => {
        // setOriginalDimensions({ width: image.width, height: image.height });
      };
      image.onerror = () => {
        console.error("Failed to load image for dimensions retrieval.");
      };
    }
  };

  return (
    <div
      className="bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50"
      style={{ height: "85vh", width: "75vw", paddingTop: "5vh" }}
    >
      <div className="mx-auto" style={{ width: "70vw", height: "70vh" }}>
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Panel - Image Selection */}
          <Card className="backdrop-blur-sm bg-white/90 shadow-xl hover:shadow-2xl transition-all duration-300 border-0">
            <CardContent className="p-6">
              <div className="space-y-6">
                {/* Dimension Controls */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-700">
                      New Width
                    </label>
                    <Input
                      type="number"
                      className="border-2 focus:ring-2 focus:ring-blue-400"
                      value={displayDimensions.width}
                      onChange={(e) =>
                        setDisplayDimensions({
                          ...displayDimensions,
                          width: parseInt(e.target.value),
                        })
                      }
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-700">
                      New Height
                    </label>
                    <Input
                      type="number"
                      className="border-2 focus:ring-2 focus:ring-blue-400"
                      value={displayDimensions.height}
                      onChange={(e) =>
                        setDisplayDimensions({
                          ...displayDimensions,
                          height: parseInt(e.target.value),
                        })
                      }
                    />
                  </div>
                </div>

                {/* Update Button */}
                <Button
                  onClick={handleResizeAndSave}
                  className="w-full bg-blue-500 text-white hover:bg-blue-600"
                >
                  Update Image Size
                </Button>

                {/* Selected Image Display */}
                <div className="border-2 rounded-xl p-4 bg-gray-50">
                  {selectedImage ? (
                    <div className="space-y-3">
                      <img
                        src={selectedImage}
                        alt="Selected"
                        className="rounded-lg shadow-md"
                        style={{
                          width: `${originalDimensions?.width}px`,
                          height: `${originalDimensions?.height}px`,
                          objectFit: "contain",
                        }}
                      />
                      <p className="text-center text-4xl text-gray-600 font-medium">
                        {selectedImageName}
                      </p>
                    </div>
                  ) : (
                    <div className="text-center p-8 text-gray-500">
                      <ImageIcon className="w-12 h-12 mx-auto mb-3 text-gray-400" />
                      <p>Select an image from below</p>
                    </div>
                  )}
                </div>

                {/* Image Gallery */}
                <div className="space-y-3">
                  <h3 className="text-sm font-medium text-gray-700">
                    Saved Images
                  </h3>
                  <div className="h-48 overflow-y-auto border-2 border-gray-100 rounded-xl p-4 bg-white">
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                      {savedImages.map((img, index) => (
                        <div
                          key={index}
                          onClick={() => handleImageSelect(img)}
                          className={`
                        relative group cursor-pointer rounded-lg overflow-hidden
                        transition-all duration-300 transform hover:scale-105
                        ${
                          selectedImage === img.data
                            ? "ring-2 ring-blue-500"
                            : ""
                        }
                      `}
                        >
                          <img
                            src={img.data}
                            alt={img.name}
                            className="w-full h-24 object-cover rounded-lg"
                          />
                          <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-300 flex items-center justify-center">
                            <span className="text-black text-5xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 font-medium">
                              {img.name}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Right Panel - Preview */}
          <Card className="backdrop-blur-sm bg-white/90 shadow-xl hover:shadow-2xl transition-all duration-300 border-0">
            <CardContent className="p-6">
              <div className="h-full min-h-[500px] flex items-center justify-center border-2 border-gray-100 rounded-xl p-4 bg-gradient-to-br from-gray-50 to-white overflow-auto">
                {selectedImage ? (
                  <div
                    className="relative"
                    style={{
                      maxWidth: `${displayDimensions.width}px`, // Limit container to image dimensions
                      maxHeight: `${displayDimensions.height}px`, // Limit container to image dimensions
                      overflow: "auto", // Enable scrolling if image exceeds dimensions
                    }}
                  >
                    <img
                      src={selectedImage}
                      alt="Preview"
                      className="rounded-lg shadow-lg transition-all duration-300 hover:shadow-xl"
                      style={{
                        width: `${displayDimensions.width}px`, // Set fixed width for the image
                        height: `${displayDimensions.height}px`, // Set fixed height for the image
                        objectFit: "contain", // Maintain aspect ratio within the fixed dimensions
                      }}
                    />
                  </div>
                ) : (
                  <div className="text-center text-gray-500">
                    <ImageIcon className="w-12 h-12 mx-auto mb-3 text-gray-400" />
                    <p>No Image Selected</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default LocalStorageImageResizer;
