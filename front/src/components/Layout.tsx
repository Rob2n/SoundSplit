import React from "react";
import styled from "styled-components";
import {Menu} from "components/Menu";

const Container = styled.div`
    height: 100%;
`

const Content = styled.div`
padding: 1.5em;
`

const Layout: React.FC = ({children}) => {
    return (
        <Container>
            <Menu />
            <Content>
                {children}
            </Content>
        </Container>
    );
}

export {Layout};