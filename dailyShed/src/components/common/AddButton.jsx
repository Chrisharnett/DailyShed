import PropTypes from "prop-types";
import { motion } from "framer-motion";

const AddButton = ({ onClick, ariaLabel, title }) => {
  return (
    <motion.div className="tooltip-container">
      <motion.button
        whileHover={{ scale: 1.2 }}
        whileTap={{ scale: 0.8 }}
        className="addIntervalButton"
        type="button"
        onClick={onClick}
        aria-label={ariaLabel ? ariaLabel : "Add"}
      >
        +
      </motion.button>
      <span className="tooltip-text">{title ? title : "Add"}</span>
    </motion.div>
  );
};

AddButton.propTypes = {
  onClick: PropTypes.func.isRequired,
  ariaLabel: PropTypes.string,
  title: PropTypes.string,
};

export default AddButton;
