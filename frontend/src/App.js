import "bootstrap/dist/css/bootstrap.min.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { PrivateRoute } from "./auth/privateRoute";
import Footer from "./components/Footer";
import NotFoundPage from "./pages/NotFoundPage";
import Navigation from "./components/NavBar";
import ExerciseTestPage from "./pages/ExerciseTestPage";
import TheShed from "./pages/TheShed";
import UserProfile from "./pages/UserProfile";
import PracticeJournal from "./pages/PracticeJournal";
import HomePage from "./pages/HomePage";
import { useState } from "react";

export function App() {
  const [user, setUser] = useState(null);
  const [loggedIn, setLoggedIn] = useState(false);

  return (
    <>
      <BrowserRouter>
        <Navigation user={user} loggedIn={loggedIn} setLoggedIn={setLoggedIn} />

        <Footer />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="*" element={<NotFoundPage />} />
          <Route element={<PrivateRoute user={user} />}>
            <Route path="/exerciseTestPage" element={<ExerciseTestPage />} />
            <Route path="/theShed" element={<TheShed user={user} />} />
            <Route path="/userProfile" element={<UserProfile user={user} />} />
            <Route
              path="/practiceJournal"
              element={<PracticeJournal user={user} />}
            />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
