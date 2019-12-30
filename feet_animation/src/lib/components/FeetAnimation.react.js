import React, { Component } from 'react';
import PropTypes from 'prop-types';
import FeetSVG from '../../images/feet.svg';

/**
 * Custom component for displaying sensors position on the feet and their current value
 */
export default class FeetAnimation extends Component {
    render() {
        const { id, setProps } = this.props;

        return (
            <div id={id}>
                <p>I'm the best Dash component!</p>
                <FeetSVG />
            </div>
        );
    }
}

FeetAnimation.defaultProps = {};

// TODO: Add sensor values to props
FeetAnimation.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};
