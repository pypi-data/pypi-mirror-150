# isinstancex (version: 1.0.0)
#
# Copyright 2022. Kim Jae-yun all rights reserved.
#
# This Library is distributed under the MIT License.
# -----------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2022 Kim Jae-yun
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import typing

__all__ = ["isinstancex"]


def isinstancex(__obj: typing.Any,
                __class_or_tuple: typing.Union[type, tuple],
                __raise_exception: type = TypeError,
                __except_message: str = "a {} is required (got type {})") \
        -> bool:
    """
    Return True or Exception whether
    an object is an instance of a class or of a subclass thereof.
    A tuple, as in isinstance(x, (A, B, ...)),
    may be given as the target to check against.
    This is equivalent to isinstance(x, A) or isinstance(x, B) or ... etc.

    :param __obj: An instance.
    :param __class_or_tuple: Class type.
    :param __raise_exception: Exception type if false.
    :param __except_message: Exception message if false.
    :return: bool
    """
    # type check
    if isinstance(__obj, __class_or_tuple):
        return True
    # get require type name
    if isinstance(__class_or_tuple, tuple):
        temp = []
        for __class in __class_or_tuple:
            temp.append(__class.__name__)
        require = ", ".join(temp)
    else:
        require = __class_or_tuple.__name__
    # get the type I got
    got_type = type(__obj).__name__
    # raise
    message = __except_message.format(require, got_type)
    raise __raise_exception(message)
