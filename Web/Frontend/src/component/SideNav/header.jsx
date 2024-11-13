import React from 'react';
import styled from 'styled-components';
import { useLocation } from 'react-router-dom';

export default function PageHeader() {
    const locate = useLocation().pathname;
  return (
    <StyledHeader>
      <Title>{locate.startsWith(`/upload`)?"Upload":locate.startsWith(`/download`)?"Download":"Bảng điều kiển"}</Title>
      <UserInfo>
        <NotificationIcon src="https://cdn.builder.io/api/v1/image/assets/39b01875d7164623805557885af3caf0/1536e40067cc9c265ca9de5605af3aeda05bbc6389ff63cfa22ac6417e4e4a6c?apiKey=39b01875d7164623805557885af3caf0&" alt="Notifications" />
        <UserAvatar src="https://cdn.builder.io/api/v1/image/assets/39b01875d7164623805557885af3caf0/3e7ee5f7efa15ee1e32ed01722ce44a19533e6369533646fe057c47b06e76753?apiKey=39b01875d7164623805557885af3caf0&" alt="User Avatar" />
        <UserDetails>
          <UserName>Võ Lý Đắc Duy</UserName>
          <UserRole>User</UserRole>
        </UserDetails>
      </UserInfo>
    </StyledHeader>
  );
};

const StyledHeader = styled.header`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
`;

const Title = styled.h1`
  color: #374858;
  font: 700 23px Segoe UI, sans-serif;
  margin: 0;
`;

const UserInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  font-family: Poppins, sans-serif;
`;

const NotificationIcon = styled.img`
  width: 24px;
  height: 24px;
  object-fit: contain;
  margin-right: 12px;
`;

const UserAvatar = styled.img`
  width: 40px;
  height: 40px;
  object-fit: contain;
  border-radius: 100%;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.161);
`;

const UserDetails = styled.div`
  display: flex;
  flex-direction: column;
`;

const UserName = styled.span`
  color: #374858;
  font-size: 12px;
  font-weight: 500;
`;

const UserRole = styled.span`
  color: #808080;
  font-size: 11px;
  font-weight: 400;
  margin-top: 4px;
`;