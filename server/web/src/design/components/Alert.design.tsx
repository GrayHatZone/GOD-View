import { IAlertButton } from '../../interfaces/design/AlertDesign.interface';
import styled from 'styled-components';

const calcBgColor = (color: string) => {
    switch (color) {
        case 'SUCCESS':
            return 'rgb(24, 79, 59)';
        case 'DANGER':
            return 'rgb(175, 45, 45)';
        case 'WARNING':
            return 'rgb(175, 121, 21)';
        case 'INFO':
            return 'rgb(23, 52, 102)';
    }
};

export const AlertButton = styled('div') <IAlertButton>`
    background-color: ${(props) => calcBgColor(props.bgColor)};
    border: solid thin rgb(255, 255, 255);
    grid-template-columns: 1fr auto;
    color: rgb(255, 255, 255);
    align-items: center;
    min-height: 2.5rem;
    text-align: center;
    font-size: 0.8rem;
    width: 17.5rem;
    display: grid;

    @media (min-width: 768px) {
        width: 22.5rem;
    }
`;

export const AlertButtonCross = styled('span')`
    border-left: solid thin rgb(255, 255, 255);
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    -khtml-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    padding: 0.5rem 1rem;
    align-items: center;
    font-size: 1.25rem;
    user-select: none;
    cursor: pointer;
    display: grid;
    height: 100%;
`;
