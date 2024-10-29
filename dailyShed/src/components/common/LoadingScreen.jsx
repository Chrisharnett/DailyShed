import { Container } from "react-bootstrap";
import PropTypes from "prop-types";
import { FadeInContainer } from "../../animation/animations";
import { useEffect, useState } from "react";

const LoadingScreen = ({ message }) => {
  const [waitingAnimation, setWaitingAnimation] = useState("");
  const [displayMessage, setDisplayMessage] = useState("");

  useEffect(() => {
    if (!message) {
      setDisplayMessage("Loading page");
    } else {
      setDisplayMessage(message);
    }
  }, []);

  setTimeout(() => {
    if (waitingAnimation.length > 3) {
      setWaitingAnimation("");
    } else {
      setWaitingAnimation(waitingAnimation + ".");
    }
  }, 1000);

  return (
    <FadeInContainer startAnimation={true}>
      <Container className="midLayer glass">
        <div className="titles p-2">
          <h2 className="dropShadow">
            {displayMessage}
            {waitingAnimation}
          </h2>
        </div>
      </Container>
    </FadeInContainer>
  );
};

LoadingScreen.propTypes = {
  message: PropTypes.string,
};

export default LoadingScreen;
