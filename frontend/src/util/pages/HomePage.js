import { Container } from "react-bootstrap";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import getCognitoURL from "../auth/getCognitoURL";

const HomePage = ({ loggedIn }) => {
  const [entryLink, setEntryLink] = useState(null);

  useEffect(() => {
    const fetchURL = async () => {
      console.log(loggedIn);
      if (!loggedIn) {
        try {
          const url = await getCognitoURL();
          setEntryLink(url);
        } catch (error) {
          console.error("Failed to fetch Cognito URL", error);
        }
      } else {
        setEntryLink("/theShed");
      }
    };
    fetchURL();
  }, [loggedIn]);

  return (
    <>
      <Container
        className="d-flex align-items-center justify-content-center"
        style={{ height: "100vh", width: "100vw" }}
      >
        <Link to={entryLink}>
          <Container className="midlayer glass d-flex align-items-center justify-content-center">
            <Container className="glass d-flex flex-column align-items-center m-2">
              <h1 className="boxShadowText"> Enter the Shed </h1>
            </Container>
          </Container>
        </Link>
      </Container>

      <div style={{ height: "10vh" }}></div>
    </>
  );
};

export default HomePage;
