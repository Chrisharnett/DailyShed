import Slider from "react-slick";
import PropTypes from "prop-types";

const Carousel = ({ children }) => {
  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 2,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 4000,
  };

  return <Slider {...settings}>{children}</Slider>;
};

Carousel.propTypes = {
  children: PropTypes.node.isRequired,
};

export default Carousel;
