import { createStore } from 'redux';
import { allReducer } from './allReducer';

export const store = createStore(allReducer);
