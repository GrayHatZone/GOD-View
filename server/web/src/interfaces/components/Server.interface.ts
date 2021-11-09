import { IClient } from '../Client.interface';
import { ISelect } from './Select.interface';

export interface IProps {
    clients: Map<string, IClient>;
    session: Set<string>;
    clientsLoad?: any;
    sessionLoad?: any;
}

export interface IState {
    clients: Map<string, IClient>;
    session: Set<string>;
    selectData: ISelect;
}
