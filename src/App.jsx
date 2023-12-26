import { Routes, Route } from "react-router-dom";
import "./styles/globals.css";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import HomePage from "./pages/HomePage";
import AnalystPage from "./pages/AnalystPage";
import AnalystInputTextPage from "./pages/AnalystInputTextPage";
import ResultsPage from "./pages/ResultsPage";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/" element={<HomePage />} />
        <Route path="/analisis" element={<AnalystPage />} />
        <Route path="/analisis/input-teks" element={<AnalystInputTextPage />} />
        <Route path="/hasil-analisis" element={<ResultsPage />} />
      </Routes>
    </div>
  );
}

export default App;
