import React, { Component, useEffect } from 'react';
import PropTypes from 'prop-types';
import FeetSVG from '../../images/feet.svg';
import * as d3 from "d3";
import { mean } from 'ramda';

/**
 * Custom component for displaying sensors position on the feet and their current value
 */
const FeetAnimation = ({ id, className, setProps, width, height, sensorValues }) => {
    // Format image (make stroke change on average sensor value)
    useEffect(() => {
        const svg = d3.select('#feet-image');
        const wholeImage = svg.select('g');
        const rightFoot = wholeImage.select('path');
        const leftFoot = wholeImage.select('g');

        const leftValues = sensorValues.slice(0, 3);
        const rightValues = sensorValues.slice(3);

        const mapValuesToStrokeWidth = (values) => {
            const MAX_VALUE = 1023;
            const a = 0.4;
            const b = 1.5;

            const avg = mean(values);
            return avg / MAX_VALUE * (b - a) + a;
        }

        const [leftWidth, rightWidth] = [leftValues, rightValues].map(mapValuesToStrokeWidth);

        leftFoot.attr('stroke-width', leftWidth);
        rightFoot.attr('stroke-width', rightWidth);
    }, [...sensorValues]);

    // Display sensor values
    useEffect(() => {
        const svg = d3.select('#feet-image');
        const r = 7;
        // TODO: Interpolate color value
        const color = '#80bd9e';


        const positions = [
            { x: 32, y: 33 },
            { x: 10, y: 45 },
            { x: 25, y: 90 },

            { x: 68, y: 33 },
            { x: 90, y: 45 },
            { x: 74, y: 90 },
        ];

        for (const [i, position] of positions.entries()) {
            const { x, y } = position;
            const value = sensorValues[i];

            const g = svg.append('g').classed('sensor-value', true);

            g.append('circle')
                .attr('cx', `${x}%`)
                .attr('cy', `${y}%`)
                .attr('r', `${r}%`)
                .style('fill', color);

            const transleteY = r * 0.29;
            const fontSize = r * 1;
            g.append('text')
                .attr('x', `${x}%`)
                .attr('y', `${y}%`)
                .attr('transform', `translate(0 ${transleteY})`)
                .attr('text-anchor', 'middle')
                .style('font-size', `${fontSize}px`)
                .text(value);
        }

        // Cleanup
        return () => {
            const svg = d3.select('#feet-image');
            svg.selectAll('.sensor-value').remove();
        }
    }, [...sensorValues]);

    return (
        <div id={id} className={className}>
            {/* Image container */}
            <div style={{ width: width, height: height }}>
                <FeetSVG id="feet-image" width={width} height={height} />
            </div>
        </div >
    )
}

FeetAnimation.defaultProps = {
    width: 350,
    height: 350,
    sensorValues: [0, 0, 0, 0, 0, 0]
};

FeetAnimation.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * CSS classes added to the main div
     */
    className: PropTypes.string,

    /**
     * Width of the component in px
     */
    width: PropTypes.number,

    /**
    * Height of the component in px
    */
    height: PropTypes.number,

    /**
     * Feet pressure sensor values
     */
    sensorValues: PropTypes.arrayOf(PropTypes.number),


    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default FeetAnimation;