import styled from "styled-components";

const ImageWrapper = styled.div`
  height: fit-content;
`;

export const StyledImage = styled.img`
  width: 50vw;

  @media screen and (max-width: 800px) {
    width: 100%;
  }
`;

function Image(props) {
  return (
    <ImageWrapper>
      <StyledImage alt="Latest capture of recipient" src={props.path} />
    </ImageWrapper>
  );
}

export default Image;
