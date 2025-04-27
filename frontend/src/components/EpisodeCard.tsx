import { Link } from "react-router-dom";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
} from "@/components/ui/card";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Circle, Check } from "lucide-react";
import { cn } from "@/lib/utils";

export interface BulletPoint {
  text: string;
  timestamp: number;
}

export interface Episode {
  id: string;
  title: string;
  host: string;
  hostId: string;
  image: string;
  summary: string;
  date: string;
  keyTakeaways?: BulletPoint[];
  category?: string;
  platformLinks?: {
    spotify?: string;
    youtube?: string;
    apple?: string;
    google?: string;
  };
  similarEpisodes?: Array<{
    id: string;
    title: string;
    thumbnail: string;
    teaser: string;
  }>;
}

interface EpisodeCardProps {
  episode: Episode;
  isSelected?: boolean;
  onSelect?: () => void;
  isSelectable?: boolean;
}

const EpisodeCard = ({
  episode,
  isSelected,
  onSelect,
  isSelectable,
}: EpisodeCardProps) => {
  const cardContent = (
    <Card
      className={cn(
        "relative overflow-hidden transition-all duration-300 shadow-lg hover:shadow-xl",
        isSelectable && "cursor-pointer hover:scale-[1.02]",
        isSelected && "ring-2 ring-primary ring-offset-2"
      )}
      onClick={isSelectable ? onSelect : undefined}
    >
      {isSelected && (
        <div className="absolute inset-0 bg-gradient-to-r from-primary/20 via-primary/10 to-primary/20 animate-shimmer" />
      )}
      <CardHeader className="p-0">
        <div className="relative aspect-[16/10]">
          <img
            src={episode.image}
            alt={episode.title}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent" />
          <div className="absolute bottom-0 left-0 right-0 p-4">
            <h3 className="font-semibold text-lg text-white mb-1 serif-headline">
              {episode.title}
            </h3>
            <p className="text-sm text-gray-300 mb-1">{episode.host}</p>
            <p className="text-xs text-gray-300">{episode.date}</p>
          </div>
          {isSelected && (
            <div className="absolute top-2 right-2 bg-primary/90 text-white p-1 rounded-full">
              <Check className="h-4 w-4" />
            </div>
          )}
        </div>
      </CardHeader>
      <CardContent className="p-4">
        <p className="text-sm text-gray-600 mb-3">{episode.summary}</p>
        {episode.keyTakeaways && episode.keyTakeaways.length > 0 && (
          <div className="space-y-2">
            <h4 className="text-sm font-medium text-gray-700">
              Key Takeaways:
            </h4>
            <ul className="space-y-1">
              {episode.keyTakeaways.map((takeaway, index) => (
                <li
                  key={index}
                  className="text-sm text-gray-600 flex items-start gap-2"
                >
                  <Circle className="h-2 w-2 mt-2 text-primary" />
                  <span>{takeaway.text}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );

  // Only wrap in Link when not in selection mode
  if (isSelectable) {
    return cardContent;
  }

  return <Link to={`/episode/${episode.id}`} state={{ episode }}>{cardContent}</Link>;
};

export default EpisodeCard;
