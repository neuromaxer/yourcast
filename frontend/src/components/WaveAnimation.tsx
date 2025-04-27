import React, { useEffect, useRef } from 'react';
import './WaveAnimation.css';

interface WaveAnimationProps {
  isAnimating?: boolean;
  onWaveChange?: () => void;
  currentWaveIndex?: number;
  className?: string;
}

const waves = [
  { d: "M0,100 C300,200 900,0 1200,100 L1200,200 L0,200 Z", colors: ["#4facfe","#43e97b","#fa709a"] },
  { d: "M0,100 C400,50 800,150 1200,100 L1200,200 L0,200 Z", colors: ["#ff6a00","#ee0979","#ff6a00"] },
  { d: "M0,100 C200,0 1000,200 1200,100 L1200,200 L0,200 Z", colors: ["#19547b","#ffd89b","#19547b"] },
  { d: "M0,100 C350,180 850,20 1200,100 L1200,200 L0,200 Z", colors: ["#ff512f","#dd2476","#ff512f"] },
  { d: "M0,100 C250,150 950,50 1200,100 L1200,200 L0,200 Z", colors: ["#00c6ff","#0072ff","#00c6ff"] },
  { d: "M0,100 C150,120 1050,80 1200,100 L1200,200 L0,200 Z", colors: ["#8E2DE2","#4A00E0","#8E2DE2"] },
  { d: "M0,100 C500,200 700,0 1200,100 L1200,200 L0,200 Z", colors: ["#FF5F6D","#FFC371","#FF5F6D"] }
];

const WaveAnimation: React.FC<WaveAnimationProps> = ({
  isAnimating = false,
  onWaveChange,
  currentWaveIndex = 0,
  className
}) => {
  const waveRef = useRef<SVGPathElement>(null);
  const morphRef = useRef<SVGAnimateElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current) {
      if (isAnimating) {
        containerRef.current.classList.add('animate');
      } else {
        containerRef.current.classList.remove('animate');
      }
    }
  }, [isAnimating]);

  useEffect(() => {
    if (waveRef.current && morphRef.current && containerRef.current) {
      const currentD = waveRef.current.getAttribute('d');
      const choice = waves[currentWaveIndex % waves.length];

      // Update color variables
      containerRef.current.style.setProperty('--c1', choice.colors[0]);
      containerRef.current.style.setProperty('--c2', choice.colors[1]);
      containerRef.current.style.setProperty('--c3', choice.colors[2]);

      // Morph path
      morphRef.current.setAttribute('values', `${currentD}; ${choice.d}`);
      morphRef.current.beginElement();
    }
  }, [currentWaveIndex]);

  return (
    <div className={`wave-container ${className || ''}`} ref={containerRef}>
      <svg viewBox="0 0 1200 200" preserveAspectRatio="none">
        <defs>
          <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="var(--c1)" />
            <stop offset="50%" stopColor="var(--c2)" />
            <stop offset="100%" stopColor="var(--c3)" />
          </linearGradient>
        </defs>
        <path
          id="wave"
          ref={waveRef}
          fill="url(#grad)"
          d={waves[0].d}
        >
          <animate
            ref={morphRef}
            id="animMorph"
            attributeName="d"
            dur="2s"
            fill="freeze"
          />
        </path>
      </svg>
    </div>
  );
};

export default WaveAnimation;