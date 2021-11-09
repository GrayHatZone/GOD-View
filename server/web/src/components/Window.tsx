import { IProps, IState } from '../interfaces/components/Window.interface';
import React, { Component, Fragment } from 'react';
import {
    WindowData,
    WindowTopBar,
    WindowTopBarTitle,
    WindowTopBarAction,
    WindowContent,
    WindowResult,
    WindowForm,
    WindowInputGroup,
    WindowLabel,
    WindowInput,
    WindowCheckbox,
    WindowFormSubmit,
    WindowFormButton,
    WindowFormClear
} from '../design/components/Window.design';
import {
    FaMinusSquare,
    FaWindowMaximize,
    FaWindowMinimize,
    FaWindowClose,
    FaRedo
} from 'react-icons/fa';

class Window extends Component<IProps, IState> {
    windowResult: any = React.createRef();
    windowTitle: any = React.createRef();
    windowForm: any = React.createRef();
    window: any = React.createRef();

    constructor(props: IProps) {
        super(props);
        this.state = {
            result: props.data || [],
            fullscreen: false,
            dragging: false,
            pos: props.pos,
            rel: null
        };
    }

    componentDidMount() {
        document.addEventListener('fullscreenchange', this.fullscreenEvent);

        if (this.windowForm.current === null)
            // CONSTANT : window height minus the margin & borders
            this.windowResult.current.style.height = 'calc(100% - 1.625rem)';
        else
            // CONSTANT : window height minus the form height, margin & borders
            // CONSTANT : Rem unit dependant & px scrollHeight
            this.windowResult.current.style.height = `
                calc(100% - 1.625rem - ${this.windowForm.current.scrollHeight / 16}rem)
            `;
    }

    componentDidUpdate(_: IProps, state: IState) {
        const { dragging } = this.state;

        if (dragging && !state.dragging) {
            document.addEventListener('mousemove', this.windowMove);
            document.addEventListener('mouseup', this.windowDrop);
        } else if (!dragging && state.dragging) {
            document.removeEventListener('mousemove', this.windowMove);
            document.removeEventListener('mouseup', this.windowDrop);
        }
    }

    componentWillUnmount() {
        document.removeEventListener('fullscreenchange', this.fullscreenEvent);
    }

    windowMove = (event: any) => {
        const { dragging, rel } = this.state;

        if (!dragging) return;

        this.setState({
            pos: {
                x: event.pageX - rel.x,
                y: event.pageY - rel.y
            }
        });
    };

    windowGrab = (event: any) => {
        if (event.button !== 0) return;

        this.windowTitle.current.style.cursor = 'grabbing';
        this.props.hightlight();

        this.setState({
            dragging: true,
            rel: {
                x: event.pageX - this.window.current.offsetLeft,
                y: event.pageY - this.window.current.offsetTop
            }
        });
    };

    windowDrop = () => {
        this.windowTitle.current.style.cursor = 'grab';
        this.setState({ dragging: false });
    };

    clearResult = (event: any) => {
        this.setState({
            result: this.state.result.filter(
                (item: string) => item === 'Request Sent... Awaiting Response')
        });
        event.preventDefault();
    };

    executeRequest = (event: any) => {
        const { requestType, requestArgs } = this.props;
        let windowResult: any = {
            message: requestType.toLowerCase()
        };
        let requiredFields = true;

        for (let i = 0; i < requestArgs.length; i++)
            if (requestArgs[i][2])
                if (
                    requestArgs[i][1] &&
                    !event.target[requestArgs[i][0]].value
                ) {
                    event.target[requestArgs[i][0]].style.border =
                        'solid 0.0625rem rgb(225, 53, 57)';
                    requiredFields = false;
                } else {
                    event.target[requestArgs[i][0]].style.border =
                        'solid 0.0625rem rgb(31, 93, 117)';
                    windowResult[requestArgs[i][0]] =
                        event.target[requestArgs[i][0]].value;
                }
            else
                windowResult[requestArgs[i][0]] =
                    event.target[requestArgs[i][0]].checked;

        if (requiredFields)
            this.setState({
                result: ['Request Sent... Awaiting Response', ...this.state.result]
            }, () =>
                window.eel.execute_eel(windowResult)((response: string) => {
                    const result = this.state.result.reverse()
                    let awaitResponseMessage = true;

                    this.setState({
                        result: result.map(
                            (item: string) => {
                                if (item === 'Request Sent... Awaiting Response')
                                    if (awaitResponseMessage) {
                                        awaitResponseMessage = false;
                                        return response;
                                    } else
                                        return item;
                                else
                                    return item;
                            }
                        ).reverse()
                    })
                })
            )

        event.preventDefault();
    };

