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
import Programs from "./pages/Programs";
import { useEffect } from "react";
import { Backgrounds } from "./util/Backgrounds.jsx";
import Spacer from "./util/Spacer.jsx";
import Callback from "./auth/Callback.jsx";
import { UserProvider } from "./auth/UserContext.jsx";

export function App() {
  useEffect(() => {
    const randomBackground =
      Backgrounds[Math.floor(Math.random() * Backgrounds.length)];
    document.body.style.backgroundImage = `url(${randomBackground})`;

    return () => {
      document.body.style.backgroundImage = null;
    };
  }, []);

  return (
    <UserProvider>
      <Spacer />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="*" element={<NotFoundPage />} />
          <Route path="/callback" element={<Callback />} />
          <Route element={<PrivateRoute />}>
            <Route path="/theShed" element={<TheShed />} />
            <Route path="/userProfile" element={<UserProfile />} />
            <Route path="/practiceJournal" element={<PracticeJournal />} />
            <Route path="/programs" element={<Programs />} />
          </Route>
        </Routes>
        <Navigation />

        <Footer />
      </BrowserRouter>
      <Spacer />
    </UserProvider>
  );
}

export default App;
