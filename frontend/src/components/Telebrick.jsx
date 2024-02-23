import { useEffect, useState } from "react";
import styled from "styled-components";
import Image from "./Image";
import Item from "./Item";
import LoadingPage from "./LoadingPage";

/* Styles and components to render the correct visuals */
const StyledWrapper = styled.div`
  align-items: center;
  display: flex;
  height: 100vh;
  padding: 0 20px;
  gap: 36px;

  @media screen and (max-width: 800px) {
    align-items: flex-start;
    flex-direction: column;
  }
`;

const InfoWrapper = styled.div``;

/*
  Main component that fetches the latest data from the server and renders the
  necessary components
*/
function Telebrick() {
  // State to manage the loading state and the data
  const [loading, setLoading] = useState(true);
  // State to store the latest available data
  const [data, setData] = useState(null);

  // TODO: Replace with the correct server URL
  const serverUrl = "http://localhost:80";

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`${serverUrl}/latest`, {
          mode: "cors", // Specify cors mode explicitly
        });

        if (!response.ok) {
          throw new Error("There's something wrong with the request");
        } else {
          const data = await response.json();

          setData(data);
          setLoading(false);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
        setLoading(true);
      }
    };

    fetchData();

    const MULTIPLIER = 1000;
    const intervalId = setInterval(fetchData, 30 * MULTIPLIER);
    return () => clearInterval(intervalId);
  }, []);

  return loading ? (
    <LoadingPage />
  ) : (
    <StyledWrapper>
      {/*
        Update the path to use `im_name` for the image name.
        Assume `im_name` contains the complete path to the image.
      */}
      <Image path={`/images/${data.im_name}`} />
      <InfoWrapper>
        {/*
          Update to use `per_full` to display the percentage of fullness,
          `full` to indicate if it's full or not, and `mixd` to indicate if the content is mixed.
        */}
        <Item>{data.mixd ? "MIXED CONTENTS" : "UNMIXED CONTENTS"}</Item>
        <Item>{data.full ? "FULL" : `NOT FULL - ${data.per_full}% FULL`}</Item>
      </InfoWrapper>
    </StyledWrapper>
  );
}

export default Telebrick;
