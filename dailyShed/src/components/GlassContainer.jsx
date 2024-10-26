import PropTypes from "prop-types";
import { Container } from "react-bootstrap";
import { FadeInContainer } from "../animation/animations";

const GlassContainer = ({
  title,
  subtitle,
  startAnimation,
  cueNextAnimation,
  children,
}) => {
  return (
    <FadeInContainer
      startAnimation={startAnimation}
      setCueNextAnimation={cueNextAnimation}
    >
      <Container className="midLayer glass">
        <div className="titles p-2">
          <h2 className="dropShadow">{title}</h2>
          <h3 className="dropShadow">{subtitle}</h3>
        </div>
        {children}
      </Container>
    </FadeInContainer>
  );
};

GlassContainer.propTypes = {
  title: PropTypes.string,
  subtitle: PropTypes.string,
  children: PropTypes.node,
  startAnimation: PropTypes.bool,
  cueNextAnimation: PropTypes.func,
};
export default GlassContainer;
