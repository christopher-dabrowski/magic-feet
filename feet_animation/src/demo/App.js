/* eslint no-magic-numbers: 0 */
import React, { Component } from 'react';

import { FeetAnimation } from '../lib';

class App extends Component {

    constructor() {
        super();
        this.state = {
            value: ''
        };
        this.setProps = this.setProps.bind(this);
    }

    setProps(newProps) {
        this.setState(newProps);
    }

    render() {
        let style = {
            display: 'flex',
            justifyContent: 'center'
        };

        return (
            <div style={style} >
                <FeetAnimation
                    setProps={this.setProps}
                    {...this.state}
                />
            </div>
        )
    }
}

export default App;
