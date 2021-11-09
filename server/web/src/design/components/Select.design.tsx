import styled from 'styled-components';

export const SelectContainer = styled('div')`
    position: fixed;
`;

export const SelectRow = styled('div')`
    border-bottom: solid thin rgb(31, 113, 145);
    border-right: solid thin rgb(31, 113, 145);
    border-left: solid thin rgb(31, 113, 145);
    background-color: rgb(5, 32, 58);
    font-size: 0.8rem;
    transition: 250ms;
    padding: 0.4rem;
    cursor: pointer;
    width: 8.5rem;

    :hover {
        background-color: rgb(0, 55, 117);
        transition: 250ms;
    }

    :first-child {
        border-top: solid thin rgb(31, 113, 145);
        border-top-right-radius: 0.25rem;
        border-top-left-radius: 0.25rem;
    }

    :last-child {
        border-bottom-right-radius: 0.25rem;
        border-bottom-left-radius: 0.25rem;
    }

    > svg {
        vertical-align: text-bottom;
    }
`;
