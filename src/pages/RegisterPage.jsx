import axios from "axios";
import Swal from "sweetalert2";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

export default function RegisterPage() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const navigate = useNavigate();
  const onSubmit = async (data) => {
    try {
      await axios.post("http://localhost:5000/register", data);
      Swal.fire({
        icon: "success",
        title: "Registration Successful",
        text: "Anda telah berhasil terdaftar.",
      });
      navigate("/login");
    } catch (error) {
      console.error("Kesalahan saat registrasi:", error);
      Swal.fire({
        icon: "error",
        title: "Registration Error",
        text: "Terjadi kesalahan saat pendaftaran. Silakan coba lagi.",
      });
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="w-full max-w-sm p-8 bg-white rounded-md shadow-md">
        <h1 className="text-3xl font-bold mb-6 text-center text-[#4B00A2]">
          Register
        </h1>
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="flex flex-col my-4">
            <input
              type="text"
              className="w-full px-3 py-2 border border-gray-300 rounded"
              placeholder="Username"
              autoComplete="current-username"
              {...register("username", { required: true })}
            />
            {errors.username && (
              <span className="mt-2 text-xs text-red-500">
                Mohon isi di kolom berikut*
              </span>
            )}
          </div>
          <div className="flex flex-col my-4">
            <input
              type="email"
              className="w-full px-3 py-2 border border-gray-300 rounded"
              placeholder="Email"
              autoComplete="current-email"
              {...register("email", { required: true })}
            />
            {errors.email && (
              <span className="mt-2 text-xs text-red-500">
                Mohon isi di kolom berikut*
              </span>
            )}
          </div>
          <div className="flex flex-col my-4">
            <input
              type="password"
              className="w-full px-3 py-2 border border-gray-300 rounded"
              placeholder="Password"
              autoComplete="current-password"
              {...register("password", { required: true })}
            />
            {errors.password && (
              <span className="mt-2 text-xs text-red-500">
                Mohon isi di kolom berikut*
              </span>
            )}
          </div>
          <div className="flex items-center justify-center mt-10">
            <button
              type="submit"
              className="bg-[#680DD0] w-full font-bold  text-white p-3 rounded mb-4"
            >
              Daftar
            </button>
          </div>
        </form>
        <p className=" text-zinc-500">
          Sudah punya akun ?
          <a href="/login" className="ms-2 text-[#680DD0]">
            Masuk
          </a>
        </p>
      </div>
    </div>
  );
}
