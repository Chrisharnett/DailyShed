const formatDate = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleString("en-CA", {
    month: "long",
    day: "numeric",
    year: "numeric",
  });
};
export default formatDate;
