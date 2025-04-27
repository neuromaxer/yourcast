import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Circle } from "lucide-react";

interface HostChipProps {
  host: {
    id: string;
    name: string;
    image: string;
  };
  isSelected: boolean;
  onClick: () => void;
  isPlaceholder?: boolean;
}

const HostChip = ({ host, isSelected, onClick, isPlaceholder = false }: HostChipProps) => {
  return (
    <button
      onClick={onClick}
      disabled={isPlaceholder}
      className={`flex items-center gap-2 px-2 py-1 rounded-full border border-black transition-all duration-300
        ${isPlaceholder ? 'opacity-50 cursor-not-allowed' : ''}
        ${isSelected ? 'bg-card' : 'hover:bg-card'}`}
    >
      <Avatar className="w-8 h-8">
        <AvatarImage src={host.image} alt={host.name} />
        <AvatarFallback>
          <Circle className="h-4 w-4 text-gray-300" />
        </AvatarFallback>
      </Avatar>
      <span>
        {host.name}
      </span>
    </button>
  );
};

export default HostChip;
