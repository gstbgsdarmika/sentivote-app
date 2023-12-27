import { Popover, Transition } from "@headlessui/react";
import { FaRegUserCircle, FaSignOutAlt } from "react-icons/fa";
import { Fragment } from "react";

const solutions = [
  {
    name: "Keluar",
    href: "/login",
    icon: IconOne,
  },
];

export default function Profile() {
  const handleLogout = () => {
    // Hapus token dari local storage
    localStorage.removeItem("token");

    // Arahkan pengguna kembali ke halaman login
    window.location.href = "/login";
  };
  return (
    <div className="">
      <Popover className="relative">
        {({ open }) => (
          <>
            <Popover.Button
              className={`
                ${open ? "text-white" : "text-white/90"}
                `}
            >
              <span>
                <FaRegUserCircle className="w-6 h-6" />
              </span>
            </Popover.Button>
            <Transition
              as={Fragment}
              enter="transition ease-out duration-200"
              enterFrom="opacity-0 translate-y-1"
              enterTo="opacity-100 translate-y-0"
              leave="transition ease-in duration-150"
              leaveFrom="opacity-100 translate-y-0"
              leaveTo="opacity-0 translate-y-1"
            >
              <Popover.Panel className="absolute z-10 min-w-full mt-1 transform -translate-x-1/2 left-1/2 lg:max-w-3xl">
                <div className="overflow-hidden rounded-lg shadow-lg ring-1 ring-black/5">
                  <div className="relative grid gap-8 p-3 bg-white">
                    {solutions.map((item) => (
                      <a
                        key={item.name}
                        href={item.href}
                        className="flex items-center p-2 -m-3 transition duration-150 ease-in-out rounded-lg hover:bg-gray-50 focus:outline-none focus-visible:ring focus-visible:ring-orange-500/50"
                        onClick={handleLogout}
                      >
                        <div className="flex items-center justify-center text-white shrink-0 sm:h-12 sm:w-12">
                          <item.icon aria-hidden="true" />
                        </div>
                        <div className="ml-2">
                          <p className="text-sm font-medium text-gray-900">
                            {item.name}
                          </p>
                          <p className="text-sm text-gray-500">
                            {item.description}
                          </p>
                        </div>
                      </a>
                    ))}
                  </div>
                </div>
              </Popover.Panel>
            </Transition>
          </>
        )}
      </Popover>
    </div>
  );
}

function IconOne() {
  return <FaSignOutAlt className="w-6 h-6 text-black" />;
}
