import styled from 'styled-components';

export const WindowData = styled('div')`
    border: solid 0.0625rem rgb(178, 178, 178);
    background-color: rgb(5, 32, 58);
    color: rgb(255, 255, 255);
    min-height: 2.1875rem;
    min-width: 18rem;
    overflow: hidden;
    position: fixed;
    resize: both;
    height: 55vh;
    width: 40vw;

    &:after {
        cursor: nwse-resize;
        position: absolute;
        display: block;
        height: 1rem;
        width: 1rem;
        content: '';
        bottom: 0;
        right: 0;
    }
`;

export const WindowTopBar = styled('div')`
    border-bottom: solid 0.0625rem rgb(31, 93, 117);
    background-color: rgb(225, 53, 57);
    grid-template-columns: 1fr auto;
    align-items: center;
    text-align: right;
    display: grid;
`;

export const WindowTopBarTitle = styled('div')`
    text-overflow: ellipsis;
    text-align: left;
    overflow: hidden;
    padding: 0.5rem;
    cursor: grab;
`;

export const WindowTopBarAction = styled('div')`
    padding: 0.5rem;
`;

export const WindowInputGroup = styled('div')`
    padding: 0 0.75rem 1rem 0.75rem;
    grid-template-columns: auto 1fr;
    justify-content: center;
    align-items: center;
    text-align: center;
    grid-gap: 0.5rem;
    display: grid;

    :first-child {
        padding-top: 0.75rem;
    }
`;

export const WindowContent = styled('div')`
    height: calc(100% - 2.1875rem);
    overflow-x: auto;
`;

export const WindowForm = styled('form')`
    border-bottom: solid 0.0625rem rgb(31, 93, 117);
    border-right: solid 0.0625rem rgb(31, 93, 117);
    border-left: solid 0.0625rem rgb(31, 93, 117);
    margin: 0 0.75rem 0.75rem 0.75rem;
    width: calc(100% - 1.5rem);
    text-align: left;
`;

export const WindowLabel = styled('label')`
    text-transform: capitalize;
    font-size: 0.8rem;
`;

export const WindowInput = styled('input')`
    border: solid 0.0625rem rgb(31, 93, 117);
    padding: 0.45rem 0.45rem 0.45rem 0.6rem;
    background-color: rgb(5, 32, 58);
    color: rgb(255, 255, 255);
    border-radius: 5rem;
    font-size: 0.8rem;
`;

export const WindowCheckbox = styled('div')`
    border: solid 0.0625rem rgb(31, 93, 117);
    background-color: rgb(5, 32, 58);
    border-radius: 3.125rem;
    position: relative;
    width: 4.6875rem;
    height: 1.5rem;
    z-index: 0;

    &:before {
        color: rgb(255, 255, 255);
        position: absolute;
        font-weight: bold;
        right: 0.625rem;
        content: 'OFF';
        top: 0.25rem;
    }

    &:after {
        color: rgb(255, 255, 255);
        position: absolute;
        font-weight: bold;
        left: 0.625rem;
        content: 'ON';
        top: 0.25rem;
        z-index: 0;
    }

    label {
        box-shadow: 0 0.125rem 0.5rem rgb(31, 93, 117);
        background-color: rgb(255, 255, 255);
        border-radius: 3.125rem;
        position: absolute;
        transition: 250ms;
        cursor: pointer;
        width: 1.875rem;
        display: block;
        top: 0.1875rem;
        left: 0.25rem;
        height: 1rem;
        z-index: 1;
    }

    input[type="checkbox"] {
        visibility: hidden;

        &:checked + label {
            left: 2.4375rem;
        }
    }
`;

export const WindowFormSubmit = styled('div')`
    padding: 0.25rem 0.75rem 0.75rem 0.75rem;
`;

export const WindowFormButton = styled('button')`
    border: solid 0.0625rem rgb(31, 93, 117);
    background-color: rgb(5, 32, 58);
    color: rgb(255, 255, 255);
    padding: 0.5rem 0.25rem;
    border-radius: 5rem;
    width: 10rem;
`;

export const WindowFormClear = styled('button')`
    border: solid 0.0625rem rgb(31, 93, 117);
    padding: 0.45rem 0.4rem 0.55rem 0.4rem;
    background-color: rgb(5, 32, 58);
    color: rgb(255, 255, 255);
    margin-left: 0.5rem;
    border-radius: 5rem;
    width: 2rem;

    > svg {
        vertical-align: bottom;
    }
`;

export const WindowResult = styled('div')`
    font-family: 'Courier New', Courier, monospace;
    border: solid 0.0625rem rgb(31, 93, 117);
    padding: 0.75rem 0.75rem 0 0.75rem;
    margin: 0.75rem 0.75rem 0 0.75rem;
    line-height: 1.2rem;
    min-height: 7.5rem;
    font-size: 0.8rem;
    text-align: left;
    white-space: pre;
    overflow: auto;

    ::-webkit-scrollbar {
        height: 0.3rem;
        width: 0.3rem;
    }

    > div {
        border: solid 0.0625rem rgb(31, 113, 145);
        background-color: rgb(5, 32, 58);
        margin-bottom: 0.75rem;
        padding: 0.25rem;
        display: table;
        width: 100%;
    }

    table {
        border-collapse: collapse;
    }

    td,
    th {
        border: solid 0.0625rem rgb(31, 113, 145);
        background-color: rgb(5, 32, 58);
        padding: 0.25rem 0.5rem;
    }

    th {
        background-color: rgb(31, 93, 117);
    }
`;
