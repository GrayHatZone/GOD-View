import styled from 'styled-components';

export const CardContainer = styled('div')`
    border: solid thin rgb(31, 113, 145);
    background-color: rgb(5, 32, 58);
    // CONSTANT : left & right borders + left & right margin
    width: calc(100% - 1.125rem);
    color: rgb(255, 255, 255);
    border-radius: 0.5rem;
    display: inline-block;
    margin: 0.5rem;
    
    @media (min-width: 992px) {
        width: 46.5%;
    }
`;

export const CardHeader = styled('div')`
    border-bottom: solid thin rgb(31, 113, 145);
    padding: 0.5rem 0.5rem 0.625rem 0.5rem;
    border-top-right-radius: 0.5rem;
    border-top-left-radius: 0.5rem;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: 0.9rem;
    text-align: left;
    overflow: hidden;
`;

export const CardFooter = styled('div')`
    border-top: solid thin rgb(31, 113, 145);
    border-bottom-right-radius: 0.5rem;
    border-bottom-left-radius: 0.5rem;
    grid-template-columns: 1fr 1fr;
    display: grid;
`;

export const CardFooterItem = styled('div')`
    border-right: solid thin rgb(31, 113, 145);
    justify-content: center;
    align-items: center;
    font-size: 0.65rem;
    padding: 0.5rem 0;
    cursor: pointer;
    display: grid;

    :hover {
        background-color: rgb(0, 55, 117);
        transition: 250ms;
    }

    :first-child {
        border-bottom-left-radius: 0.5rem;
    }

    :last-child {
        border-bottom-right-radius: 0.5rem;
        border-right: none;
    }
`;
