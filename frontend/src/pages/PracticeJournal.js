import Container from "react-bootstrap/Container";
import TopSpacer from "../util/TopSpacer";
import axios from "axios";
import { useState, useEffect } from "react";

const PracticeJournal = ({ user, playerDetails }) => {
  const [journal, setJournal] = useState(null);

  useEffect(() => {
    const fetchJournal = async () => {
      try {
        const response = await axios.get(`/api/getUserJournal/${user.sub}`);
        setJournal(response.data);
      } catch (error) {
        console.error("Error: ", error);
      }
    };
    if (user) {
      fetchJournal();
    }
  }, [user]);

  if (!playerDetails) {
    return (
      <>
        <TopSpacer />
        <p>Loading...</p>;
      </>
    );
  } else {
    return (
      <>
        <TopSpacer />
        <Container className="midLayer glass">
          <h1>Practice Journal</h1>
          <h2 className="dropShadow"> {playerDetails.name} </h2>
        </Container>
      </>
    );
  }
};

export default PracticeJournal;
