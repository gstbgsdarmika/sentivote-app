import { Link } from "react-router-dom";
import Navigation from "../components/Navigation";
import Img from "../assets/hero.jpg";
export default function AnalystInputTextPage() {
  return (
    <div className="">
      <Navigation />
      <div className="grid gap-20 grid-cols-2 w-11/12 md:container mx-auto mt-10 md:w-5/6 justify-center items-center">
        <div className="col-span-1">
          <div className="mx-auto py-10 md:py-20 my-0">
            <img src={Img} alt="Hero Image" className="w-full md:w-auto" />
          </div>
        </div>
        <div className="col-span-1">
          <h1 className="text-[#1E1E1E] text-4xl font-semibold mb-5">
            Tuliskan teks
          </h1>
          <textarea
            name="postContent"
            placeholder="Ketik teks yang ingin dianalisis...."
            className="p-3 w-full bg-white rounded-lg border border-zinc-300 text-neutral-400 text-sm"
            rows={8}
            cols={0}
          />
          <div className="gap-5 flex mt-5">
            <Link to="/hasil-analisis">
              <button
                type="button"
                className="px-12 py-3 rounded-lg bg-[#680DD0] text-white font-bold"
              >
                Analisis
              </button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
