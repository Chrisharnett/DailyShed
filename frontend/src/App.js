import "bootstrap/dist/css/bootstrap.min.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { PrivateRoute } from "./auth/privateRoute";
import Footer from "./components/Footer";
import NotFoundPage from "./pages/NotFoundPage";
import Navigation from "./components/NavBar";
import TheShed from "./pages/TheShed";
import UserProfile from "./pages/UserProfile";
import PracticeJournal from "./pages/PracticeJournal";
import HomePage from "./pages/HomePage";

export function App() {
  return (
    <>
      <BrowserRouter>
        <Navigation />

        <Footer />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="*" element={<NotFoundPage />} />
          <Route element={<PrivateRoute />}>
            <Route path="/theShed" element={<TheShed />} />
            <Route path="/userProfile" element={<UserProfile />} />
            <Route path="/practiceJournal" element={<PracticeJournal />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
