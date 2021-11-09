import { IStream } from '../Stream.interface';

export interface IProps {}

export interface IState {
    showContent: boolean;
    streams: IStream[];
}
