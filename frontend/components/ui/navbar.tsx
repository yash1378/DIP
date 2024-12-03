"use client";
import React from 'react';
import { Upload, Image as ImageIcon, Camera, VideoIcon,Settings2, Download, Home, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { useRouter, usePathname } from 'next/navigation'; // Import usePathname

function Navbar() {
    const router = useRouter(); // Initialize the router
    const pathname = usePathname(); // Get the current pathname
    const navButtons = [
        { id: "home", label: "Home", icon: <Home className="w-4 h-4" />, route: "/" },
        { id: "resize", label: "Change Size", icon: <Settings2 className="w-4 h-4" />, route: "/resize" },
        { id: "resolution", label: "Super Resolution", icon: <Camera className="w-4 h-4" />, route: "/super_resolute" },
        { id: "processing", label: "Processing", icon: <ArrowRight className="w-4 h-4" />, route: "/processing" },
        { id: "download", label: "Compare", icon: <Download className="w-4 h-4" />, route: "/download" },
        { id: "video", label: "Video", icon: <VideoIcon className="w-4 h-4" />, route: "/video" },
        { id: "DL", label: "DL based Processing", icon: <ArrowRight className="w-4 h-4" />, route: "/dlbased" },
    ];
    
    // Determine the active button based on the current pathname
    const activeButton = navButtons.find(button => button.route === pathname)?.id || "home";

    const handleButtonClick = (buttonId: string, route: string) => {
        router.push(route); // Navigate to the specified route
    };

    return (
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
                            onClick={() => handleButtonClick(button.id, button.route)} // Updated click handler
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
    );
}

export default Navbar;
