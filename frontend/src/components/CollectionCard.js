import { Container, Card } from "react-bootstrap";
import ToTitleCase from "../util/ToTitleCase";
import { useEffect, useState } from "react";

const CollectionCard = ({ i, collection }) => {
  const [collectionLength, setCollectionLength] = useState(0);

  useEffect(() => {}, []);

  return (
    <>
      <Container key={i}>
        <Card className="">
          <Card.Header>
            {collection.collectionTitle} in {ToTitleCase(collection.currentKey)}{" "}
            {ToTitleCase(collection.currentMode)}
          </Card.Header>
          <Card.Body>
            <Card.Text>
              Rhythm: {ToTitleCase(collection.rhythmMatcher)}
            </Card.Text>
          </Card.Body>
          <Card.Footer>
            Exercises completed: {collection.index + 1} of X
          </Card.Footer>
        </Card>
      </Container>
    </>
  );
};
export default CollectionCard;
