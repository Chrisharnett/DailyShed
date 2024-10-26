export const defaultInFromBelowAnimation = {
  initial: { y: 30, opacity: 1 },
  animate: { y: 0, opacity: 1 },
  transition: { duration: 1, ease: "easeOut" },
};

export const defaultInFromAboveAnimation = {
  initial: { y: -30, opacity: 1 },
  animate: { y: 0, opacity: 1 },
  transition: { duration: 1, ease: "easeOut" },
};

export const containerSpellerVariantDefaults = {
  hidden: { opacity: 1, scale: 0 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: {
      duration: 1,
      delayChildren: 0.5,
      staggerChildren: 0.3,
    },
  },
};

export const itemSpellerVariantDefaults = {
  hidden: {
    opacity: 0,
    y: 20,
  },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.5,
      ease: "easeOut",
    },
  },
};
