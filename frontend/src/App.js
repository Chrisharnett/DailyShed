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
import Spacer from "./util/Spacer.js";
import Callback from "./auth/Callback";

export function App() {
  const [, setToken] = useToken();
  const [loggedIn, setLoggedIn] = useState(false);

  const { user } = useUser();

  useEffect(() => {
    const storedToken = sessionStorage.getItem("id_token");
    if (storedToken) {
      setLoggedIn(true);
    } else {
      setLoggedIn(false);
    }
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
        <Navigation loggedIn={loggedIn} setLoggedIn={setLoggedIn} />
        <Spacer />
        <Footer />

        <Routes>
          <Route
            path="/"
            element={<HomePage loggedIn={loggedIn} user={user} />}
          />
          <Route path="*" element={<NotFoundPage />} />
          <Route path="/callback" element={<Callback />} />
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
