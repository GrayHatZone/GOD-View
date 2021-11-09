import { IAllReducer } from './interfaces/AllReducer.interface';
import { IActivity } from './interfaces/Activity.interface';
import { IClient } from './interfaces/Client.interface';
import { useDispatch, useSelector } from 'react-redux';
import { IAlert } from './interfaces/Alert.interface';
import Server from './components/Server';
import { useAlert } from 'react-alert';
import React from 'react';
import {
    sessionAll,
    sessionClose,
    sessionAdd,
    sessionRemove,
    clientAdd,
    clientRemove,
    activityUpdate
} from './redux/actions';

let sessionAllEel,
    sessionCloseEel,
    sessionAddEel,
    sessionRemoveEel,
    clientAddEel,
    clientRemoveEel,
    activityUpdateEel;

function App() {
    const dispatch = useDispatch(),
        alert = useAlert();

    document.title = useSelector<IAllReducer, string>((state) => {
        return `${state.clients.size} Connected Client${state.clients.size === 1 ? '' : 's'
            }${state.session.size > 0
                ? ` [${state.session.size} Client Session]`
                : ''
            }`;
    });

    clientAddEel = (unique_id: string, client: IClient, audio_alert: boolean) => {
        dispatch(clientAdd(unique_id, client));

        if (audio_alert) {
            const promise = new Audio('./static/alert.wav').play();

            promise !== undefined &&
                promise.catch(() => window.showAlert({
                    message: 'Failed To Play Alert Audio',
                    type: 'DANGER'
                }));

            window.showAlert({
                message: 'Client Connected',
                type: 'SUCCESS'
            });
        }
    };

    window.showAlert = (data: IAlert) =>
        // @ts-ignore
        alert.show(data.message, { type: data.type });

    sessionRemoveEel = (unique_id: string) =>
        dispatch(sessionRemove(unique_id));

    sessionAllEel = () => dispatch(sessionAll());
    sessionCloseEel = () => dispatch(sessionClose());
    sessionAddEel = (unique_id: string) => dispatch(sessionAdd(unique_id));
    clientRemoveEel = (unique_id: string) => dispatch(clientRemove(unique_id));
    activityUpdateEel = (activity: IActivity) => dispatch(activityUpdate(activity));

    window.eel.expose(sessionAllEel, 'sessionAllEel');
    window.eel.expose(sessionCloseEel, 'sessionCloseEel');
    window.eel.expose(sessionAddEel, 'sessionAddEel');
    window.eel.expose(sessionRemoveEel, 'sessionRemoveEel');
    window.eel.expose(clientAddEel, 'clientAddEel');
    window.eel.expose(clientRemoveEel, 'clientRemoveEel');
    window.eel.expose(activityUpdateEel, 'activityUpdateEel');

    return <Server />;
}

export default App;
