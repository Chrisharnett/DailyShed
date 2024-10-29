import { Button } from "react-bootstrap";
import { motion } from "framer-motion";
import PropTypes from "prop-types";

const AnimatedButton = ({ handleOnClick, buttonText, variant }) => {
  return (
    <Button
      as={motion.button}
      whileHover={{ scale: 1.2 }}
      whileTap={{ scale: 0.8 }}
      onClick={handleOnClick}
      className="m-2"
      variant={variant ? variant : "success"}
    >
      {buttonText}
    </Button>
  );
};

AnimatedButton.propTypes = {
  buttonText: PropTypes.string,
  handleOnClick: PropTypes.func.isRequired,
  variant: PropTypes.string,
};

export default AnimatedButton;
