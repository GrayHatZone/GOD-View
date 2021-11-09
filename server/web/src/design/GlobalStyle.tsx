import { createGlobalStyle } from 'styled-components';

// NOTE : rem unit is used instead of px. But
// the UI is still dependant on px units, mostly
// because of some javascript calculations
export const GlobalStyle = createGlobalStyle`
    ::-webkit-scrollbar {
        height: 0.2rem;
        width: 0.4rem;
    }

    ::-webkit-scrollbar-track {
        background-color: rgb(5, 32, 58);
    }

    ::-webkit-scrollbar-thumb {
        background-color: rgb(31, 113, 145);
    }

    ::placeholder {
        text-transform: capitalize;
        color: rgb(204, 204, 204);
        opacity: 1;
    }

    * {
        box-sizing: border-box;
        outline: none;
    }

    body {
        font-family: Arial, Helvetica, sans-serif;
        background-color: rgb(5, 32, 58);
        color: rgb(255, 255, 255);
        font-size: 0.7rem;
        font-weight: 100;
        margin: 0;
    }

    button, svg {
        cursor: pointer;
    }

    button {
        transition: 150ms;

        :active {
            transform: translateY(0.125rem);
            transition: 150ms;
        }
    }
`;
