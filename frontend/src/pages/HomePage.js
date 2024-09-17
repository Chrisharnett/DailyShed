import { Container } from "react-bootstrap";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { getCognitoURL } from "../util/getCognitoURL";

const HomePage = ({ loggedIn, user }) => {
  const [entryLink, setEntryLink] = useState(null);

  useEffect(() => {
    if (loggedIn) {
      setEntryLink(`/theShed`);
    } else {
      setEntryLink(getCognitoURL);
    }
  }, [loggedIn]);

  return (
    <>
      <Container
        className="d-flex justify-content-center position-relative"
        style={{ height: "100vh", width: "100vw" }}
      >
        <Link to={entryLink}>
          <Container className="midLayer glass entry">
            <h1 className="dropShadow ">Enter the shed</h1>
          </Container>
        </Link>
      </Container>
    </>
  );
};

export default HomePage;
