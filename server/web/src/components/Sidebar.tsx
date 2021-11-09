import { IProps, IState } from '../interfaces/components/Sidebar.interface';
import { FaChevronLeft, FaChevronRight } from 'react-icons/fa';
import { IStream } from '../interfaces/Stream.interface';
import React, { Component } from 'react';
import Card from './Card';
import {
    SidebarDropdown,
    SidebarDropdownButton,
    SidebarDropdownContent,
    SidebarStreamContent,
    SidebarStream,
    SidebarStreamSection,
    SidebarStreamInput,
    SidebarStreamButton,
    SidebarBlock
} from '../design/components/Sidebar.design';

class Sidebar extends Component<IProps, IState> {
    sourceInput: any = React.createRef();
    titleInput: any = React.createRef();

    constructor(props: IProps) {
        super(props);

        this.state = {
            showContent: false,
            streams: []
        };
    }

    removeStream = (toRemove: IStream) =>
        this.setState({
            streams: this.state.streams.filter(
                (stream: IStream) => (
                    !(stream.source === toRemove.source
                        && stream.title === toRemove.title)
                )
            )
        });

    addStream = () => {
        const source = this.sourceInput.current;
        const title = this.titleInput.current;
        const sourceValue = source.value.trim();
        const titleValue = title.value.trim();
        let sourcePassed = true;
        let titlePassed = true;

        if (sourceValue === '') {
            source.style.border = 'solid thin rgb(225, 53, 57)';
            sourcePassed = false;
        } else
            source.style.border = 'solid thin rgb(31, 93, 117)';

        if (titleValue === '') {
            title.style.border = 'solid thin rgb(225, 53, 57)';
            titlePassed = false;
        } else
            title.style.border = 'solid thin rgb(31, 93, 117)';

        if (sourcePassed && titlePassed)
            if (this.streamExists(sourceValue, titleValue))
                alert('Stream Already Exists!')
            else {
                this.state.streams.push({
                    source: sourceValue,
                    title: titleValue
                });
                source.value = '';
                title.value = '';
            }
    }

    streamExists = (source: string, title: string) => {
        for (const stream of this.state.streams)
            if (stream.source === source && stream.title === title)
                return true;
        return false;
    }

    updateShowContent = () =>
        this.setState({ showContent: !this.state.showContent });

    render() {
        const { showContent, streams } = this.state;

        return (
            <SidebarDropdown>
                <SidebarDropdownButton onClick={this.updateShowContent}>
                    {showContent ? (
                        <FaChevronRight size=".8rem" />
                    ) : (
                            <FaChevronLeft size=".8rem" />
                        )}
                </SidebarDropdownButton>

                <SidebarDropdownContent active={showContent}>
                    <SidebarStream>
                        <SidebarStreamInput
                            type="search"
                            placeholder="Flash video source..."
                            ref={this.sourceInput}
                        />
                        <SidebarStreamSection>
                            <SidebarStreamInput
                                type="search"
                                placeholder="Stream title..."
                                ref={this.titleInput}
                            />
                            <SidebarStreamButton
                                onClick={this.addStream}
                            >
                                Add
                            </SidebarStreamButton>
                        </SidebarStreamSection>
                    </SidebarStream>
                    {streams.length === 0 ? (
                        <SidebarBlock>No Streams Available</SidebarBlock>
                    ) : (
                            <SidebarStreamContent>
                                {streams.map((stream: IStream) => (
                                    <Card
                                        removeStream={this.removeStream}
                                        source={stream.source}
                                        title={stream.title}
                                    />
                                ))}
                            </SidebarStreamContent>
                        )}
                </SidebarDropdownContent>
            </SidebarDropdown>
        );
    }
}

export default Sidebar;
