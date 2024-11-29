"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Download, Copy, AlertCircle } from "lucide-react";

export default function ImageViewer() {
  const router = useRouter();
  const [imageSrc, setImageSrc] = useState<string | null>(null);
  const [width, setWidth] = useState<number>(0);
  const [height, setHeight] = useState<number>(0);
  const [error, setError] = useState<string | null>(null);

  // Extracting `id` from query
  useEffect(() => {
    const { searchParams } = new URL(window.location.href);
    const id = searchParams.get("id"); // Assuming the query parameter is `id`

    if (id) {
      try {
        console.log(id);
        const storedImage = localStorage.getItem(id);

        if (storedImage) {
          // Parse the stored object if it contains Base64
          const parsedImage = JSON.parse(storedImage);

          // Check if the `processedImage` exists and is a valid Base64 string
          if (
            parsedImage?.processedImage &&
            parsedImage.processedImage.startsWith("data:image/")
          ) {
            setImageSrc(parsedImage.processedImage);
            setWidth(parsedImage.width);
            setHeight(parsedImage.height);
            setError(null);
          } else {
            setError("No valid image found in the stored data.");
          }
        } else {
          setError("No image found for this route.");
        }
      } catch (err) {
        setError("Error retrieving image from localStorage.");
      }
    } else {
      setError("No ID provided in the URL.");
    }
  }, []);

  const handleDownload = () => {
    if (imageSrc) {
      const link = document.createElement("a");
      link.href = imageSrc;
      link.download = `image.png`;
      link.click();
    }
  };

  const handleCopyLink = () => {
    if (imageSrc) {
      navigator.clipboard
        .writeText(imageSrc)
        .then(() => {
          alert("Image URL copied to clipboard");
        })
        .catch(() => {
          alert("Failed to copy image URL");
        });
    }
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center p-4">
      <Card className="w-full max-w-4xl bg-gray-900 border-gray-700 shadow-2xl">
        <CardContent className="p-8">
          {error ? (
            <div className="flex flex-col items-center justify-center text-white space-y-4">
              <AlertCircle className="w-16 h-16 text-red-500" />
              <h2 className="text-2xl font-bold text-gray-200">{error}</h2>
              <p className="text-gray-400 text-center">
                Ensure an image is stored in localStorage with the key matching
                this route.
              </p>
            </div>
          ) : (
            <div className="flex flex-col md:flex-row items-center space-y-6 md:space-y-0 md:space-x-8">
              {/* Image Container */}
              <div className="flex-shrink-0 w-full md:w-1/2 bg-gray-800 p-4 rounded-lg shadow-inner">
                <div className="overflow-auto rounded-md border-2 border-gray-700">
                  {imageSrc && (
                    <div
                      className="relative w-full h-full"
                      style={{
                        width: `${width}px`,
                        height: `${height}px`,
                      }}
                    >
                      <Image
                        src={imageSrc}
                        alt="Fetched Image"
                        layout="intrinsic"
                        width={width}
                        height={height}
                        className="object-contain grayscale hover:grayscale-0 transition-all duration-300"
                      />
                    </div>
                  )}
                </div>
              </div>

              {/* Image Details */}
              <div className="w-full md:w-1/2 text-white space-y-6">
                <div>
                  <h1 className="text-3xl font-bold text-gray-100 mb-2">
                    Image Details
                  </h1>
                </div>

                <div className="space-y-4">
                  <Button
                    onClick={handleDownload}
                    className="w-full bg-gray-800 hover:bg-gray-700 text-white"
                  >
                    <Download className="mr-2 h-4 w-4" /> Download Image
                  </Button>
                  <Button
                    onClick={handleCopyLink}
                    variant="outline"
                    className="w-full border-gray-700 text-white hover:bg-gray-800"
                  >
                    <Copy className="mr-2 h-4 w-4" /> Copy Image URL
                  </Button>
                </div>

                <div className="text-sm text-gray-500 italic">
                  Tip: Hover to reveal image color
                </div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
