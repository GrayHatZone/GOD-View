// @ts-nocheck
import { AlertButton, AlertButtonCross } from '../design/components/Alert.design';
import React from 'react';

export const AlertTemplate = ({ style, options, message, close }) => (
    <AlertButton style={style} color={options.type} bgColor={options.type}>
        {message}
        {options.type === 'SUCCESS' && '!'}
        {options.type === 'DANGER' && '.'}
        {options.type === 'WARNING' && '.'}
        {options.type === 'INFO' && '.'}
        <AlertButtonCross onClick={close}>x</AlertButtonCross>
    </AlertButton>
);
