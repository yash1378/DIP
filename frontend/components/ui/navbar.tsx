"use client"
import React from 'react'
import { Upload, Image as ImageIcon, Camera, Settings2, Download, Home, ArrowRight } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
function Navbar() {
    const navButtons = [
        { id: "home", label: "Home", icon: <Home className="w-4 h-4" /> },
        { id: "resize", label: "Change Size", icon: <Settings2 className="w-4 h-4" /> },
        { id: "resolution", label: "Super Resolution", icon: <Camera className="w-4 h-4" /> },
        { id: "processing", label: "Processing", icon: <ArrowRight className="w-4 h-4" /> },
        { id: "download", label: "Download", icon: <Download className="w-4 h-4" /> },
      ];
      const [activeButton, setActiveButton] = React.useState<string>("home");
  return (
    <>
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
    </>
  )
}

export default Navbar
