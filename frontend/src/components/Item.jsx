import styled from "styled-components";

const StyledItem = styled.p``;

function Item(props) {
  return <StyledItem>{props.children}</StyledItem>;
}

export default Item;
