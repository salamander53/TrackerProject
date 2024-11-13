import React from "react";
import styled from "styled-components";
import { menuItems } from "./navdata";
import MenuItem from "./navitem";
import PageHeader from "./header";

function NavigationMenu(props) {
  const { content } = props;
  return (
    <>
    <Container>
      <Nav>
        <Header>
          <Logo src="https://cdn.builder.io/api/v1/image/assets/39b01875d7164623805557885af3caf0/f6972f0b75853885fbb0cbf0bc9d69ff06b8d702eda0c0aa88648b183a111562?apiKey=39b01875d7164623805557885af3caf0&" alt="BK SSPS Logo" />
          <Title>STA</Title>
        </Header>
        <MenuList>
          {menuItems.map((item, index) => (
            <MenuItem key={index} {...item} />
          ))}
        </MenuList>
        <Logout>
          <MenuItem
            icon= "https://cdn.builder.io/api/v1/image/assets/39b01875d7164623805557885af3caf0/5a59f03d7e03ac2566b68edf99594bdec686e930bb556eb79eee39785c6c7a04?apiKey=39b01875d7164623805557885af3caf0&"
            label= "Đăng xuất"
            isActive= {false}
            isLogout= {true}
            link= "logout"
          />
        </Logout>
      </Nav>
      <Content>
        <PageHeader/>
        {content}
      </Content>
    </Container>
    </>
  );
};
const Container = styled.div`
  display: flex;
`;

const Nav = styled.nav`
  display: flex;
  width: 210px;
  flex-direction: column;
  overflow: hidden;
  font: 600 16px Segoe UI, sans-serif;
  background-color: #fff;
  padding: 40px 0 0 0;
  height: 100vh;
  box-sizing: border-box
`;

const Header = styled.header`
  align-self: center;
  display: flex;
  gap: 11px;
  color: #3497f9;
  letter-spacing: 1.6px;
  font: 700 20px Sarala, sans-serif;
  margin-bottom: 40px;
`;

const Logo = styled.img`
  aspect-ratio: 1;
  object-fit: contain;
  object-position: center;
  width: 36px;
`;

const Title = styled.h1`
  transform: rotate(-0.005163154802990027rad);
  margin: auto;
`;

const MenuList = styled.ul`
  list-style-type: none;
  padding: 0;
  margin: 0;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
`;
const Logout = styled.ol`
  padding: 0;
  margin: 0;
`;
const Content = styled.div`
  flex-grow: 1;
  padding: 30px 40px;
  background-color: #F1F8FF;
`;
export default NavigationMenu;