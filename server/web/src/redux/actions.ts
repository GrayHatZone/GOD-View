import { IActivity } from '../interfaces/Activity.interface';
import { IClient } from '../interfaces/Client.interface';

export type ClientsLoadType = { type: 'CLIENTS_LOAD'; payload: Map<string, IClient>; };
export type SessionLoadType = { type: 'SESSION_LOAD'; payload: Set<string>; };
export type SessionAllType = { type: 'SESSION_ALL'; };
export type SessionCloseType = { type: 'SESSION_CLOSE'; };
export type SessionAddType = { type: 'SESSION_ADD'; payload: string; };
export type SessionRemoveType = { type: 'SESSION_REMOVE'; payload: string; };
export type ClientAddType = { type: 'CLIENT_ADD'; payload: { unique_id: string, client: IClient; }; };
export type ClientRemoveType = { type: 'CLIENT_REMOVE'; payload: string; };
export type ActivityUpdateType = { type: 'ACTIVITY_UPDATE'; payload: IActivity; };

export const clientsLoad = (clients: Map<string, IClient>): ClientsLoadType => ({
    type: 'CLIENTS_LOAD',
    payload: clients
});

export const sessionLoad = (session: Set<string>): SessionLoadType => ({
    type: 'SESSION_LOAD',
    payload: session
});

export const sessionAll = (): SessionAllType => ({
    type: 'SESSION_ALL'
});

export const sessionClose = (): SessionCloseType => ({
    type: 'SESSION_CLOSE'
});

export const sessionAdd = (unique_id: string): SessionAddType => ({
    type: 'SESSION_ADD',
    payload: unique_id
});

export const sessionRemove = (unique_id: string): SessionRemoveType => ({
    type: 'SESSION_REMOVE',
    payload: unique_id
});

export const clientAdd = (unique_id: string, client: IClient): ClientAddType => ({
    type: 'CLIENT_ADD',
    payload: { unique_id, client }
});

export const clientRemove = (unique_id: string): ClientRemoveType => ({
    type: 'CLIENT_REMOVE',
    payload: unique_id
});

export const activityUpdate = (activity: IActivity): ActivityUpdateType => ({
    type: 'ACTIVITY_UPDATE',
    payload: activity
});