    updateCheckbox = (event: any) => {
        if (event.target.previousSibling.hasAttribute('checked'))
            event.target.previousSibling.removeAttribute('checked');
        else event.target.previousSibling.setAttribute('checked', '');
    };

    fullscreenEvent = () => {
        if (document.fullscreenElement) this.setState({ fullscreen: true });
        else this.setState({ fullscreen: false });
    };

    enterFullscreen = () => this.window.current.requestFullscreen();

    exitFullscreen = () => document.exitFullscreen();

    render() {
        const { pos, result, fullscreen } = this.state;
        const {
            requestType,
            requestArgs,
            hightlight,
            toggle,
            destroy
        } = this.props;

        return (
            <WindowData
                ref={this.window}
                style={{
                    left: `${pos.x}px`,
                    top: `${pos.y}px`
                }}
            >
                <WindowTopBar>
                    <WindowTopBarTitle
                        title={`${requestType} Request / Response Window`}
                        onMouseDown={this.windowGrab}
                        ref={this.windowTitle}
                    >
                        {requestType}
                    </WindowTopBarTitle>
                    <WindowTopBarAction>
                        {fullscreen ? (
                            <FaWindowMinimize
                                onClick={this.exitFullscreen}
                                size="1rem"
                            />
                        ) : (
                                <FaWindowMaximize
                                    onClick={this.enterFullscreen}
                                    size="1rem"
                                />
                            )}{' '}
                        <FaMinusSquare onClick={toggle} size="1rem" />{' '}
                        <FaWindowClose onClick={destroy} size="1rem" />
                    </WindowTopBarAction>
                </WindowTopBar>
                <WindowContent onMouseDown={hightlight}>
                    <WindowResult ref={this.windowResult}>
                        {result.length > 0 ? (
                            result.map((response: any, index: number) => (
                                <Fragment key={index}>
                                    {response ? (
                                        response.html ? (
                                            <div
                                                dangerouslySetInnerHTML={{
                                                    __html: response.message
                                                        ? response.message
                                                        : 'Empty Response'
                                                }}
                                            ></div>
                                        ) : (
                                                <div>{response}</div>
                                            )
                                    ) : (
                                            <div>Empty Response</div>
                                        )}
                                </Fragment>
                            ))
                        ) : (
                                <div>No Responses Present</div>
                            )}
                    </WindowResult>
                    {requestArgs.length > 0 ? (
                        <WindowForm
                            onSubmit={this.executeRequest}
                            ref={this.windowForm}
                        >
                            {requestArgs.map((
                                [name, required, response]: [string, boolean, boolean],
                                index: number
                            ) =>
                                response ? (
                                    <WindowInputGroup key={index}>
                                        <WindowLabel>
                                            {required
                                                ? 'Required'
                                                : 'Optional'}
                                        </WindowLabel>

                                        <WindowInput
                                            type="search"
                                            name={name}
                                            placeholder={name}
                                        />
                                    </WindowInputGroup>
                                ) : (
                                        <WindowInputGroup key={index}>
                                            <WindowLabel>{name}</WindowLabel>
                                            <WindowCheckbox>
                                                <input
                                                    type="checkbox"
                                                    name={name}
                                                />
                                                <label
                                                    onClick={
                                                        this.updateCheckbox
                                                    }
                                                ></label>
                                            </WindowCheckbox>
                                        </WindowInputGroup>
                                    )
                            )}
                            <WindowFormSubmit>
                                <WindowFormButton>
                                    Execute Request
                                </WindowFormButton>
                                <WindowFormClear onClick={this.clearResult}>
                                    <FaRedo />
                                </WindowFormClear>
                            </WindowFormSubmit>
                        </WindowForm>
                    ) : null}
                </WindowContent>
            </WindowData>
        );
    }
}

export default Window;
