import { IProps, IState } from '../interfaces/components/Card.interface';
import { FaRedo, FaTrash } from 'react-icons/fa';
import React, { Component } from 'react';
import svg from 'plyr/dist/plyr.svg';
import 'plyr/dist/plyr.css';
import flvjs from 'flv.js';
import Plyr from 'plyr';
import {
    CardContainer,
    CardHeader,
    CardFooter,
    CardFooterItem
} from '../design/components/Card.design';

class Card extends Component<IProps, IState> {
    videoRef: any = React.createRef();
    plyrPlayer: any;
    flvPlayer: any;

    componentDidMount() {
        const video = this.videoRef.current;
        this.createFlvPlayer();

        this.plyrPlayer = new Plyr(video, {
            iconUrl: svg,
            controls: [
                'play-large',
                'play',
                'progress',
                'mute',
                'volume',
                'fullscreen'
            ]
        });
    }

    createFlvPlayer = () => {
        const video = this.videoRef.current;
        const { source } = this.props;

        this.flvPlayer = flvjs.createPlayer({
            type: 'flv',
            isLive: true,
            url: source
        });
        this.flvPlayer.attachMediaElement(video);
        this.flvPlayer.load()
    }

    reload = () => {
        this.flvPlayer.destroy();
        this.createFlvPlayer();
    }

    remove = () => {
        const { source, title } = this.props;
        this.props.removeStream({ source, title });
    }

    render() {
        const { source, title } = this.props;

        return (
            <CardContainer>
                <CardHeader title={`${title}: ${source}`}>{title}: {source}</CardHeader>
                <video ref={this.videoRef} data-poster="./static/poster.png" />
                <CardFooter>
                    <CardFooterItem onClick={this.reload}>
                        <FaRedo size="0.8rem" />
                    </CardFooterItem>
                    <CardFooterItem onClick={this.remove}>
                        <FaTrash size="0.8rem" />
                    </CardFooterItem>
                </CardFooter>
            </CardContainer>
        )
    }
}

export default Card;
