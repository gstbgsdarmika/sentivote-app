import Navigation from "../components/Navigation";
import { Link } from "react-router-dom";

export default function ResultsPage() {
  return (
    <div className="mt-12">
      <Navigation />
      <div className="flex flex-col justify-center items-center h-screen text-center">
        <h1 className="text-stone-900 text-4xl font-semibold">
          Hasil Analisis Sentimen
        </h1>
        <div className="w-[524.82px] mt-5">
          <p className="text-stone-900 text-base font-medium">
            Ulasan:
            <span className="text-zinc-600 text-base font-normal">
              Ahok-Djarot kalah dalam pilkada, tapi menang dalam menjaga
              integritas berdemokrasi Pancasila. Bangga!
            </span>
          </p>
          <h1 className="mt-10 md:p-2.5 p-1.5 bg-violet-700 rounded-lg  text-white md:text-4xl text-2xl font-extrabold inline-block">
            Sentimen : Positif
          </h1>
        </div>
        <div className="mt-12">
          <Link to="/analisis">
            <button
              type="button"
              className="px-8 py-3 rounded-lg border border-violet-700 font-bold text-violet-700 hover:bg-violet-700 hover:text-white"
            >
              Coba Lagi
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}
