import { Form, Container, Card } from "react-bootstrap";
import { useEffect, useState } from "react";
import axios from "axios";

const CollectionCard = ({ i, collection }) => {
  return (
    <>
      <Container key={i}>
        <Card className="">
          <Card.Header>Title: {collection.title}</Card.Header>
          <Card.Body>
            <Card.Text>
              Key: {collection.currentKey} {collection.currentMode}
            </Card.Text>
          </Card.Body>
          <Card.Footer>
            Exercises completed: {collection.index} of X
          </Card.Footer>
        </Card>
      </Container>
    </>
  );
};
export default CollectionCard;
