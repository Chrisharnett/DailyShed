import "bootstrap/dist/css/bootstrap.min.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { PrivateRoute } from "./auth/privateRoute";
import Footer from "./components/Footer";
import NotFoundPage from "./pages/NotFoundPage";
import CreateAccountPage from "./pages/CreateAccountPage";
import LoginPage from "./pages/LoginPage";
import Navigation from "./components/NavBar";
import ExerciseTestPage from "./pages/ExerciseTestPage";
import { useState } from "react";

export function App() {
  const [user, setUser] = useState(null);

  return (
    <>
      <BrowserRouter>
        <Navigation />

        <Footer />
        <Routes>
          <Route path="/" element={<ExerciseTestPage />} />
          <Route path="*" element={<NotFoundPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/createAccount" element={<CreateAccountPage />} />
          <Route element={<PrivateRoute user={user} />}>
            <Route path="/exerciseTestPage" element={<ExerciseTestPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
