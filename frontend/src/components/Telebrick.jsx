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
  const serverUrl = "http://localhost:8000";

  /*
    The function inside useEffect will be called when the page first loads, and
    every 30 seconds, to retrieve the latest data from the server
  */
  useEffect(() => {
    const fetchData = async () => {
      // Get the data from the backend
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
        // Display error message if there's been an error
        console.error("Error fetching data:", error);
        setLoading(true);
      }
    };

    fetchData();

    // Set the interval to fetch the data every 30 seconds
    const MULTIPLIER = 1000;
    const intervalId = setInterval(fetchData, 30 * MULTIPLIER);
    // Clear the interval for optimization
    return () => clearInterval(intervalId);
  }, []);

  /*
    Render loading page if the data is still being fetched, otherwise render the
    information provided by the server
  */
  return loading ? (
    <LoadingPage />
  ) : (
    <StyledWrapper>
      {/*
        The server will return the path to the latest capture from the recipient in
        the following format: images/202402052150.jpg; with the image being named by
        the date and time it was taken. We concat the server URL with the path to the
        image to display it in the Image component.
      */}
      <Image path={`${data.image}`} />
      <InfoWrapper>
        {/*
          The server will return an object with the following structure:
            data: { light: boolean, full: boolean, image: string }
          If data.light is true, we display "LIGHT ON", otherwise we display "LIGHT OFF".
          If data.full is true, we display "FULL", otherwise we display "NOT FULL".
        */}
        <Item>LIGHT {data.light ? "ON" : "OFF"}</Item>
        <Item>{!data.full && "NOT "}FULL</Item>
        {/* <Item>{data.percentage}% full</Item> */}
      </InfoWrapper>
    </StyledWrapper>
  );
}

export default Telebrick;