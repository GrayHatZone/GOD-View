import { IAllReducer } from '../interfaces/AllReducer.interface';
import { IClient } from '../interfaces/Client.interface';
import {
    ClientsLoadType,
    SessionLoadType,
    SessionAllType,
    SessionCloseType,
    SessionAddType,
    SessionRemoveType,
    ClientAddType,
    ClientRemoveType,
    ActivityUpdateType
} from './actions';

const initialState: IAllReducer = {
    clients: new Map<string, IClient>(),
    session: new Set<string>()
};

export const allReducer = (
    state: IAllReducer = initialState,
    action:
        | ClientsLoadType
        | SessionLoadType
        | SessionAllType
        | SessionCloseType
        | SessionAddType
        | SessionRemoveType
        | ClientAddType
        | ClientRemoveType
        | ActivityUpdateType
) => {
    switch (action.type) {
        case 'CLIENTS_LOAD': {
            return { ...state, clients: new Map<string, IClient>(action.payload) };
        }
        case 'SESSION_LOAD': {
            return { ...state, session: new Set<string>(action.payload) };
        }
        case 'SESSION_ALL': {
            return { ...state, session: new Set<string>(state.clients.keys()) };
        }
        case 'SESSION_CLOSE': {
            return { ...state, session: new Set<string>() };
        }
        case 'SESSION_ADD': {
            const updatedSession = new Set<string>(state.session);
            updatedSession.add(action.payload);
            return { ...state, session: updatedSession };
        }
        case 'SESSION_REMOVE': {
            const updatedSession = new Set<string>(state.session);
            updatedSession.delete(action.payload);
            return { ...state, session: updatedSession };
        }
        case 'CLIENT_ADD': {
            const updatedClients = new Map<string, IClient>(state.clients);
            updatedClients.set(action.payload.unique_id, action.payload.client);
            return { ...state, clients: updatedClients };
        }
        case 'CLIENT_REMOVE': {
            const updatedClients = new Map<string, IClient>(state.clients);
            updatedClients.delete(action.payload);
            return { ...state, clients: updatedClients };
        }
        case 'ACTIVITY_UPDATE': {
            const { unique_id, active_window, idle_time, resource_usage } = action.payload;
            const updatedClients = new Map<string, IClient>(state.clients);
            const client = updatedClients.get(unique_id);

            if (client !== undefined) {
                client.active_window = active_window;
                client.idle_time = idle_time;
                client.resource_usage = resource_usage;
                updatedClients.set(unique_id, client);
            }

            return { ...state, clients: updatedClients };
        }
        default:
            return state;
    }
};
