import { Container, Nav, Navbar } from "react-bootstrap";
import { useNavigate, useLocation } from "react-router-dom";
import { getCognitoURL } from "../../util/getCognitoURL";
import { useUserContext } from "../../auth/useUserContext";
import { applicationData } from "../../config/applicationConfig";
import { InFromAboveAnimation } from "../../animation/animations";

const Navigation = () => {
  const navigate = useNavigate();
  const { user, removeToken } = useUserContext();
  const location = useLocation();
  const { pages } = applicationData;
  const homePage = pages.find((page) => page.path === "/");
  const pageLinks = pages.filter((page) => page.path !== "/");

  const logOutHandler = () => {
    removeToken();
    navigate("/");
  };

  return (
    <>
      <Navbar
        expand="lg"
        className="navbar-dark bg-black p-3"
        id="top"
        fixed="top"
      >
        <Container fluid>
          <InFromAboveAnimation>
            <Navbar.Brand href={homePage.path}>{homePage.brand}</Navbar.Brand>
          </InFromAboveAnimation>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              {user &&
                pageLinks.map(
                  (page, index) =>
                    location.pathname !== page.path && (
                      <InFromAboveAnimation key={index}>
                        <Nav.Link href={page.path}>{page.title}</Nav.Link>
                      </InFromAboveAnimation>
                    )
                )}
            </Nav>
            <Nav className="ms-auto">
              <InFromAboveAnimation>
                {user ? (
                  <Nav.Link className="" href="#" onClick={logOutHandler}>
                    <h4>Logout</h4>
                  </Nav.Link>
                ) : (
                  <Nav.Link
                    className=""
                    href="#login"
                    onClick={() => {
                      window.location.href = getCognitoURL;
                    }}
                  >
                    <h4>Login</h4>
                  </Nav.Link>
                )}
              </InFromAboveAnimation>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </>
  );
};

export default Navigation;
