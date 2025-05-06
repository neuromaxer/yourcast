import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Check, X, Download } from "lucide-react";
import { useState, useEffect } from "react";
import { Label } from "@/components/ui/label";
import WaveAnimation from "./WaveAnimation";

interface KeyTakeaway {
  text: string;
}

interface Episode {
  id?: number;
  title?: string;
  description?: string;
  keyTakeaways?: KeyTakeaway[];
  [key: string]: any; // For any other properties that might exist
}

interface EpisodeSelectionDialogProps {
  isOpen: boolean;
  onClose: () => void;
  selectedCount: number;
  data_sample: Episode[];
}

const EpisodeSelectionDialog = ({
  isOpen,
  onClose,
  selectedCount,
  data_sample,
}: EpisodeSelectionDialogProps) => {
  const [length, setLength] = useState<string>("precise");
  const [tone, setTone] = useState<string>("neutral");
  const [style, setStyle] = useState<string>("single");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [isAnimating, setIsAnimating] = useState(false);
  const [waveIndex, setWaveIndex] = useState(0);

  const handleWaveChange = () => {
    setWaveIndex((prev) => (prev + 1) % 7);
  };

  const handleSelectionChange = (
    setter: (value: string) => void,
    value: string
  ) => {
    setter(value);
    handleWaveChange();
  };

  const generateAudio = async () => {
    try {
      const response = await fetch("http://0.0.0.0:8000/summary_audio", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          length,
          tone,
          style,
          data_sample: data_sample.map((episode) => ({
            ...episode,
            id: 9,
            keyTakeaways:
              episode.keyTakeaways?.map((point) => point.text) || [],
          })),
        }),
      });

      if (!response.ok) {
        throw new Error(`Failed to generate podcast: ${response.status}`);
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setAudioUrl(url);
      return url;
    } catch (err) {
      throw new Error(
        err instanceof Error ? err.message : "Failed to generate audio"
      );
    }
  };

  const handleGenerateAudio = async () => {
    setIsLoading(true);
    setIsAnimating(true);
    setError(null);

    try {
      await generateAudio();
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
      console.error("Error generating podcast:", err);
    } finally {
      setIsLoading(false);
      setIsAnimating(false);
    }
  };

  // Cleanup function to revoke object URLs
  useEffect(() => {
    return () => {
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
  }, [audioUrl]);

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader className="relative min-h-[200px]">
          <div className="absolute inset-0 overflow-hidden -mx-6 -mt-6">
            <WaveAnimation
              isAnimating={isAnimating}
              currentWaveIndex={waveIndex}
              onWaveChange={handleWaveChange}
              className="w-full h-full !w-full !max-w-none"
            />
          </div>
          <div className="relative z-10 px-6 pt-6 pb-4 text-center">
            <DialogTitle className="text-2xl font-bold mb-3 text-white">
              Generate your personalized episode
            </DialogTitle>
            <DialogDescription className="text-md opacity-90 text-white">
              You have selected {selectedCount} episode
              {selectedCount !== 1 ? "s" : ""}. Please select your preferences
              below.
            </DialogDescription>
          </div>
        </DialogHeader>
        <div className="space-y-6 py-4">
          <div className="space-y-2">
            <Label>Length</Label>
            <div className="flex flex-wrap gap-2">
              <Button
                variant={length === "precise" ? "default" : "outline"}
                size="sm"
                onClick={() => handleSelectionChange(setLength, "precise")}
                className="rounded-full"
                disabled={isLoading}
              >
                Precise
              </Button>
              <Button
                variant={length === "elaborate" ? "default" : "outline"}
                size="sm"
                onClick={() => handleSelectionChange(setLength, "elaborate")}
                className="rounded-full"
                disabled={isLoading}
              >
                Elaborate
              </Button>
            </div>
          </div>

          <div className="space-y-2">
            <Label>Tone</Label>
            <div className="flex flex-wrap gap-2">
              <Button
                variant={tone === "neutral" ? "default" : "outline"}
                size="sm"
                onClick={() => handleSelectionChange(setTone, "neutral")}
                className="rounded-full"
                disabled={isLoading}
              >
                Neutral
              </Button>
              <Button
                variant={tone === "funny" ? "default" : "outline"}
                size="sm"
                onClick={() => handleSelectionChange(setTone, "funny")}
                className="rounded-full"
                disabled={isLoading}
              >
                Funny
              </Button>
              <Button
                variant={tone === "professional" ? "default" : "outline"}
                size="sm"
                onClick={() => handleSelectionChange(setTone, "professional")}
                className="rounded-full"
                disabled={isLoading}
              >
                Professional
              </Button>
              <Button
                variant={tone === "easy" ? "default" : "outline"}
                size="sm"
                onClick={() => handleSelectionChange(setTone, "easy")}
                className="rounded-full"
                disabled={isLoading}
              >
                Easy Language
              </Button>
            </div>
          </div>

          <div className="space-y-2">
            <Label>Style</Label>
            <div className="flex flex-wrap gap-2">
              <Button
                variant={style === "single" ? "default" : "outline"}
                size="sm"
                onClick={() => handleSelectionChange(setStyle, "single")}
                className="rounded-full"
                disabled={isLoading}
              >
                Single Reader
              </Button>
              <Button
                variant={style === "conversation" ? "default" : "outline"}
                size="sm"
                onClick={() => handleSelectionChange(setStyle, "conversation")}
                className="rounded-full"
                disabled={isLoading}
              >
                Conversation
              </Button>
            </div>
          </div>

          {error && <div className="text-red-500 text-sm mt-2">{error}</div>}
        </div>

        <DialogFooter className="flex gap-2">
          <Button variant="outline" onClick={onClose} disabled={isLoading}>
            <X className="mr-2 h-4 w-4" />
            Cancel
          </Button>
          {audioUrl ? (
            <a
              href={audioUrl}
              download="custom-episode.mp3"
              className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
            >
              <Download className="mr-2 h-4 w-4" />
              Download Audio
            </a>
          ) : (
            <Button onClick={handleGenerateAudio} disabled={isLoading}>
              <Check className="mr-2 h-4 w-4" />
              {isLoading ? "Generating..." : "Generate Audio"}
            </Button>
          )}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default EpisodeSelectionDialog;
