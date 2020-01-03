# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class FeetAnimation(Component):
    """A FeetAnimation component.
Custom component for displaying sensors position on the feet and their current value

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- className (string; optional): CSS classes added to the main div
- width (number; default 350): Width of the component in px
- height (number; default 350): Height of the component in px
- sensorValues (list of numbers; default [0, 0, 0, 0, 0, 0]): Feet pressure sensor values"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, className=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, sensorValues=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'width', 'height', 'sensorValues']
        self._type = 'FeetAnimation'
        self._namespace = 'feet_animation'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'width', 'height', 'sensorValues']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(FeetAnimation, self).__init__(**args)
