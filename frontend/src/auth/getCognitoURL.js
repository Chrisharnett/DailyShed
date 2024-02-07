import axios from "axios";

const getCognitoURL = async () => {
  try {
    const response = await axios.get("/api/auth/cognito/url");
    const { url } = response.data;
    return url;
  } catch (e) {
    console.log(e);
  }
};

export default getCognitoURL;
