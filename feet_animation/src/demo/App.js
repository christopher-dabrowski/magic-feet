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
        this.animateChange = this.animateChange.bind(this);
        this.generateValues = this.generateValues.bind(this);
        this.timerId = null;
    }

    setProps(newProps) {
        this.setState(newProps);
    }

    generateValues() {
        const lValue = Math.round(Math.random() * 1023);
        const rvalue = Math.round(Math.random() * 1023);
        this.setState({ sensorValues: [lValue, lValue, lValue, rvalue, rvalue, rvalue] });
    }

    animateChange(e) {
        const checked = e.target.checked;
        if (checked) {
            this.timerId = setInterval(this.generateValues, 1000);
        }
        else {
            clearInterval(this.timerId);
        }
    }

    render() {
        let style = {
            display: 'flex',
            alignItems: 'center',
            flexDirection: 'column'
        };

        return (
            <div style={style} >
                <FeetAnimation
                    setProps={this.setProps}
                    {...this.state}
                />

                <form style={{ marginTop: '20px' }}>
                    <input onChange={this.animateChange} type="checkbox" name="animate" />
                    <label>Animate values</label>
                </form>
            </div>
        )
    }
}

export default App;
