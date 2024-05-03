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
import useUser from "./auth/useUser";
import axios from "axios";

export function App() {
  const [, setToken] = useToken();
  const [cognitoURL, setCognitoURL] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);
  // const [playerDetails, setPlayerDetails] = useState(null);

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
        const response = await axios.get("/api/auth/cognito/url");
        const { url } = response.data;
        setCognitoURL(url);
      } catch (e) {
        console.log(e);
      }
    };
    loadCognitoURL();
  }, []);

  // useEffect(() => {
  //   const fetchPlayerDetails = async () => {
  //     const response = await axios.get(`/api/getUserData/${user.sub}`);
  //     setPlayerDetails(response.data.userData);
  //   };
  //   if (user) {
  //     fetchPlayerDetails();
  //   }
  // }, [user]);

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
            <Route
              path="/theShed"
              element={
                <TheShed
                  user={user}
                  // playerDetails={playerDetails}
                  // updatePlayerDetails={setPlayerDetails}
                />
              }
            />
            <Route
              path="/userProfile"
              element={
                <UserProfile
                  user={user}
                  // playerDetails={playerDetails}
                  // updatePlayerDetails={setPlayerDetails}
                />
              }
            />
            <Route
              path="/practiceJournal"
              element={
                <PracticeJournal
                  user={user}
                  // playerDetails={playerDetails}
                />
              }
            />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
