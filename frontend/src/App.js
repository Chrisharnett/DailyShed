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
import { Backgrounds } from "./util/Backgrounds.js";
import { useToken } from "./auth/useToken";
import axios from "axios";

export function App() {
  const [, setToken] = useToken();
  const [cognitoURL, setCognitoURL] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);

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
    const loadCognitoURL = async () => {
      try {
        const response = await axios.get("/api/auth/cognito/url");
        const { url } = response.data;
        setCognitoURL(url);
      } catch (e) {
        console.log(e);
      }
    };
    loadCognitoURL();
  }, []);

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
        <Navigation
          loggedIn={loggedIn}
          setLoggedIn={setLoggedIn}
          cognitoURL={cognitoURL}
        />

        <Footer />
        <Routes>
          <Route
            path="/"
            element={<HomePage loggedIn={loggedIn} cognitoURL={cognitoURL} />}
          />
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
