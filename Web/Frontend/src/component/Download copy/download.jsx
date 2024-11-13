import React from 'react';
import styled from 'styled-components';
import DownloadMain from './downloadmain';
import { Link } from "react-router-dom";

export default function Download() {
    return (
        <StyledPrinterList>
            <StyledHeader>
                <Title>Hoat dong gi do</Title>
                <>
                  <Link to={`/`} className="btn btn-primary ">+ Add file </Link>
                </>
            </StyledHeader>
            <hr />
            <DownloadMain/>
        </StyledPrinterList>
    );
};
  
const StyledPrinterList = styled.section`
    background-color: #fff;
    border-radius: 8px;
    padding: 24px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const StyledHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
`;

const Title = styled.h2`
  color: #242222;
  font-size: 16px;
  font-weight: 600;
`;