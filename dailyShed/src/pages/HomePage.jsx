import { Container } from "react-bootstrap";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { getCognitoURL } from "../util/getCognitoURL";
import { useUserContext } from "../auth/useUserContext";
import GlassContainer from "../components/common/GlassContainer";

const HomePage = () => {
  const [entryLink, setEntryLink] = useState(null);
  const { user, loading } = useUserContext();

  useEffect(() => {
    if (!loading && user) {
      setEntryLink(`/theShed`);
    } else {
      setEntryLink(getCognitoURL);
    }
  }, []);

  return (
    <>
      <Container
        className="d-flex justify-content-center position-relative"
        style={{ height: "100vh", width: "100vw" }}
      >
        <Link to={entryLink}>
          <GlassContainer title="Start Shedding" startAnimation={true} />
        </Link>
      </Container>
    </>
  );
};

export default HomePage;
