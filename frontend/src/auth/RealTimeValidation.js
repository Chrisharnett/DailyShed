import React from "react";
import { useState } from "react";
import Form from "react-bootstrap/Form";

export const initialConditionsMet = [
  { condition: "At least 8 characters long", met: "  " },
  { condition: "Contain at least one uppercase letter", met: "  " },
  { condition: "Contain at least one number", met: " " },
  { condition: "Contain at least one special character", met: "  " },
];

export const RealTimeValidation = ({ passwordValue, onPasswordChange }) => {
  const handlePasswordChange = (e) => {
    const newPasswordValue = e.target.value;
    const conditionsMet = initialConditionsMet.map((item) => ({ ...item }));

    if (newPasswordValue.length >= 8) {
      conditionsMet[0].met = "\u2705";
    }
    if (/[A-Z]/.test(newPasswordValue)) {
      conditionsMet[1].met = "\u2705";
    }
    if (/\d/.test(newPasswordValue)) {
      conditionsMet[2].met = "\u2705";
    }
    if (/[!@#$%^&*(),.?":{}|<>]/.test(newPasswordValue)) {
      conditionsMet[3].met = "\u2705";
    }

    onPasswordChange(newPasswordValue, conditionsMet);
  };

  return (
    <>
      <Form.Group className="mb-3">
        <Form.Label className="blue-text" htmlFor="password">
          Password:{" "}
        </Form.Label>
        <Form.Control
          id="password"
          type="password"
          placeholder="password"
          value={passwordValue}
          onChange={handlePasswordChange}
        />
      </Form.Group>
    </>
  );
};
