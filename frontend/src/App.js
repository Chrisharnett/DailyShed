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
import { useEffect, useState } from "react";
import { useToken } from "./auth/useToken";
import { Backgrounds } from "./util/Backgrounds";

export function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [, setToken] = useToken();

  const urlParams = new URLSearchParams(window.location.search);
  const token = urlParams.get("token");

  useEffect(() => {
    const t = localStorage.getItem("token");
    if (t) {
      setLoggedIn(true);
    }
  }, []);

  useEffect(() => {
    if (token) {
      setToken(token);
      setLoggedIn(true);
    }
  }, [token, setToken]);

  useEffect(() => {
    const randomBackground =
      Backgrounds[Math.floor(Math.random() * Backgrounds.length)];
    document.body.style.backgroundImage = `url(${randomBackground})`;
    return () => {
      document.body.style.backgroundImage = null;
    };
  }, []);

  return (
    <>
      <BrowserRouter>
        <Navigation loggedIn={loggedIn} setLoggedIn={setLoggedIn} />

        <Footer />
        <Routes>
          <Route path="/" element={<HomePage loggedIn={loggedIn} />} />
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
