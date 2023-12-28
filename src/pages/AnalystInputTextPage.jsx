import axios from "axios";
import Navigation from "../components/Navigation";
import Img from "../assets/hero.jpg";
import { useState } from "react";

export default function AnalystInputTextPage() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [prediction, setPrediction] = useState(null); // Tambah state untuk menyimpan prediksi

  const onSubmit = async () => {
    try {
      const response = await axios.post(
        "http://localhost:5000/analisis/input-teks",
        { text }
      );
      if (response && response.data && response.data.result) {
        setResult(response.data.result);
        // Perbarui state prediction
        setPrediction(response.data.prediction);
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
            {result !== null ? (
              <div>
                <p>Hasil: {result}</p>
                {/* Tampilkan prediksi */}
                {prediction !== null && <p>Prediksi: {prediction}</p>}
              </div>
            ) : null}
          </div>
        </div>
      </div>
    </div>
  );
}
