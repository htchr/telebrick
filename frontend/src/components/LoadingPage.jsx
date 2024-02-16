import styled from "styled-components";

const PageWrapper = styled.div`
  align-items: center;
  display: flex;
  height: 100vh;
  justify-content: center;
  width: 100vw;
`;

function LoadingPage(props) {
  return (
    <PageWrapper>
      <span>Loading...</span>
    </PageWrapper>
  );
}

export default LoadingPage;
