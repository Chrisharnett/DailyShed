import React from "react";
import Container from "react-bootstrap/Container";

export const PasswordRequirements = ({ conditionsMet }) => {
  return (
    <>
      <Container>
        <p>Password Requirements</p>
        <ul className="noBulletsList">
          {conditionsMet.map((condition, index) => (
            <li key={index}>
              {condition.met} {condition.condition}
            </li>
          ))}
        </ul>
      </Container>
    </>
  );
};
