import 'bootstrap/dist/css/bootstrap.css'
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { App, Teacher, StudentSignIn, Exercises, StudentPracticePage } from './App';
import reportWebVitals from './reportWebVitals';
import { 
  BrowserRouter, 
  Routes, 
  Route } from "react-router-dom";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />} />
      {/* <Route path="/student" element={<Student />} /> */}
      <Route path="/teacher" element={<Teacher />} />
      <Route path="/studentSignIn" element={<StudentSignIn />} />
      <Route path="/exerciseList" element={<Exercises />} />
      <Route path="/studentPracticePage/:studentName" element={<StudentPracticePage />} />
    </Routes>
  </BrowserRouter>,
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
