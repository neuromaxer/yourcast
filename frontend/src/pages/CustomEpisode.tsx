import { useParams, useLocation, Navigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { BookmarkPlus } from "lucide-react";
import { Link } from "react-router-dom";
import AudioPlayer from "@/components/AudioPlayer";

const CustomEpisode = () => {
  const { id } = useParams();
  const location = useLocation();

  console.log('location', location.state);
  // If no audioUrl is available, redirect back to home
  if (!location.state?.audioUrl) {
    return <Navigate to="/" replace />;
  }

  const { audioUrl, audioFilename } = location.state;
  


  // const length = location.state?.length;
  // const tone = location.state?.tone;
  // const style = location.state?.style;
  // const data_sample = location.state?.data_sample;



  // const fetchEpisode = async () => {
  //   const response = await fetch('http://0.0.0.0:8081/generate-podcast-metadata', {
  //     method: 'POST',
  //     body: JSON.stringify({
  //         length,
  //         tone,
  //         style,
  //         data_sample: data_sample.map(episode => ({
  //         ...episode,
  //         id: 9,
  //         keyTakeaways: episode.keyTakeaways?.map(point => point.text) || []
  //       }))
  //     }),
  //   });

  //   if (!response.ok) {
  //     throw new Error('Failed to generate podcast');
  //   }

  //   const data = await response.json();
  //   console.log(data);
  //   return data;

  // }


  // fetchEpisode();

  // Placeholder data - would come from your API


  const episode = {
    id: 1,
    title: "Your Personalized Episode",
    host: "YourCast",
    hostId: "yourcast",
    image: "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b",
    summary: "A personalized episode generated just for you.",
    date: new Date().toISOString().split('T')[0],
    aiSummary: "This episode has been generated based on your selected preferences and episodes.",
    bulletPoints: [
      "Customized content based on your selections",
      "Personalized audio experience",
      "Unique episode tailored to your interests"
    ],
    category: "Custom",
    duration: "45:30",
    similarEpisodes: []
  };

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
          {/* Audio Player Section */}
          <AudioPlayer 
            audioUrl={audioUrl}
          />

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Left Column */}
            <div className="md:col-span-2">
              <div className="mb-8">
                <h2 className="text-xl font-semibold mb-3 serif-headline">Episode Summary</h2>
                <p className="text-gray-700 leading-relaxed">{episode.aiSummary}</p>
              </div>

              <div>
                <h2 className="text-xl font-semibold mb-3 serif-headline">Key Takeaways</h2>
                <ul className="list-disc pl-5 space-y-2">
                  {episode.bulletPoints.map((point, index) => (
                    <li key={index} className="text-gray-700">{point}</li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Right Column */}
            <div className="space-y-8">
              <div>
                <h2 className="text-xl font-semibold mb-3 serif-headline">Category</h2>
                <span className="inline-block border-2 border-black px-4 py-2 rounded-full text-sm font-medium">
                  {episode.category}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CustomEpisode; 