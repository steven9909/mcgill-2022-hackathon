import { Routes, Route } from "react-router-dom";
import { APIProvider } from "./contexts/api-context";

import MainPage from "./pages/main";

const App = () => {
  return (
    <APIProvider>
      <Routes>
        <Route path="/" element={<MainPage />} />
      </Routes>
    </APIProvider>
  );
};

export default App;
