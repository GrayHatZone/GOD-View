import { ISidebarSlide } from '../../interfaces/design/SidebarDesign.interface';
import styled from 'styled-components';

export const SidebarDropdown = styled('div')`
    background-color: rgb(5, 32, 58);
    grid-template-columns: 1fr auto;
    color: rgb(0, 255, 255);
    position: fixed;
    display: grid;
    height: 100%;
    z-index: 999;
    right: 0;
    top: 0;
`;

export const SidebarDropdownButton = styled('div')`
    border-left: solid thin rgb(31, 113, 145);
    padding: 0 0.25rem 0 0.2rem;
    color: rgb(0, 255, 255);
    align-items: center;
    cursor: pointer;
    width: 1.2rem;
    display: grid;
    height: 100vh;
    z-index: 999;
`;

export const SidebarDropdownContent = styled('div') <ISidebarSlide>`
    overflow-x: hidden;
    text-align: center;
    transition: 250ms;
    overflow-y: auto;
    opacity: 0;
    padding: 0;
    width: 0;

    ${({ active }: any) =>
        active &&
        `
        border-left: solid thin rgb(31, 113, 145);
        width: calc(100vw - 1.2rem);
        opacity: 1;

        @media (min-width: 576px) {
            width: 65vw;
        }
    `}
`;

export const SidebarStreamContent = styled('div')`
    @media (min-width: 992px) {
        padding: 0.5rem 0;
    }

    @media (min-width: 1200px) {
        padding: 1rem 0;
    }

    @media (min-width: 1600px) {
        padding: 1.5rem 0;
    }
`;

export const SidebarStream = styled('div')`
    border-bottom: solid thin rgb(31, 113, 145);
    border-top: solid thin rgb(31, 113, 145);
    background-color: rgb(5, 32, 58);
    color: rgb(255, 255, 255);
    text-align: center;
    padding: 0.8rem 0;
`;

export const SidebarStreamSection = styled('div')`
    grid-template-columns: 1fr auto;
    display: grid;
`;

export const SidebarStreamInput = styled('input')`
    padding: 0.45rem 0.45rem 0.45rem 0.6rem;
    border: solid thin rgb(31, 93, 117);
    background-color: rgb(5, 32, 58);
    width: calc(100% - 0.8rem);
    color: rgb(255, 255, 255);
    border-radius: 5rem;
    font-size: 0.8rem;
    margin: 0.4rem;
`;

export const SidebarStreamButton = styled('button')`
    border: solid thin rgb(31, 93, 117);
    background-color: rgb(5, 32, 58);
    margin: 0.4rem 0.4rem 0.4rem 0;
    color: rgb(255, 255, 255);
    padding: 0.5rem 2rem;
    border-radius: 5rem;
    transition: 250ms;

    @media (min-width: 576px) {
        padding: 0.5rem 4rem;
    } 
`;

export const SidebarBlock = styled('div')`
    background-color: rgb(31, 93, 117);
    color: rgb(255, 255, 255);
    text-align: center;
    padding: 0.8rem 0;
`;
