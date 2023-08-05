"""
A callsign is an object identification used in logging.
Normally, an object's class name is enough.
This is the default case for the callsign methods.

However, sometimes there are multiple objects of the same class
which need to be distinguised between each other.
For example when there are multiple http servers on different ports.

To handle this case, the class should have a callsign() method
which returns the identifying string, such as the port.
"""

import html
from typing import Optional

from dls_utilpack.qualname import qualname


# ----------------------------------------------------------------------------------------
def callsign(something: object, message: Optional[str] = None) -> str:
    """
    Return the callsign of the object.  If a message is given,
    then return a full message with the callsign prepended.

    Args:
        something: object for which the callsign is desired
        message: message body if a full message is desired

    Returns:
        str: callsign or callsign with message appended

    If the something object has a callsign method, then this is used.
    Otherwise, use the object's module and type name.
    """

    callsign = None

    # The thing looks like a type?
    if isinstance(something, type):
        # Return nicely qualified name of the class.
        callsign = qualname(something)

    # The thing has a callsign method?
    elif hasattr(something, "callsign"):
        callsign = getattr(something, "callsign")
        # Let the thing's own method provide the callsign.
        if callable(callsign):
            callsign = callsign()

    if callsign is None or callsign == "":
        callsign = "%s.%s" % (type(something).__module__, type(something).__name__)
        # callsign = type(something).__name__

    if message is None or message == "":
        return callsign
    else:
        return "%s says %s" % (callsign, message)


# ----------------------------------------------------------------------------------------
def callsign_html(the_object: object, message: Optional[str] = None) -> str:
    """
    Return the callsign of the object wrapped in an html div with css class T_callsign.

    See the callsign method for argument details.

    Any html thus composed will have the callsign identifiers embedded in it.

    The idea is that the css class normally be ``display: none;`` unless debugging.

    Args:
        the_object: the object whose callsign is wanted.
        message : Extra bit of message text if desired. Defaults to None.
    """

    text = html.escape(callsign(the_object, message))
    return f"<div class='T_callsign'>html generated by python class {text}</div>"
