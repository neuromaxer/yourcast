import { useParams, useLocation, Navigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { BookmarkPlus } from "lucide-react";
import { Link } from "react-router-dom";
import { SpotifyIcon, ApplePodcastsIcon, GooglePodcastsIcon, YouTubeIcon } from "@/components/PlatformIcons";
import type { Episode } from "@/components/EpisodeCard";

const Episode = () => {
  const { id } = useParams();
  const location = useLocation();
  const episode = location.state?.episode as Episode | undefined;

  // If no episode data is available, redirect back to home
  if (!episode) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        {/* Banner Image */}
        <div className="relative w-full h-[400px]">
          <img
            src={episode.image}
            alt={episode.title}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
          <div className="absolute bottom-0 left-0 right-0 p-6 text-white">
            <h1 className="text-4xl font-bold mb-2 serif-headline">{episode.title}</h1>
            <p className="text-blue-200 hover:text-blue-100">
              <Link to={`/host/${episode.hostId}`} className="hover:underline">
                {episode.host}
              </Link>
            </p>
            <p className="text-gray-200 text-sm">{new Date(episode.date).toLocaleDateString()}</p>
          </div>
        </div>

        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Left Column */}
            <div className="md:col-span-2">
              <div className="mb-8">
                <h2 className="text-xl font-semibold mb-3 serif-headline">Episode Summary</h2>
                <p className="text-gray-700 leading-relaxed">{episode.summary}</p>
              </div>

              {episode.keyTakeaways && episode.keyTakeaways.length > 0 && (
                <div>
                  <h2 className="text-xl font-semibold mb-3 serif-headline">Key Takeaways</h2>
                  <ul className="list-disc pl-5 space-y-2">
                    {episode.keyTakeaways.map((point, index) => (
                      <li key={index} className="text-gray-700">{point.text}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Right Column */}
            <div className="space-y-8">
              <div>
                <h2 className="text-xl font-semibold mb-3 serif-headline">Listen On</h2>
                <div className="flex gap-4">
                  <a href={episode.platformLinks?.spotify} target="_blank" rel="noopener noreferrer" className="hover:text-green-500">
                    <SpotifyIcon />
                  </a>
                  <a href={episode.platformLinks?.youtube} target="_blank" rel="noopener noreferrer" className="hover:text-red-500">
                    <YouTubeIcon />
                  </a>
                </div>
              </div>

              {episode.category && (
                <div>
                  <h2 className="text-xl font-semibold mb-3 serif-headline">Category</h2>
                  <span className="inline-block border-2 border-black px-4 py-2 rounded-full text-sm font-medium">
                    {episode.category}
                  </span>
                </div>
              )}
            </div>
          </div>

          {/* Similar Episodes Section */}
          {episode.similarEpisodes && episode.similarEpisodes.length > 0 && (
            <div className="mt-12">
              <h2 className="text-2xl font-semibold mb-6 serif-headline">Similar Episodes</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {episode.similarEpisodes.map((similar) => (
                  <Link
                    to={`/episode/${similar.id}`}
                    key={similar.id}
                    className="group"
                  >
                    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                      <img
                        src={similar.thumbnail}
                        alt={similar.title}
                        className="w-full h-32 object-cover"
                      />
                      <div className="p-4">
                        <h3 className="font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                          {similar.title}
                        </h3>
                        <p className="text-sm text-gray-600 mt-2">
                          {similar.teaser}
                        </p>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Episode;
