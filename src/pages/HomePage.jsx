import Navigation from "../components/Navigation";
import Img from "../assets/hero.jpg";
import { Link } from "react-router-dom";
export default function HomePage() {
  return (
    <div className="">
      <Navigation />
      <div className="grid items-center justify-center w-11/12 grid-cols-2 gap-20 mx-auto mt-10 md:container md:w-5/6">
        <div className="col-span-1">
          <div className="py-10 mx-auto my-0 md:py-20">
            <img src={Img} alt="Hero Image" className="w-full md:w-auto" />
          </div>
        </div>
        <div className="col-span-1">
          <h1 className="text-[#1E1E1E] text-4xl font-semibold mb-2">
            Aplikasi SentiVote
          </h1>
          <p className=" text-[#615F5F] text-justify text-base mb-7">
            SentiVote adalah sebuah aplikasi analisis sentimen yang menggunakan
            pendekatan berbasis aspek untuk menganalisis data tekstual. Aplikasi
            ini dirancang untuk membantu pengguna dalam memahami dan
            menganalisis opini atau sentimen yang terkandung dalam teks.
          </p>
          <Link to="/analisis">
            <button
              type="submit"
              className="px-12 py-3 rounded-lg bg-[#680DD0] text-white font-bold"
            >
              Coba Sekarang
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}
