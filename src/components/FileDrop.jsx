import { useState } from "react";
import Swal from "sweetalert2";
import Files from "react-files";
import PropTypes from "prop-types";
import axios from "axios";

const FileDropzone = ({ onCsvData }) => {
  const [isUploading, setIsUploading] = useState(false);

  const handleUpload = (files) => {
    const file = files[0];
    const formData = new FormData();
    formData.append("file", file);

    // Set state to indicate that upload is in progress
    setIsUploading(true);

    axios
      .post("http://localhost:5000/analisis", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        // Handle the response from the server
        onCsvData(response.data);

        Swal.fire({
          icon: "success",
          title: "Upload Successful!",
          text: "File Anda telah berhasil diunggah.",
        });
      })
      .catch((error) => {
        // Handle errors
        Swal.fire({
          icon: "error",
          title: "Upload Error",
          text: error.response ? error.response.data.error : "Unknown error",
        });
      })
      .finally(() => {
        // Set state to indicate that upload is complete
        setIsUploading(false);
      });
  };

  const handleError = (error) => {
    // Set state to indicate that upload is complete
    setIsUploading(false);

    Swal.fire({
      icon: "error",
      title: "Upload Error",
      text: `Error code ${error.code}: ${error.message}`,
    });
  };

  return (
    <button
      className={`px-12 py-3 rounded-lg ${
        isUploading ? "bg-yellow-500" : "bg-[#680DD0]"
      } text-white font-bold`}
    >
      <Files
        className="files-dropzone"
        onChange={handleUpload}
        onError={handleError}
        accepts={[".csv"]}
        multiple
        maxFileSize={10000000}
        minFileSize={0}
        clickable
      >
        {isUploading ? <span>Uploading... </span> : <span>Upload File</span>}
      </Files>
    </button>
  );
};

FileDropzone.propTypes = {
  onCsvData: PropTypes.func.isRequired,
};

export default FileDropzone;
