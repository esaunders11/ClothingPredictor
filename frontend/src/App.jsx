import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Trends from "./pages/Trends";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/trends" element={<Trends />} />
      </Routes>
    </Router>
  );
}

export default App;
