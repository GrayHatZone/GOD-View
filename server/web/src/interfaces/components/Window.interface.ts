interface IPos {
    x: number;
    y: number;
}

export interface IProps {
    requestType: string;
    requestArgs: any;
    hightlight: any;
    data?: string[];
    destroy: any;
    toggle: any;
    pos: IPos;
}

export interface IState {
    fullscreen: boolean;
    dragging: boolean;
    result: string[];
    pos: IPos;
    rel: any;
}
