import { useState, useEffect } from "react";

const DynamicHeadline = () => {
  const [displayText, setDisplayText] = useState("");
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const [isPaused, setIsPaused] = useState(false);

  const words = [
    "Discover New Perspectives",
    "Learn From Experts",
    "Find Your Next Favorite Show",
    "Expand Your Knowledge",
    "Get Daily Insights",
    "Stay Ahead With Podcasts"
  ];

  useEffect(() => {
    const currentWord = words[currentWordIndex];
    let timeout: NodeJS.Timeout;

    if (isPaused) {
      timeout = setTimeout(() => {
        setIsPaused(false);
        setIsDeleting(true);
      }, 12000);
    } else if (!isDeleting) {
      if (currentIndex < currentWord.length) {
        timeout = setTimeout(() => {
          setDisplayText(currentWord.substring(0, currentIndex + 1));
          setCurrentIndex(currentIndex + 1);
        }, 300);
      } else {
        setIsPaused(true);
      }
    } else {
      if (currentIndex > 0) {
        timeout = setTimeout(() => {
          setDisplayText(currentWord.substring(0, currentIndex - 1));
          setCurrentIndex(currentIndex - 1);
        }, 100);
      } else {
        setIsDeleting(false);
        setCurrentWordIndex((prevIndex) => (prevIndex + 1) % words.length);
        setCurrentIndex(0);
      }
    }

    return () => {
      if (timeout) clearTimeout(timeout);
    };
  }, [currentIndex, isDeleting, currentWordIndex, isPaused]);

  return (
    <h1 className="text-5xl font-bold serif-headline text-gray-900 mb-8 min-h-[120px]">
      {displayText}
      <span className="animate-pulse">|</span>
    </h1>
  );
};

export default DynamicHeadline; 