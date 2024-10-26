import { Container, Card, Form, Button } from "react-bootstrap";
import ToTitleCase from "../util/ToTitleCase";
import { useEffect, useState } from "react";
import { saveUserProgram } from "../util/flaskRoutes";
import axios from "axios";
import PropTypes from "prop-types";

const ProgramBuilderCard = ({
  user,
  rhythmCollections,
  scalePatternPrograms,
  tonicSequences,
  instruments,
  modes,
  userDefaultInstrument,
  setMessage,
  setOpenSuccessMessage,
  handleProgramUpdate,
}) => {
  const [newProgram, setNewProgram] = useState({
    scaleMode: null,
    rhythmCollection: null,
    primaryCollection: null,
    tonicSequence: null,
    instrument: null,
    startingTonic: null,
  });
  const [allSet, setAllSet] = useState(false);
  const [matchingRhythms, setMatchingRhythms] = useState([]);
  const [allKeys, setAllKeys] = useState(false);

  useEffect(() => {
    if (
      instruments.length > 0 &&
      modes.length > 0 &&
      scalePatternPrograms.length > 0 &&
      rhythmCollections.length > 0 &&
      tonicSequences.length > 0
    ) {
      const instrument = instruments.find(
        (instrument) => instrument.instrumentName === userDefaultInstrument
      );
      const mode = modes[0];
      const scalePatternType = scalePatternPrograms[0];
      const tonicSequence = tonicSequences[0];

      setNewProgram({
        scaleMode: mode,
        rhythmCollection: null,
        primaryCollection: scalePatternType,
        tonicSequence: tonicSequence,
        startingTonic: instrument ? instrument.defaultTonic[0] : "",
        instrument: instrument || null,
      });
      setAllSet(true);
    }
  }, [
    instruments,
    modes,
    scalePatternPrograms,
    rhythmCollections,
    tonicSequences,
    userDefaultInstrument,
  ]);

  useEffect(() => {
    if (newProgram.primaryCollection) {
      const scaleProgram = newProgram.primaryCollection;
      const collections = rhythmCollections.filter(
        (rhythm) => rhythm.collectionType === scaleProgram.rhythmType
      );
      setMatchingRhythms(collections);
      setNewProgram((prevProgram) => ({
        ...prevProgram,
        rhythmCollection: collections.length > 0 ? collections[0] : null,
      }));
    }
  }, [newProgram.primaryCollection, rhythmCollections]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    let selectedObject = null;

    switch (name) {
      case "scaleMode":
        selectedObject = modes.find(
          (mode) => mode.scaleModeID === parseInt(value)
        );
        break;
      case "rhythmCollection":
        selectedObject = rhythmCollections.find(
          (collection) => collection.collectionID === parseInt(value)
        );
        break;
      case "primaryCollection":
        selectedObject = scalePatternPrograms.find(
          (program) => program.scalePatternType === value
        );
        setAllKeys(selectedObject.allKeys);
        break;
      case "tonicSequence":
        selectedObject = tonicSequences.find(
          (sequence) => sequence.tonicSequenceID === parseInt(value)
        );
        break;
      case "instrument":
        selectedObject = instruments.find(
          (instrument) => instrument.instrumentID === parseInt(value)
        );
        break;
      case "startingTonic":
        selectedObject = value;
        break;
      default:
        break;
    }

    setNewProgram((prevProgram) => ({
      ...prevProgram,
      [name]: selectedObject,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const program = {
      sub: user.sub,
      scaleModeID: newProgram.scaleMode.scaleModeID,
      rhythmCollectionID: newProgram.rhythmCollection.collectionID,
      primaryCollectionTitle:
        newProgram.scaleMode.scaleModeName +
        "," +
        newProgram.primaryCollection.scalePatternType,
      tonicSequenceID: newProgram.tonicSequence.tonicSequenceID,
      instrumentID: newProgram.instrument.instrumentID,
      startingTonicIndex: newProgram.tonicSequence.sequence.indexOf(
        newProgram.startingTonic
      ),
    };

    try {
      const response = await axios.post(`${saveUserProgram}`, { program });
      setMessage("Program Saved!");
      setOpenSuccessMessage(true);
      handleProgramUpdate(response.data);
    } catch (error) {
      console.error("Error: ", error);
    }
  };

  if (!allSet) {
    return <div>Loading...</div>;
  }

  return (
    <Container>
      <Card className="">
        <Card.Header>
          <Form.Label className="">Create a program</Form.Label>
          <Form.Select
            name="primaryCollection"
            value={
              newProgram.primaryCollection
                ? newProgram.primaryCollection.scalePatternType
                : ""
            }
            onChange={handleInputChange}
          >
            {scalePatternPrograms.map((program, index) => (
              <option key={index} value={program.scalePatternType}>
                {ToTitleCase(program.scalePatternType)}
              </option>
            ))}
          </Form.Select>
        </Card.Header>
        <Card.Body>
          <Card.Text>
            <Form.Label className="">Mode:</Form.Label>
            <Form.Select
              name="scaleMode"
              value={
                newProgram.scaleMode ? newProgram.scaleMode.scaleModeID : ""
              }
              onChange={handleInputChange}
            >
              {modes.map((mode, index) => (
                <option key={index} value={mode.scaleModeID}>
                  {ToTitleCase(mode.scaleModeName)}
                </option>
              ))}
            </Form.Select>
          </Card.Text>
          {allKeys ? (
            <>
              <Card.Text>
                <Form.Label>Starting Key:</Form.Label>
                <Form.Select
                  name="startingTonic"
                  value={newProgram.startingTonic || ""}
                  onChange={handleInputChange}
                >
                  {newProgram.tonicSequence.sequence.map((tonic, index) => (
                    <option key={index} value={tonic}>
                      {ToTitleCase(tonic)}
                    </option>
                  ))}
                </Form.Select>
              </Card.Text>
              <Card.Text>
                <Form.Label className="">Key Sequence:</Form.Label>
                <Form.Select
                  name="tonicSequence"
                  value={
                    newProgram.tonicSequence
                      ? newProgram.tonicSequence.sequenceID
                      : ""
                  }
                  onChange={handleInputChange}
                >
                  {tonicSequences.map((sequence, index) => (
                    <option key={index} value={sequence.tonicSequenceID}>
                      {ToTitleCase(sequence.name)}
                    </option>
                  ))}
                </Form.Select>
              </Card.Text>
            </>
          ) : (
            <>
              <Card.Text>
                <Form.Label>Key:</Form.Label>
                <Form.Select
                  name="startingTonic"
                  value={newProgram.startingTonic || ""}
                  onChange={handleInputChange}
                >
                  {newProgram.tonicSequence.sequence.map((tonic, index) => (
                    <option key={index} value={tonic}>
                      {ToTitleCase(tonic)}
                    </option>
                  ))}
                </Form.Select>
              </Card.Text>
            </>
          )}
          <Card.Text>
            <Form.Label className="">Instrument:</Form.Label>
            <Form.Select
              name="instrument"
              value={
                newProgram.instrument ? newProgram.instrument.instrumentID : ""
              }
              onChange={handleInputChange}
            >
              {instruments.map((instrument, index) => (
                <option key={index} value={instrument.instrumentID}>
                  {ToTitleCase(instrument.level) +
                    " " +
                    ToTitleCase(instrument.instrumentName)}
                </option>
              ))}
            </Form.Select>
          </Card.Text>
          <Card.Text>
            <Form.Label className="">Rhythm:</Form.Label>
            <Form.Select
              name="rhythmCollection"
              value={
                newProgram.rhythmCollection
                  ? newProgram.rhythmCollection.collectionID
                  : ""
              }
              onChange={handleInputChange}
            >
              {matchingRhythms.map((rhythms, index) => (
                <option key={index} value={rhythms.collectionID}>
                  {ToTitleCase(rhythms.collectionTitle)}
                </option>
              ))}
            </Form.Select>
          </Card.Text>
        </Card.Body>
        <Card.Footer>
          <Button onClick={handleSubmit}>Save Program</Button>
        </Card.Footer>
      </Card>
    </Container>
  );
};

ProgramBuilderCard.propTypes = {
  user: PropTypes.object,
  rhythmCollections: PropTypes.array,
  scalePatternPrograms: PropTypes.array,
  tonicSequences: PropTypes.array,
  instruments: PropTypes.array,
  modes: PropTypes.array,
  userDefaultInstrument: PropTypes.string,
  setMessage: PropTypes.func,
  setOpenSuccessMessage: PropTypes.func,
  handleProgramUpdate: PropTypes.func,
};

export default ProgramBuilderCard;
