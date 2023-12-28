import { useState } from "react";
import { Link } from "react-router-dom";
import Navigation from "../components/Navigation";
import FileDropzone from "../components/FileDrop";
import Img from "../assets/hero.jpg";
import ReactPaginate from "react-paginate";
import PropTypes from "prop-types";
import { FaChevronLeft, FaChevronRight } from "react-icons/fa";

const DataDisplay = ({ csvData }) => {
  const itemsPerPage = 10;
  const [currentPage, setCurrentPage] = useState(0);

  const offset = currentPage * itemsPerPage;
  const currentData = csvData.slice(offset, offset + itemsPerPage) || [];

  const pageCount = Math.ceil(csvData.length / itemsPerPage);

  const handlePageClick = ({ selected }) => {
    setCurrentPage(selected);
  };

  return (
    <div className="items-center justify-center w-11/12 mx-auto mt-32 mb-10 md:container md:w-5/6">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-[#1E1E1E] text-4xl font-semibold">
          Hasil Analisis Sentimen
        </h1>
      </div>
      <div className="overflow-auto">
        {csvData.length > 0 && (
          <table className="w-full p-6 text-left ">
            <thead className="text-white bg-[#680DD0]">
              <tr className="p-1 text-sm">
                {Object.keys(csvData[0]).map((header) => (
                  <th key={header} className="p-3 border-r border-gray-300">
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {currentData.map((row, index) => (
                <tr
                  key={index}
                  className="p-3 text-left border border-b border-gray-700 border-opacity-20"
                >
                  {Object.values(row).map((value, i) => (
                    <td
                      key={i}
                      className="p-4 text-sm border-r border-gray-300"
                    >
                      {value}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
      <ReactPaginate
        className="flex items-center justify-end gap-5 mt-10"
        previousLabel={
          <div className="p-3 text-base border rounded-full">
            <FaChevronLeft />
          </div>
        }
        nextLabel={
          <div className="p-3 text-base border rounded-full">
            <FaChevronRight />
          </div>
        }
        breakLabel={"..."}
        pageCount={pageCount}
        marginPagesDisplayed={1}
        pageRangeDisplayed={1}
        onPageChange={handlePageClick}
        containerClassName={"pagination"}
        activeClassName={"bg-[#680DD0] text-white"}
        pageClassName={
          "text-base border p-5 cursor-pointer w-5 h-5 flex items-center justify-center rounded-full cursor-pointer"
        }
      />
    </div>
  );
};

DataDisplay.propTypes = {
  csvData: PropTypes.array.isRequired,
};

const AnalystPage = () => {
  const [csvData, setCsvData] = useState([]);
  const [fileUploaded, setFileUploaded] = useState(false);

  const handleCsvData = (data) => {
    setCsvData(data);
    setFileUploaded(true);
  };

  return (
    <div>
      <Navigation />
      {!fileUploaded && (
        <div className="grid items-center justify-center w-11/12 grid-cols-2 gap-20 mx-auto mt-10 md:container md:w-5/6">
          <div className="col-span-1">
            <div className="py-10 mx-auto my-0 md:py-20">
              <img src={Img} alt="Hero Image" className="w-full md:w-auto" />
            </div>
          </div>
          <div className="col-span-1">
            <h1 className="text-[#1E1E1E] text-4xl font-semibold mb-2">
              Pilih Masukan Data
            </h1>
            <p className="text-[#615F5F] text-justify text-base mb-7">
              SentiVote memungkinkan untuk memasukkan teks langsung atau
              mengunggah data dalam format CSV.
            </p>
            <div className="flex gap-5 mt-20">
              <Link to="/analisis/input-teks">
                <button
                  type="button"
                  className="px-12 py-3 rounded-lg bg-[#680DD0] text-white font-bold"
                >
                  Input teks
                </button>
              </Link>
              <FileDropzone onCsvData={handleCsvData} />
            </div>
          </div>
        </div>
      )}
      {fileUploaded && <DataDisplay csvData={csvData} />}
    </div>
  );
};

export default AnalystPage;
