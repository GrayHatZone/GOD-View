import { IClient } from './Client.interface';

export interface IAllReducer {
    clients: Map<string, IClient>;
    session: Set<string>;
    sessionLoad?: any;
    clientsLoad?: any;
}
