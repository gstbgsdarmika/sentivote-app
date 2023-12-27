import { Routes, Route } from "react-router-dom";
import "./styles/globals.css";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import HomePage from "./pages/HomePage";
import AnalystPage from "./pages/AnalystPage";
import AnalystInputTextPage from "./pages/AnalystInputTextPage";
import ResultsPage from "./pages/ResultsPage";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/" element={<ProtectedRoute element={<HomePage />} />} />
        <Route
          path="/analisis"
          element={<ProtectedRoute element={<AnalystPage />} />}
        />
        <Route
          path="/analisis/input-teks"
          element={<ProtectedRoute element={<AnalystInputTextPage />} />}
        />
        <Route
          path="/hasil-analisis"
          element={<ProtectedRoute element={<ResultsPage />} />}
        />
      </Routes>
    </div>
  );
}

export default App;
