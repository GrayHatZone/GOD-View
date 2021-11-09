import { IProps, IState } from '../interfaces/components/Footer.interface';
import React, { Component, Fragment } from 'react';
import Window from './Window';
import {
    FooterDropdown,
    FooterDropdownToggle,
    FooterDropdownContent,
    FooterNameSpaceButton,
    FooterDropdownButton,
    FooterWindowManager,
    FooterWindowButton,
    FooterWindowClear,
    FooterBlock,
    FooterMenu,
    FooterParagraph
} from '../design/components/Footer.design';
import {
    FaChevronDown,
    FaChevronUp,
    FaLink,
    FaListUl,
    FaPlus,
    FaMinus,
    FaSyncAlt,
    FaTrash
} from 'react-icons/fa';

class Footer extends Component<IProps, IState> {
    winManager: any = React.createRef();
    column = 0;
    row = 0;

    state = {
        showHelp: false,
        address: '',
        windows: [],
        help: {}
    };

    componentDidMount() {
        window.eel.host_eel()((address: string) =>
            window.eel.help_eel()((help: object) =>
                this.setState({ address: address, help: help })
            )
        );
    }

    componentDidUpdate() {
        this.column = 0;
        this.row = 0;
    }

    createWindow = (
        requestType: string,
        argsArray: any,
        windowData: string
    ) => {
        const newWindow = [
            requestType,
            argsArray,
            React.createRef(),
            true,
            windowData ? [windowData] : null
        ];

        const windows: any = [...this.state.windows];
        let undefinedExists = false;

        for (let i = 0; i < windows.length; i++)
            if (windows[i] === undefined) {
                windows[i] = newWindow;
                undefinedExists = true;
                break;
            }

        if (!undefinedExists)
            windows.push(newWindow);

        this.setState({ windows: windows });
    };

    removeWindow = (index: number) => (event: any) => {
        const windows = [...this.state.windows];
        delete windows[index];

        windows.filter(Boolean).length === 0
            ? this.clearWindows()
            : this.setState({ windows });

        event.stopPropagation();
    };

    clearWindows = () => {
        this.winManager.current.style.zIndex = 1;
        this.setState({ windows: [] });
    };

    windowPosition = () => {
        if (this.column === 5) {
            this.column = 0;
            this.row++;
        }

        this.column++;

        return {
            // CONSTANT : px for every row and column (left & top)
            x: this.column * 25 + this.row * 25,
            y: this.column * 25 + 40 + this.row
        };
    };

    windowHighlight = (ref: any) => {
        const newZIndex = Number(this.winManager.current.style.zIndex) + 1
        this.winManager.current.style.zIndex = newZIndex;
        ref.current.window.current.style.zIndex = newZIndex;
    };

    windowToggle = (show: boolean, window: any) => {
        const windows: any[] = [...this.state.windows];
        const index: number = windows.indexOf(window);
        windows[index][3] = show;

        this.windowHighlight(window[2]);
        this.setState({ windows });

        if (!show) window[2].current.window.current.style.display = 'none';
        else window[2].current.window.current.style.display = 'block';
    };

    windowCenter = (window: any) => (event: any) => {
        this.windowToggle(true, window);
        // CONSTANT : based on default styles from the CSS of the window
        // (height & width) & the values of each column & row (left & top)
        window[2].current.window.current.style.height = '55vh';
        window[2].current.window.current.style.width = '40vw';
        window[2].current.window.current.style.left = '25px';
        window[2].current.window.current.style.top = '65px';

        event.stopPropagation();
    };

    createWindowEvent = (requestType: string, argsArray: any) => () => {
        if (argsArray.length > 0) this.createWindow(requestType, argsArray, '');
        else
            window.eel.execute_eel({
                message: requestType.toLowerCase()
            })((response: any) => {
                response !== null
                    ? response.alert
                        ? window.showAlert({
                            message: response.message,
                            type: response.type
                        })
                        : this.createWindow(requestType, argsArray, response)
                    : window.showAlert({
                        message: `${requestType} Request Executed`,
                        type: 'INFO'
                    });
            });
    };

    windowHighlightEvent = (ref: any) => () => this.windowHighlight(ref);

    windowToggleEvent = (show: boolean, window: any) => (event: any) => {
        this.windowToggle(show, window);
        event.stopPropagation();
    };

    launchWebVersion = (event: any) => {
        if (event.ctrlKey) {
            window.open(window.location.href, '_blank');
            window.showAlert({
                message: 'Web Version Launched',
                type: 'INFO'
            });
        } else if (event.altKey) {
            const request = new XMLHttpRequest();
            request.open('GET', '/logout');
            request.send();
            window.location.reload();
        }
    };

