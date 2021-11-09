import styled, { css } from 'styled-components';
import {
    IServerTableRow,
    IServerTableBar
} from '../../interfaces/design/ServerDesign.interface';

const tableColumn = css`
    border: solid thin rgb(31, 113, 145);
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 3.1rem;
    border-top: none;
    overflow: hidden;
    padding: 0.3rem;
`;

const tableResponsive = css`
    @media (max-width: 767px) {
        display: block;
    }
`;

export const ServerTable = styled('table')`
    width: calc(100% - 1.125rem);
    color: rgb(255, 255, 255);
    border-collapse: collapse;
    -webkit-user-select: none;
    -khtml-user-select: none;
    -moz-user-select: none;
    margin-bottom: 5.9rem;
    -ms-user-select: none;
    text-align: center;
    user-select: none;
    ${tableResponsive}
`;

export const ServerTableHead = styled('thead')`
    background-color: rgb(31, 93, 117);

    @media (max-width: 767px) {
        display: none;
    }
`;

export const ServerTableBody = styled('tbody')`
    background-color: rgb(5, 32, 58);
    ${tableResponsive}

    > tr:first-child {
        padding-top: 1.5rem;
    }

    > tr:last-child {
        padding-bottom: 1.5rem;
    }
`;

export const ServerTableRow = styled('tr') <IServerTableRow>`
    ${(props) => props.activeSession && `color: ${props.activeSession};`}
    padding: 0.75rem 1.5rem;
    ${tableResponsive}

    > td:first-child {
        border-top: solid thin rgb(31, 113, 145);
    }
`;

export const ServerTableHeader = styled('th')`
    ${tableColumn}
`;

export const ServerTableData = styled('td')`
    ${tableColumn}

    @media (max-width: 767px) {
        min-height: 1.4125rem;
        padding-right: 1rem;
        position: relative;
        text-align: right;
        padding-left: 45%;
        overflow: hidden;
        max-width: 100%;
        display: block;

        &:before {
            content: attr(data-label);
            position: absolute;
            padding-left: 1rem;
            text-align: left;
            width: 55%;
            left: 0;
        }
    }
`;

export const ServerTableImage = styled('img')`
    vertical-align: text-bottom;
    margin-right: 0.15rem;
    height: 0.90625rem;
    width: 0.90625rem;
`;

export const ServerTableBarBg = styled('div')`
    background-color: rgb(31, 93, 117);
`;

export const ServerTableBar = styled('div') <IServerTableBar>`
    ${(props) => props.width && `width: ${props.width}%;`}
    background-color: rgb(24, 79, 59);
    margin: 0.0625rem 0;
    height: 0.375rem;
`;

export const ServerBlock = styled('div')`
    background-color: rgb(31, 93, 117);
    width: calc(100% - 1.2rem);
    color: rgb(255, 255, 255);
    text-align: center;
    padding: 0.8rem 0;
`;
