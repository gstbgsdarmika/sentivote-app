import axios from "axios";
import Navigation from "../components/Navigation";
import Img from "../assets/hero.jpg";
import { useState } from "react";
import { Link } from "react-router-dom";

export default function AnalystInputTextPage() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [predictionAspect, setPredictionAspect] = useState(null);

  const onSubmit = async () => {
    try {
      const response = await axios.post(
        "http://localhost:5000/analisis/input-teks",
        { text }
      );
      if (response && response.data && response.data.result) {
        setResult(response.data.result);
        setPrediction(response.data.prediction_sentiment);
        setPredictionAspect(response.data.prediction_aspect);
      } else {
        console.error(
          "Respon dari server tidak sesuai format yang diharapkan",
          response
        );
      }
    } catch (error) {
      console.error("Kesalahan saat analisis teks input:", error);
    }
  };

  return (
    <div className="">
      <Navigation />
      {result !== null ? (
        <div className="flex flex-col items-center justify-center h-screen mt-10 text-center">
          <h1 className="text-4xl font-semibold text-stone-900">
            Hasil Analisis Sentimen
          </h1>
          <div className="w-[524.82px] mt-5">
            <p className="text-base font-semibold text-stone-900">
              Teks:
              <span className="text-base font-normal text-zinc-600">
                {"  " + result}
              </span>
            </p>
            <p className="text-base font-semibold text-stone-900">
              Aspek:
              <span className="text-base font-normal whitespace-pre-wrap text-zinc-600">
                {"  " + predictionAspect}
              </span>
            </p>
            {prediction !== null && (
              <h1 className="capitalize mt-10 md:p-2.5 p-1.5 bg-violet-700 rounded-lg  text-white md:text-4xl text-2xl font-extrabold inline-block">
                Sentimen : {prediction}
              </h1>
            )}
          </div>
          <div className="mt-12">
            <Link to="/analisis">
              <button
                type="button"
                className="px-8 py-3 font-bold border rounded-lg border-violet-700 text-violet-700 hover:bg-violet-700 hover:text-white"
              >
                Coba Lagi
              </button>
            </Link>
          </div>
        </div>
      ) : (
        <div className="grid items-center justify-center w-11/12 grid-cols-2 gap-20 mx-auto mt-10 md:container md:w-5/6">
          <div className="col-span-1">
            <div className="py-10 mx-auto my-0 md:py-20">
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
              className="w-full p-3 text-sm bg-white border rounded-lg border-zinc-300 text-neutral-400"
              rows={8}
              cols={0}
              value={text}
              onChange={(e) => setText(e.target.value)}
            />
            <div className="flex gap-5 mt-5">
              <button
                onClick={onSubmit}
                type="button"
                className="px-12 py-3 rounded-lg bg-[#680DD0] text-white font-bold"
              >
                Analisis
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
