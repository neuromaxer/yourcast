import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { User } from "lucide-react";

const Navbar = () => {
  return (
    <nav className="bg-background border-b border-black">
      <div className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <Link to="/" className="text-2xl font-bold serif-headline text-black">
            YourCast**
          </Link>

        </div>
      </div>
    </nav>
  );
};

export default Navbar;
