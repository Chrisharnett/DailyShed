import Container from "react-bootstrap/Container";
import useUser from "../auth/useUser";
import ExerciseCard from "../components/ExerciseCard";
import { useState, useEffect } from "react";
import axios from "axios";

const Collections = () => {
  return (
    <>
      <Container className="midLayer glass">
        <h2>Collection Viewer</h2>
      </Container>
    </>
  );
};

export default Collections;
