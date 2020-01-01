import React, { Component } from 'react';
import PropTypes from 'prop-types';
import FeetSVG from '../../images/feet.svg';

/**
 * Custom component for displaying sensors position on the feet and their current value
 */
export default class FeetAnimation extends Component {
    render() {
        let { id, setProps, width, height } = this.props;

        // Set default values
        width = width || 600;
        height = height || 600;

        return (
            <div id={id}>
                <p style={{ textAlign: 'center' }}>I'm the best Dash component!</p>
                <FeetSVG width={width} height={height} />
            </div >
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
     * Size of the component
     */
    width: PropTypes.number,
    height: PropTypes.number,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};
