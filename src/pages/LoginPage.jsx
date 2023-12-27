import axios from "axios";
import Swal from "sweetalert2";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const navigate = useNavigate();
  const onSubmit = async (data) => {
    try {
      const response = await axios.post("http://localhost:5000/login", data);

      if (response.data.success) {
        const accessToken = response.data.access_token;
        localStorage.setItem("token", accessToken);

        navigate("/");
        Swal.fire({
          icon: "success",
          title: "Login Successful!",
          text: "Anda berhasil login.",
        });
      } else {
        console.error("Login gagal:", response.data.message);
        Swal.fire({
          icon: "error",
          title: "Login Failed",
          text: response.data.message || "Terjadi kesalahan saat login.",
        });
      }
    } catch (error) {
      console.error("Error during login:", error);
      Swal.fire({
        icon: "error",
        title: "Login Failed",
        text: "Terjadi kesalahan saat login. Silakan coba lagi.",
      });
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="w-full max-w-sm p-8 bg-white rounded-md shadow-md">
        <h1 className="text-3xl font-bold mb-6 text-center text-[#4B00A2]">
          Login
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
              Masuk
            </button>
          </div>
        </form>
        <p className=" text-zinc-500">
          Belum punya akun ?
          <a href="/register" className="ms-2 text-[#680DD0]">
            Daftar
          </a>
        </p>
      </div>
    </div>
  );
}
