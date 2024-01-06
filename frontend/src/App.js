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
import StudentExercisePage from "./pages/StudentExercisePage";
import HomePage from "./pages/HomePage";
import { useState } from "react";

export function App() {
  const [user] = useState(null);

  return (
    <>
      <BrowserRouter>
        <Navigation />

        <Footer />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="*" element={<NotFoundPage />} />
          <Route element={<PrivateRoute />}>
            <Route
              path="studentExercisePage"
              element={<StudentExercisePage />}
            />
            <Route path="/exerciseTestPage" element={<ExerciseTestPage />} />
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
