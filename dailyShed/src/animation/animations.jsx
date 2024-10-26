import { motion } from "framer-motion";
import PropTypes from "prop-types";
import {
  containerSpellerVariantDefaults,
  itemSpellerVariantDefaults,
  defaultInFromAboveAnimation,
  defaultInFromBelowAnimation,
} from "../config/animationConfig";
import AnimatedButton from "../components/AnimatedButton";

const randomizedDuration = (defaultDuration) => {
  return defaultDuration + Math.random() * 0.4 - 0.2;
};

export const InFromBelowAnimation = ({ children }) => {
  return (
    <motion.span
      initial={defaultInFromBelowAnimation.initial}
      animate={defaultInFromBelowAnimation.animate}
      transition={{
        ...defaultInFromBelowAnimation.transition,
        duration: randomizedDuration(
          defaultInFromBelowAnimation.transition.duration
        ),
      }}
    >
      {children}
    </motion.span>
  );
};
InFromBelowAnimation.propTypes = {
  children: PropTypes.node.isRequired,
};

export const InFromAboveAnimation = ({ children }) => {
  return (
    <motion.span
      initial={defaultInFromAboveAnimation.initial}
      animate={defaultInFromAboveAnimation.animate}
      transition={{
        ...defaultInFromAboveAnimation.transition,
        duration: randomizedDuration(
          defaultInFromAboveAnimation.transition.duration
        ),
      }}
    >
      {children}
    </motion.span>
  );
};

InFromAboveAnimation.propTypes = {
  children: PropTypes.node.isRequired,
};

export const FadeInContainer = ({
  children,
  startAnimation,
  setCueNextAnimation,
}) => {
  const handleAnimationComplete = () => {
    setCueNextAnimation ? setCueNextAnimation(true) : null;
  };

  return (
    <motion.div
      className="animate-list"
      variants={containerSpellerVariantDefaults}
      initial="hidden"
      animate={startAnimation ? "visible" : "hidden"}
      onAnimationComplete={handleAnimationComplete}
    >
      {children}
    </motion.div>
  );
};

FadeInContainer.propTypes = {
  children: PropTypes.node.isRequired,
  startAnimation: PropTypes.bool,
  setCueNextAnimation: PropTypes.func,
};

export const FadeInItems = ({
  items,
  startAnimation,
  setCueNextAnimation,
  handleOnClick,
}) => {
  const handleAnimationComplete = () => {
    setCueNextAnimation ? setCueNextAnimation(true) : null;
  };

  return (
    <>
      <motion.span
        className="d-flex justify-content-center"
        variants={containerSpellerVariantDefaults}
        initial="hidden"
        animate={startAnimation ? "visible" : "hidden"}
        onAnimationComplete={handleAnimationComplete}
      >
        {items?.map((item, index) => (
          <motion.span key={index} variants={itemSpellerVariantDefaults}>
            <AnimatedButton
              handleOnClick={() => handleOnClick(index)}
              buttonText={item}
            />
          </motion.span>
        ))}
      </motion.span>
    </>
  );
};

FadeInItems.propTypes = {
  items: PropTypes.array.isRequired,
  startAnimation: PropTypes.bool,
  setCueNextAnimation: PropTypes.func,
  handleOnClick: PropTypes.func,
};

export const FadeInButtons = ({
  items,
  startAnimation,
  setCueNextAnimation,
  handleOnClick,
}) => {
  const handleAnimationComplete = () => {
    setCueNextAnimation ? setCueNextAnimation(true) : null;
  };

  return (
    <>
      <motion.span
        className="d-flex justify-content-center"
        variants={containerSpellerVariantDefaults}
        initial="hidden"
        animate={startAnimation ? "visible" : "hidden"}
        onAnimationComplete={handleAnimationComplete}
      >
        {items?.map((item, index) => (
          <motion.span key={index} variants={itemSpellerVariantDefaults}>
            <AnimatedButton
              handleOnClick={() => handleOnClick(index)}
              buttonText={item}
            />
          </motion.span>
        ))}
      </motion.span>
    </>
  );
};

FadeInButtons.propTypes = {
  items: PropTypes.array.isRequired,
  startAnimation: PropTypes.bool,
  setCueNextAnimation: PropTypes.func,
  handleOnClick: PropTypes.func,
};

export const SpellItOutAnimation = ({
  stringToSplit,
  startAnimation,
  setCueNextAnimation,
}) => {
  const elements = stringToSplit?.split("");
  const handleAnimationComplete = () => {
    setCueNextAnimation ? setCueNextAnimation(true) : null;
  };

  return (
    <motion.div
      className="animate-list"
      variants={containerSpellerVariantDefaults}
      initial="hidden"
      animate={startAnimation ? "visible" : "hidden"}
      onAnimationComplete={handleAnimationComplete}
    >
      {elements?.map((letter, index) => (
        <motion.span key={index} variants={itemSpellerVariantDefaults}>
          {letter === " " ? "\u00A0" : letter}
        </motion.span>
      ))}
    </motion.div>
  );
};

SpellItOutAnimation.propTypes = {
  startAnimation: PropTypes.bool,
  stringToSplit: PropTypes.string.isRequired,
  setCueNextAnimation: PropTypes.func,
};
