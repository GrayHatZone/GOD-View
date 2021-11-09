import { IFooterDropdownContent } from '../../interfaces/design/FooterDesign.interface';
import styled from 'styled-components';

export const FooterDropdown = styled('div')`
    border-top: solid thin rgb(31, 93, 117);
    background-color: rgb(5, 32, 58);
    width: calc(100% - 1.2rem);
    text-align: center;
    position: fixed;
    bottom: 4.45rem;
    left: 0;
`;

export const FooterDropdownToggle = styled('div')`
    background-color: rgb(5, 32, 58);
    color: rgb(0, 255, 255);
    padding: 0.25rem 0;
    cursor: pointer;
`;

export const FooterWindowManager = styled('div')`
    border-top: solid thin rgb(31, 93, 117);
    background-color: rgb(5, 32, 58);
    width: calc(100% - 1.2rem);
    color: rgb(255, 255, 255);
    -ms-overflow-style: none;
    scrollbar-width: none;
    white-space: nowrap;
    text-align: center;
    overflow-x: scroll;
    overflow-y: hidden;
    position: fixed;
    height: 3.25rem;
    bottom: 1.2rem;
    left: 0;
`;

export const FooterWindowButton = styled('button')`
    border: solid thin rgb(31, 93, 117);
    background-color: rgb(5, 32, 58);
    margin: 0.578125rem 0.15rem;
    color: rgb(255, 255, 255);
    padding: 0.5rem 1.5rem;
    border-radius: 5rem;
    transition: 250ms;
`;

export const FooterWindowClear = styled('button')`
    border: solid thin rgb(225, 53, 57);
    background-color: rgb(5, 32, 58);
    margin: 0.578125rem 0.15rem;
    color: rgb(255, 255, 255);
    padding: 0.5rem 1.5rem;
    border-radius: 5rem;
    transition: 250ms;
`;

export const FooterBlock = styled('div')`
    background-color: rgb(5, 32, 58);
    color: rgb(255, 255, 255);
    margin: 1.1875rem 0;
`;

export const FooterDropdownContent = styled('div') <IFooterDropdownContent>`
    background-color: rgb(5, 32, 58);
    overflow-y: scroll;
    transition: 250ms;
    padding: 0;
    height: 0;

    ${({ active }: any) =>
        active &&
        `
        border-top: solid thin rgb(31, 93, 117);
        padding: 0.5rem 0;
        transition: 250ms;
        height: 9.2rem;

        @media (min-width: 1280px) {
            height: 7.2rem;
        }

        @media (min-width: 2000px) {
            height: 5.2rem;
        }
    `}
`;

export const FooterNameSpaceButton = styled('button')`
    border: solid thin rgb(225, 53, 57);
    background-color: rgb(225, 53, 57);
    color: rgb(255, 255, 255);
    padding: 0.4rem 1rem;
    border-radius: 5rem;
    transition: none;
    cursor: text;
    
    :active {
        transform: none;
        transition: none;
    }
`;

export const FooterDropdownButton = styled('button')`
    background-color: rgb(31, 93, 117);
    color: rgb(255, 255, 255);
    border: rgb(31, 93, 117);
    padding: 0.4rem 1rem;
    border-radius: 5rem;
    margin: 0.15rem;
`;

export const FooterMenu = styled('div')`
    border-top: solid thin rgb(31, 93, 117);
    background-color: rgb(5, 32, 58);
    width: calc(100% - 1.2rem);
    color: rgb(255, 255, 255);
    position: fixed;
    height: 1.2rem;
    bottom: 0;
    left: 0;
`;

export const FooterParagraph = styled('p')`
    text-overflow: ellipsis;
    padding-top: 0.15rem;
    white-space: nowrap;
    font-size: 0.75rem;
    overflow: hidden;
    height: 1.2rem;
    margin-top: 0;
`;
