import { transitions, positions, Provider as AlertProvider } from 'react-alert';
import { GlobalStyle } from './design/GlobalStyle';
import { AlertTemplate } from './components/Alert';
import { Provider } from 'react-redux';
import { store } from './redux/store';
import ReactDOM from 'react-dom';
import React from 'react';
import App from './App';

const alertOptions = {
    // CONSTANT : alert parameters
    position: positions.TOP_LEFT,
    transition: transitions.FADE,
    timeout: 3000
};

declare global {
    interface Window {
        showAlert: any;
        eel: any;
    }
}

window.eel.set_host(`ws://${window.location.host}`);
window.oncontextmenu = () => false;

window.addEventListener('load', () => {
    window.addEventListener('error', (event: any) =>
        console.log(`Window Error: ${event.message}`));

    window.eel._websocket.addEventListener('open', () =>
        console.log('Host Websocket Connected!'));

    window.eel._websocket.addEventListener('error', (event: any) => {
        console.log(`Websocket Error: ${event.message}`);
        window.alert('Host Connection Error. Closing!');
        window.close();
    });

    window.eel._websocket.addEventListener('close', () => {
        window.alert('Host Disconnected. Closing!');
        window.close();
    });
});

ReactDOM.render(
    <React.StrictMode>
        <Provider store={store}>
            <GlobalStyle />
            <AlertProvider template={AlertTemplate} {...alertOptions}>
                <App />
            </AlertProvider>
        </Provider>
    </React.StrictMode>,
    document.getElementById('root')
);
