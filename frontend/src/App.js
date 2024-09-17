import "bootstrap/dist/css/bootstrap.min.css";
// import "dotenv/config";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { PrivateRoute } from "./auth/privateRoute";
import Footer from "./components/Footer";
import NotFoundPage from "./pages/NotFoundPage";
import Navigation from "./components/NavBar";
import TheShed from "./pages/TheShed";
import UserProfile from "./pages/UserProfile";
import PracticeJournal from "./pages/PracticeJournal";
import HomePage from "./pages/HomePage";
import Programs from "./pages/Programs";
import { useEffect, useState } from "react";
import { Backgrounds } from "./util/Backgrounds.js";
import { useToken } from "./auth/useToken";
import useUser from "./auth/useUser";
import axios from "axios";
import Spacer from "./util/Spacer.js";

export function App() {
  const [, setToken] = useToken();
  const [cognitoURL, setCognitoURL] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);

  const urlParams = new URLSearchParams(window.location.search);
  const token = urlParams.get("token");

  const { user } = useUser();

  useEffect(() => {
    const t = localStorage.getItem("token");
    if (t) {
      setLoggedIn(true);
    }
  }, []);

  useEffect(() => {
    if (token && !loggedIn) {
      setToken(token);
      setLoggedIn(true);
    }
  }, [token, setToken, loggedIn]);

  useEffect(() => {
    const loadCognitoURL = async () => {
      try {
        const response = await axios.get(
          // `${process.env.REACT_APP_API_GATEWAY_PROD}/api/auth/cognito/url`
          `${process.env.REACT_APP_COGNITO_URL}`
        );
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
        <Spacer />
        <Footer />

        <Routes>
          <Route
            path="/"
            element={
              <HomePage
                loggedIn={loggedIn}
                cognitoURL={cognitoURL}
                user={user}
              />
            }
          />
          <Route path="*" element={<NotFoundPage />} />
          <Route element={<PrivateRoute />}>
            <Route path="/theShed" element={<TheShed user={user} />} />
            <Route path="/userProfile" element={<UserProfile user={user} />} />
            <Route
              path="/practiceJournal"
              element={<PracticeJournal user={user} />}
            />
            <Route path="/programs" element={<Programs user={user} />} />
          </Route>
        </Routes>
      </BrowserRouter>
      <Spacer />
    </>
  );
}

export default App;
