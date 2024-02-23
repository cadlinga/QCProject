r"""
Name The Chapter Up Here
==========================
This narrative can explain the whole point of the module (the file).

You can include maths inline like this: :math:`a^2 + b^2 = c^2`

Or, if you need to display, do it like this (be sure to leave a blank line
above the .. math:: delcaration):

.. math::
    \lim_{n\to\infty} \frac{1}{n} \neq \infty


We can make use of referencing code objects like classes and methods
like this:

In this chapter we will start by explaining the :class:`Example` class
and the required arguments for the :meth:`__init__` method.


.. note::
    Add notes like this.

.. warning::
    Add warnings like this.

Insert code sample with backticks `def __init__()`.
Make text **bold**, or *italics* just like markdown.

This is a list:
    * With
    * Bullets.

This is also a list:
    1. With
    2. Numbers.
"""


class Example:
    r"""
    Class explanation.

    This can be a high level overview of what the object is.
    """

    def __init__(self, arg1: int):
        r"""
        This function initialises the class.

        """
        self.arg1 = arg1

        """
        Describe the `self.arg1` term.
        This behaviour is unique to the init method. 
        """

    def usefulMethod(self, input: int):
        r"""
        Explain the utility of this method.


        Params:
            input:
                This :class:`int` should represent something.

        Returns:
            This method returns a :class:`Vector`.

        .. This is how we comment (note the two leading fullstops)
            to continue to comment indent like this. This text will
            not appear in the docs.
            After explaining the last function in a class, add
            four consecutive dashes (like below) to draw a
            hrule between classes in the docs

        ----
        """
        return self.arg1


class Example2:
    r"""
    This is the second class
    """

    pass
