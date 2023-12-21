import Profile from "./Profile";
import { Link, useLocation } from "react-router-dom";

export default function Navigation() {
  const location = useLocation();
  const isActive = (path) => location.pathname === path;
  return (
    <nav className="bg-[#4B00A2] py-5 fixed w-full top-0">
      <div className="w-11/12 md:container mx-auto md:w-5/6 flex justify-between items-center">
        <div>
          <h1 className="text-white text-2xl font-semibold">
            Aplikasi SentiVote
          </h1>
        </div>
        <div className="flex items-center">
          <ul className="flex gap-x-10">
            <li
              className={`text-white text-base ${
                isActive("/") && "font-bold transition-all duration-300"
              }`}
            >
              <Link to="/">Beranda</Link>
            </li>
            <li
              className={`text-white text-base ${
                isActive("/analisis") && "font-bold transition-all duration-300"
              }`}
            >
              <Link to="/analisis">Analisis</Link>
            </li>
            <li
              className={`text-white text-base ${
                isActive("/hasil-analisis") &&
                "font-bold transition-all duration-300"
              }`}
            >
              <Link to="/hasil-analisis">Arsip</Link>
            </li>
            <li className="text-white">
              <Profile />
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}
