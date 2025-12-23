import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import SoccerPage from "./pages/SoccerPage";
import NbaPage from "./pages/NbaPage";
import "./App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/soccer" element={<SoccerPage />} />
        <Route path="/nba" element={<NbaPage />} />
      </Routes>
    </Router>
  );
}

export default App;
