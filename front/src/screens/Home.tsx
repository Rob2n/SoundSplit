import React from "react";
import styled from "styled-components";

const Container = styled.div`
`

const Title = styled.h1`
margin: 0;
`

const Subtitle = styled.h3`
margin-top: 0.5em;
`

const Home = () => {
    return (
        <Container>
            <Title>Spliter.io</Title>
            <Subtitle>Split your audio track in one click  <span role="img" aria-labelledby="music-emoji" aria-label="music-emoji">🎶</span></Subtitle>
        </Container>
    );
}

export {Home};