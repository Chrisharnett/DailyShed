import "bootstrap/dist/css/bootstrap.css";
import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { App, StudentSignIn, Exercises, Teacher } from "./App";
import reportWebVitals from "./reportWebVitals";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import StudentExercisePage from "./pages/StudentExercisePage";
import StudentPracticePage from "./pages/StudentPracticePage";
import ExerciseTestPage from "./pages/ExerciseTestPage";
import LoginPage from "./pages/LoginPage";
import CreateAccountPage from "./pages/CreateAccountPage";
import NotFoundPage from "./pages/NotFoundPage";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBNE0ra0rk5lkJ4mEpPmhkqV33E9myVsMI",
  authDomain: "dailyshed-9d748.firebaseapp.com",
  projectId: "dailyshed-9d748",
  storageBucket: "dailyshed-9d748.appspot.com",
  messagingSenderId: "883178666965",
  appId: "1:883178666965:web:ce4b9bd76c75050ad5db5c",
  measurementId: "G-Z45SE9M03G",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />} />
      {/* <Route path="/student" element={<Student />} /> */}
      <Route path="/teacher" element={<Teacher />} />
      <Route path="/studentSignIn" element={<StudentSignIn />} />
      <Route path="/exerciseList" element={<Exercises />} />
      <Route
        path="/studentExercisePage/:studentName"
        element={<StudentExercisePage />}
      />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/createAccount" element={<CreateAccountPage />} />
      <Route path="*" element={<NotFoundPage />} />
      <Route path="/studentExercisePage" element={<StudentExercisePage />} />
      <Route path="/exerciseTestPage" element={<ExerciseTestPage />} />
      <Route path="/studentPracticePage" element={<StudentPracticePage />} />
    </Routes>
  </BrowserRouter>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
