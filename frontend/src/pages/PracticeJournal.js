import Container from "react-bootstrap/Container";
import TopSpacer from "../util/TopSpacer";
import axios from "axios";
import { useState, useEffect } from "react";
import JournalByDateEntry from "../components/JournalByDateEntry";

const PracticeJournal = ({ user, playerDetails }) => {
  const [journal, setJournal] = useState([]);

  const groupBySessionID = (journalEntries) => {
    const grouped = journalEntries.reduce((acc, journalEntry) => {
      if (!acc[journalEntry.sessionID]) {
        acc[journalEntry.sessionID] = [];
      }
      acc[journalEntry.sessionID].push(journalEntry);
      return acc;
    }, {});
    return Object.values(grouped);
  };

  useEffect(() => {
    const fetchJournal = async () => {
      try {
        const response = await axios.get(`/api/getUserJournal/${user.sub}`);
        const groupedData = groupBySessionID(response.data);
        setJournal(groupedData);
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
    console.log(journal);
    return (
      <>
        <TopSpacer />
        <Container className="midLayer glass">
          <h1>Practice Journal</h1>
          <h2 className="dropShadow"> {playerDetails.name} </h2>
          {journal.map((journalEntry, i) => {
            return <JournalByDateEntry key={i} journalEntry={journalEntry} />;
          })}
        </Container>
      </>
    );
  }
};

export default PracticeJournal;
