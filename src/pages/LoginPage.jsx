import { useForm } from "react-hook-form";

export default function LoginPage() {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm();

  const onSubmit = (data) => console.log(data);
  console.log(watch("example"));

  return (
    <div className="bg-[#7879EF]">
      <div className="flex justify-center items-center h-screen">
        <div className="rounded-lg shadow p-12 bg-white">
          <h1 className="text-4xl text-center text-[#4B00A2] font-semibold mb-6">
            Login
          </h1>
          <form onSubmit={handleSubmit(onSubmit)}>
            <div className="gap-2">
              <div className="mb-4">
                <label className="block text-[#4B00A2] text-sm font-semibold mb-2">
                  Username
                </label>
                <input
                  className="gap-2.5 w-[340px] border p-2 rounded-lg border-solid border-[#D8D8D8]"
                  defaultValue=""
                  {...register("username", { required: true })}
                />
              </div>
              <div className="mb-4">
                <label className="block text-[#4B00A2] text-sm font-semibold mb-2">
                  Password
                </label>
                <input
                  type="password"
                  className="gap-2.5 w-[340px] border p-2 rounded-lg border-solid border-[#D8D8D8]"
                  defaultValue=""
                  {...register("password", { required: true })}
                />
                {errors.password && <span>Password is required</span>}
              </div>
            </div>
            <div className="justify-center items-center flex mt-10">
              <button
                type="submit"
                className="px-12 py-3 rounded-lg bg-[#680DD0] text-white font-bold"
              >
                Masuk
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
