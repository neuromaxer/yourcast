import { useParams } from "react-router-dom";
import EpisodeCard from "@/components/EpisodeCard";

const Host = () => {
  const { id } = useParams();

  // Placeholder data - would come from your API
  const host = {
    id: "sarah123",
    name: "Tech Talks with Sarah",
    profileImage: "https://images.unsplash.com/photo-1494790108377-be9c29b29330",
    description: "Join Sarah as she explores the fascinating world of technology, interviewing industry experts and discussing the latest trends in AI, machine learning, and software development. With over 5 years of experience in the tech industry, Sarah brings a unique perspective to complex technical topics.",
    followers: 12500,
    episodes: [
      {
        id: 1,
        title: "The Future of AI",
        host: "Tech Talks with Sarah",
        hostId: "sarah123",
        image: "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b",
        summary: "A fascinating discussion about artificial intelligence and its impact on society.",
        date: "2025-04-20",
        duration: "45:30",
        views: 2500,
      },
      {
        id: 3,
        title: "Machine Learning Basics",
        host: "Tech Talks with Sarah",
        hostId: "sarah123",
        image: "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b",
        summary: "An introduction to machine learning concepts and applications.",
        date: "2025-04-18",
        duration: "38:15",
        views: 1800,
      },
      {
        id: 2,
        title: "Web Development Trends 2025",
        host: "Tech Talks with Sarah",
        hostId: "sarah123",
        image: "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b",
        summary: "Exploring the latest trends and technologies in web development.",
        date: "2025-04-15",
        duration: "52:10",
        views: 3200,
      },
    ],
    recommendedEpisodes: [
      {
        id: 4,
        title: "The Rise of Quantum Computing",
        host: "Tech Talks with Sarah",
        hostId: "sarah123",
        image: "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b",
        summary: "A deep dive into quantum computing and its potential applications.",
        date: "2025-04-10",
        duration: "41:25",
        views: 4200,
      },
      {
        id: 5,
        title: "Cybersecurity Best Practices",
        host: "Tech Talks with Sarah",
        hostId: "sarah123",
        image: "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b",
        summary: "Essential cybersecurity practices for developers and businesses.",
        date: "2025-04-05",
        duration: "48:40",
        views: 3800,
      },
    ],
  };

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Profile Section */}
      <div className="flex flex-col md:flex-row gap-8 mb-12">
        <div className="w-full md:w-1/3">
          <img
            src={host.profileImage}
            alt={host.name}
            className="w-full h-64 md:h-80 object-cover rounded-lg shadow-lg"
          />
        </div>
        <div className="w-full md:w-2/3">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">{host.name}</h1>
          <p className="text-gray-600 mb-4">{host.description}</p>

        </div>
      </div>

      {/* Recommended Episodes Section */}
      <section>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Recommended Episodes</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {host.recommendedEpisodes.map((episode) => (
          <EpisodeCard key={episode.id} episode={episode} />
        ))}
      </div>
      </section>

      {/* Recent Episodes Section */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Recent Episodes</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {host.episodes.map((episode) => (
            <EpisodeCard key={episode.id} episode={episode} />
          ))}
        </div>
      </section>


    </div>
  );
};

export default Host;
