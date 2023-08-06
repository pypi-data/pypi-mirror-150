# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Describetable(Component):
    """A Describetable component.
An alternative to dash's DataTable. This was built specfically with pandas .describe method in mind, but can take any stringified table. Keep in mind, this was built with * a specific stylesheet in mind. The layout should be reasonable as is, but override the colors amnd whatever styles you like.

example usage:
describetable.DescribeTable(id="someId", )

Keyword arguments:

- id (string; optional):
    The id will be used in the innercontainer to insert the supplied
    html into.

- buttonText (string; optional)

- classAppendix (string; optional)

- data (a list of or a singular dash component, string or number; optional):
    Data is a stringified html output. Can be used with any
    pandas.to_html() but default *  * css is targeted specifically at
    the .describe() method."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, classAppendix=Component.UNDEFINED, buttonText=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'buttonText', 'classAppendix', 'data']
        self._type = 'Describetable'
        self._namespace = 'describetable'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'buttonText', 'classAppendix', 'data']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Describetable, self).__init__(**args)
