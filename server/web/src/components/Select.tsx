import { SelectContainer, SelectRow } from '../design/components/Select.design';
import { ISelect, IState } from '../interfaces/components/Select.interface';
import React, { Component } from 'react';
import {
    FaUserPlus,
    FaUserMinus,
    FaBan,
    FaUnlockAlt,
    FaTrash
} from 'react-icons/fa';

class Select extends Component<ISelect, IState> {
    render() {
        const {
            show,
            top,
            left,
            sessionAdd,
            sessionRemove,
            blacklistAdd,
            blacklistRemove,
            clientRemove
        } = this.props;

        return show ? (
            <SelectContainer
                style={{
                    top: top,
                    left: left
                }}
            >
                <SelectRow onClick={sessionAdd}>
                    <FaUserPlus size="1rem" color="rgb(0, 255, 255)" /> Session
                    Add
                </SelectRow>
                <SelectRow onClick={sessionRemove}>
                    <FaUserMinus size="1rem" color="rgb(0, 255, 255)" /> Session
                    Remove
                </SelectRow>
                <SelectRow onClick={blacklistAdd}>
                    <FaBan size="1rem" color="rgb(138, 43, 226)" /> Blacklist
                    Add
                </SelectRow>
                <SelectRow onClick={blacklistRemove}>
                    <FaUnlockAlt size="1rem" color="rgb(138, 43, 226)" />{' '}
                    Blacklist Remove
                </SelectRow>
                <SelectRow onClick={clientRemove}>
                    <FaTrash size="1rem" color="rgb(225, 53, 57)" /> Delete
                </SelectRow>
            </SelectContainer>
        ) : null;
    }
}

export default Select;
