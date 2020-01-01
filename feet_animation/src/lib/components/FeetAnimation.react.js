import React, { Component, useEffect } from 'react';
import PropTypes from 'prop-types';
import FeetSVG from '../../images/feet.svg';
import * as d3 from "d3";

/**
 * Custom component for displaying sensors position on the feet and their current value
 */
const FeetAnimation = ({ id, setProps, width, height }) => {

    // Format image (make stroke change on average sensor value)
    useEffect(() => {
        const svg = d3.select('#feet-image');
        const wholeImage = svg.select('g');

        wholeImage.attr('stroke', 'blue');
        wholeImage.attr('stroke-width', 1);

        const rightFoot = wholeImage.select('path');
        const leftFoot = wholeImage.select('g');

        rightFoot.attr('stroke', 'red');
        leftFoot.attr('stroke-width', 2);


        return () => { // Here we can add cleanup
            console.log('nice cleanup')
        };
    });

    // Display sensor values
    useEffect(() => {
        const svg = d3.select('#feet-image');

        const r = '5%';
        const x = '20%';
        const y = '35%';
        const color = 'purple';

        const g = svg.append('g');

        g.append('circle')
            .attr('cx', x)
            .attr('cy', y)
            .attr('r', r)
            .style('fill', color);

    });

    return (
        <div id={id}>
            <p style={{ textAlign: 'center' }}>I'm the best Dash component!</p>

            {/* Image container */}
            <div width={width} height={height}>
                <FeetSVG id="feet-image" width={width} height={height} />
            </div>
        </div >
    )
}

FeetAnimation.defaultProps = {
    width: 350,
    height: 350
};

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

export default FeetAnimation;