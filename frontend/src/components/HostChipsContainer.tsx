import { useState, useMemo } from "react";
import { Search, ChevronDown, ChevronUp } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import HostChip from "@/components/HostChip";

interface Host {
  id: string;
  name: string;
  image: string;
}

interface HostChipsContainerProps {
  hosts: Host[];
  selectedHosts: string[];
  onHostToggle: (hostId: string) => void;
  isPlaceholder?: boolean;
}

const HostChipsContainer = ({ hosts, selectedHosts, onHostToggle, isPlaceholder = false }: HostChipsContainerProps) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  const filteredHosts = useMemo(() => {
    return hosts.filter(host =>
      host.name.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [hosts, searchQuery]);

  const visibleHosts = isExpanded ? filteredHosts : filteredHosts.slice(0, 2);

  return (
    <div className="w-full space-y-4">
      {isExpanded && (
        <div className="flex items-center gap-2">
          <div className="relative flex-1 transition-all duration-300 ease-in-out">
            <Input
              type="text"
              placeholder="Search hosts..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 focus-visible:ring-0 focus-visible:ring-offset-0"
              disabled={isPlaceholder}
            />
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
          </div>
          <Button
            variant="outline"
            size="icon"
            onClick={() => setIsExpanded(!isExpanded)}
            className="shrink-0"
            disabled={isPlaceholder}
          >
            <ChevronUp className="h-4 w-4" />
          </Button>
        </div>
      )}

      <div className="flex items-center gap-2">
        <div className="flex flex-wrap gap-2 flex-1 transition-all duration-300 ease-in-out">
          {visibleHosts.map((host) => (
            <HostChip
              key={host.id}
              host={host}
              isSelected={selectedHosts.includes(host.id)}
              onClick={() => onHostToggle(host.id)}
              isPlaceholder={isPlaceholder}
            />
          ))}
        </div>
        {!isExpanded && (
          <Button
            variant="outline"
            size="icon"
            onClick={() => setIsExpanded(!isExpanded)}
            className="shrink-0"
            disabled={isPlaceholder}
          >
            <ChevronDown className="h-4 w-4" />
          </Button>
        )}
      </div>
    </div>
  );
};

export default HostChipsContainer;