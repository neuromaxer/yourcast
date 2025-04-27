import { useRef, useState } from "react";

interface AudioPlayerProps {
  audioUrl?: string;
}

const AudioPlayer = ({ audioUrl }: AudioPlayerProps) => {
  const audioRef = useRef<HTMLAudioElement>(null);

  return (
    <div className="mb-8 bg-gray-50 rounded-lg p-6">
      <div className="flex flex-col gap-4">
        <audio
          ref={audioRef}
          src={audioUrl}
          controls
          className="w-full"
        />
      </div>
    </div>
  );
};

export default AudioPlayer;