    showHelpToggle = () => this.setState({ showHelp: !this.state.showHelp });

    render() {
        const { showHelp, address, windows, help } = this.state;

        return (
            <Fragment>
                <FooterDropdown>
                    <FooterDropdownToggle onClick={this.showHelpToggle}>
                        {showHelp ? (
                            <FaChevronDown size="0.8rem" />
                        ) : (
                                <FaChevronUp size="0.8rem" />
                            )}
                    </FooterDropdownToggle>

                    <FooterDropdownContent active={showHelp}>
                        {Object.entries(help).map(
                            ([namespace, requests]: any, index: number) => (
                                <Fragment key={index}>
                                    <FooterNameSpaceButton
                                        title={`${namespace} Namespace`}
                                    >
                                        {namespace}
                                    </FooterNameSpaceButton>{' '}
                                    {requests.map(
                                        (
                                            [
                                                available,
                                                requestType,
                                                argsString,
                                                argsArray
                                            ]: any[],
                                            i: number
                                        ) => (
                                            <FooterDropdownButton
                                                key={i}
                                                title={`Available: ${available}${argsString
                                                    ? ` ${argsString}`
                                                    : ''
                                                    }`}
                                                onClick={this.createWindowEvent(
                                                    requestType,
                                                    argsArray
                                                )}
                                            >
                                                {available === 'Session' ? (
                                                    <FaLink size="0.6rem" />
                                                ) : null}{' '}
                                                {argsString ? (
                                                    <FaListUl size="0.65rem" />
                                                ) : null}{' '}
                                                {requestType}
                                            </FooterDropdownButton>
                                        )
                                    )}
                                </Fragment>
                            )
                        )}
                    </FooterDropdownContent>
                </FooterDropdown>

                <FooterWindowManager>
                    <div ref={this.winManager} style={{ zIndex: 1 }}>
                        {windows.length > 0 ? (
                            <Fragment>
                                <FooterWindowClear
                                    title='Remove All Windows'
                                    onClick={this.clearWindows}
                                >
                                    Clear Windows
                                </FooterWindowClear>
                                {windows.map((window: any, index: number) => (
                                    <Fragment key={index}>
                                        {window !== undefined ? (
                                            <Fragment>
                                                <Window
                                                    ref={window[2]}
                                                    requestType={window[0]}
                                                    requestArgs={window[1]}
                                                    pos={this.windowPosition()}
                                                    data={window[4]}
                                                    hightlight={this.windowHighlightEvent(
                                                        window[2]
                                                    )}
                                                    toggle={this.windowToggleEvent(
                                                        false,
                                                        window
                                                    )}
                                                    destroy={this.removeWindow(
                                                        index
                                                    )}
                                                />
                                                <FooterWindowButton
                                                    onClick={this.windowToggleEvent(
                                                        window[3]
                                                            ? false
                                                            : true,
                                                        window
                                                    )}
                                                >
                                                    {window[0]}{' '}
                                                    {window[3] ? (
                                                        <FaMinus
                                                            size="0.7rem"
                                                            title={`Hide ${window[0]} Window`}
                                                            onClick={this.windowToggleEvent(
                                                                false,
                                                                window
                                                            )}
                                                        />
                                                    ) : (
                                                            <FaPlus
                                                                size="0.7rem"
                                                                title={`Show ${window[0]} Window`}
                                                                onClick={this.windowToggleEvent(
                                                                    true,
                                                                    window
                                                                )}
                                                            />
                                                        )}{' '}
                                                    <FaSyncAlt
                                                        size="0.7rem"
                                                        title={`Reset ${window[0]} Window Position`}
                                                        onClick={this.windowCenter(
                                                            window
                                                        )}
                                                    />{' '}
                                                    <FaTrash
                                                        size="0.7rem"
                                                        title={`Remove ${window[0]} Window`}
                                                        onClick={this.removeWindow(
                                                            index
                                                        )}
                                                    />
                                                </FooterWindowButton>
                                            </Fragment>
                                        ) : null}
                                    </Fragment>
                                ))}
                            </Fragment>
                        ) : (
                                <FooterBlock>
                                    No Active Windows To Manage
                                </FooterBlock>
                            )}
                    </div>
                </FooterWindowManager>

                <FooterMenu>
                    <FooterParagraph
                        title={`Listening Address: ${address}`}
                        onClick={this.launchWebVersion}
                    >
                        {`Listening Address: ${address}`}
                    </FooterParagraph>
                </FooterMenu>
            </Fragment>
        );
    }
}

export default Footer;
