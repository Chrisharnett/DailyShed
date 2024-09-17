import Container from "react-bootstrap/Container";
import axios from "axios";
import { useState, useEffect } from "react";
import JournalExerciseCard from "../components/JournalExerciseCard";
import { getUserJournal } from "../util/flaskRoutes";

const PracticeJournal = ({ user }) => {
  const [journal, setJournal] = useState([]);
  const [userName, setUserName] = useState("");

  useEffect(() => {
    const fetchJournal = async () => {
      try {
        const response = await axios.post(`${getUserJournal}/${user.sub}`);
        const { userName, exerciseHistory } = response.data.userHistory;
        setJournal(exerciseHistory);
        setUserName(userName);
      } catch (error) {
        console.error("Error: ", error);
      }
    };
    if (user) {
      fetchJournal();
    }
  }, [user]);

  if (!journal || !userName) {
    return (
      <>
        <p>Loading...</p>;
      </>
    );
  } else {
    return (
      <>
        <Container className="midLayer glass">
          <h1>{userName}'s Practice Journal</h1>
          <Container className="journal">
            {journal.map((journalEntry, i) => {
              return <JournalExerciseCard key={i} exercise={journalEntry} />;
            })}
          </Container>
        </Container>
      </>
    );
  }
};

export default PracticeJournal;
