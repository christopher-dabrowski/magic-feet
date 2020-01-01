/* eslint no-magic-numbers: 0 */
import React, { Component } from 'react';

import { FeetAnimation } from '../lib';

class App extends Component {

    constructor() {
        super();
        this.state = {
            sensorValues: [896, 568, 708, 23, 0, 5]
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

        console.log(this.state);

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
