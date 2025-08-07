import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import Navbar from "./components/Navbar";
import MatchingsPage from "./components/matchings/MatchingsPage";
import Search from "./components/search/Search";
import Queue from "./components/queue/Queue";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Applied from "./components/applied/Applied";
function App() {
  const [count, setCount] = useState(0);

  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<MatchingsPage />}></Route>
        <Route path="/search" element={<Search />}></Route>
        <Route path="/queue" element={<Queue />}></Route>
        <Route path="/applied" element={<Applied />}></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
