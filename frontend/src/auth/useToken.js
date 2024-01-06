import { useState } from "react";

export const useToken = () => {
  const [token, setTokenInternal] = useState(() => {
    return localStorage.getItem("token");
  });

  const setToken = (newToken) => {
    localStorage.setItem("token", newToken);
    setTokenInternal(newToken);
  };

  return [token, setToken];
};

// const [token, setTokenInternal] = useState(() => {
//   const cookies = document.cookie.split(";");
//   for (let i = 0; i < cookies.length; i++) {
//     const cookie = cookies[i].trim();
//     if (cookie.startsWith("token=")) {
//       return cookie.substring("token=".length);
//     }
//   }
//   return null;
// });

// const setToken = (newToken) => {
//   const secureCookie = true;
//   // Currently stopping login process. Investigate and make true later. May be due to local?
//   const httpOnlyCookie = false;

//   const cookieOptions = `path=/;${secureCookie ? "secure;" : ""}${
//     httpOnlyCookie ? "HttpOnly;" : ""
//   }`;

//   document.cookie = `token=${newToken}; ${cookieOptions}`;
//   setTokenInternal(newToken);
// };
// return [token, setToken];
