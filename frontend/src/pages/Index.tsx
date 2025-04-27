import { Search, Check, X } from "lucide-react";
import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import EpisodeCard from "@/components/EpisodeCard";
import HostChipsContainer from "@/components/HostChipsContainer";
import EpisodeSelectionDialog from "@/components/EpisodeSelectionDialog";
import DynamicHeadline from "@/components/DynamicHeadline";
import { Episode } from "@/components/EpisodeCard";
import axios from "axios";
import podcastImages from "@/../public/podcast_images.json";

const Index = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedHosts, setSelectedHosts] = useState<string[]>([]);
  const [isSelectionMode, setIsSelectionMode] = useState(false);
  const [selectedEpisodes, setSelectedEpisodes] = useState<string[]>([]);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [episodes, setEpisodes] = useState<Episode[]>([]);

  // Convert podcast images JSON to the required format
  const allHosts = Object.entries(podcastImages).map(([name, image]) => ({
    id: name.toLowerCase().replace(/\s+/g, '-'),
    name,
    image,
  }));

  // Filter hosts to only include those with episodes, or use all hosts if episodes is empty
  const availableHosts = episodes.length > 0
    ? allHosts.filter(host =>
        episodes.some(episode =>
          episode.host.toLowerCase().replace(/\s+/g, '-') === host.id
        )
      )
    : allHosts;

  const toggleHost = (hostId: string) => {
    setSelectedHosts((prev) =>
      prev.includes(hostId)
        ? prev.filter((id) => id !== hostId)
        : [...prev, hostId]
    );
  };

  const toggleEpisodeSelection = (episodeId: string) => {
    setSelectedEpisodes((prev) =>
      prev.includes(episodeId)
        ? prev.filter((id) => id !== episodeId)
        : [...prev, episodeId]
    );
    console.log(selectedEpisodes);
  };

  const resetSelectionState = () => {
    setIsSelectionMode(false);
    setSelectedEpisodes([]);
  };

  const handleExitSelection = () => {
    resetSelectionState();
  };

  async function searchBulletpoints(query, limit = 10) {
    try {
      const response = await axios.get("http://localhost:8000/search", {
        params: {
          query: query,
          limit: limit,
        },
      });
      console.log(response.data.results);
      setEpisodes(response.data.results);
    } catch (error) {
      console.error("Error fetching search results:", error);
      throw error;
    }
  }

  // Filter episodes based on selected hosts
  const filteredEpisodes = episodes.filter(episode => {
    if (selectedHosts.length === 0) return true;
    // Convert episode host name to the same ID format as the hosts
    const episodeHostId = episode.host.toLowerCase().replace(/\s+/g, '-');
    return selectedHosts.includes(episodeHostId);
  });

  return (
    <div className="container mx-auto px-4 py-8 bg-background">
      <div className="flex flex-col items-center mb-12">
        <DynamicHeadline />
        <div className="w-full max-w-xl space-y-4">
          <div className="flex items-center gap-4">
            <div className="relative flex-1">
              <Input
                type="text"
                placeholder="What are you interested in?"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    searchBulletpoints(searchQuery);
                  }
                }}
                className="w-full pl-10 pr-4 py-2 text-gray-900 rounded-lg border-2 border-black-400 transition-all duration-300 ease-in-out focus:ring-2 focus:ring-primary focus:ring-opacity-50 focus:border-transparent"
              />
            </div>
            <div className="flex gap-2 transition-all duration-300">
              {!isSelectionMode ? (
                <Button
                  variant="outline"
                  onClick={() => setIsSelectionMode(true)}
                  className="flex items-center gap-2 whitespace-nowrap border-2"
                >
                  <Check className="h-4 w-4" />
                  Select
                </Button>
              ) : (
                <>
                  <Button
                    variant="outline"
                    onClick={handleExitSelection}
                    className="flex items-center gap-2 whitespace-nowrap border-2"
                  >
                    <X className="h-4 w-4" />
                    Exit Selection
                  </Button>
                  {selectedEpisodes.length > 0 && (
                    <Button
                      onClick={() => setIsDialogOpen(true)}
                      className="flex items-center gap-2 whitespace-nowrap border-2"
                    >
                      <Check className="h-4 w-4" />
                      Confirm ({selectedEpisodes.length})
                    </Button>
                  )}
                </>
              )}
            </div>
          </div>
          <HostChipsContainer
            hosts={availableHosts}
            selectedHosts={selectedHosts}
            onHostToggle={toggleHost}
            isPlaceholder={episodes.length === 0}
          />
        </div>
      </div>

      <div className="columns-1 md:columns-2 lg:columns-3 gap-6 space-y-6">
        {filteredEpisodes.map((episode) => (
          <div key={episode.id} className="mb-6 break-inside-avoid">
            <EpisodeCard
              episode={episode}
              isSelectable={isSelectionMode}
              isSelected={selectedEpisodes.includes(episode.id)}
              onSelect={() => toggleEpisodeSelection(episode.id)}
            />
          </div>
        ))}
      </div>

      <EpisodeSelectionDialog
        isOpen={isDialogOpen}
        onClose={() => setIsDialogOpen(false)}
        selectedCount={selectedEpisodes.length}
        data_sample={selectedEpisodes.map((id) => episodes.find((episode) => episode.id === id))}
      />
    </div>
  );
};

export default Index;
