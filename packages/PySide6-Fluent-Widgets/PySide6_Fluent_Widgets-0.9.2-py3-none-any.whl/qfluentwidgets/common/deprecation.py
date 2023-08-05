import contextlib
import functools
import inspect
import itertools
import re
import sys
import warnings


class FluentDeprecationWarning(UserWarning):
    """
    A class for issuing deprecation warnings for PyQt-Fluent-Widgets users.

    In light of the fact that Python builtin DeprecationWarnings are ignored
    by default as of Python 2.7 (see link below), this class was put in to
    allow for the signaling of deprecation, but via UserWarnings which are not
    ignored by default.

    https://docs.python.org/dev/whatsnew/2.7.html#the-future-for-python-2-x
    """



def _generate_deprecation_warning(
        since, message='', name='', alternative='', pending=False, obj_type='',
        addendum='', removal=''):
    if pending:
        if removal:
            raise ValueError(
                "A pending deprecation cannot have a scheduled removal")
    else:
        if removal:
            removal = "in {}".format(removal)
        else:
            removal = {"2.2": "in 3.1", "3.0": "in 3.2", "3.1": "in 3.3"}.get(
                since, "two minor releases later")
    if not message:
        message = (
            "\nThe `%(name)s` %(obj_type)s"
            + (" will be deprecated in a future version"
               if pending else
               (" was deprecated in PyQt-Fluent-Widgets %(since)s"
                + (" and will be removed %(removal)s"
                   if removal else
                   "")))
            + "."
            + (" Use `%(alternative)s` instead." if alternative else "")
            + (" %(addendum)s" if addendum else ""))
    warning_cls = (PendingDeprecationWarning if pending
                   else FluentDeprecationWarning)
    return warning_cls(message % dict(
        func=name, name=name, obj_type=obj_type, since=since, removal=removal,
        alternative=alternative, addendum=addendum))


def _warn_external(message, category=None):
    """
    `warnings.warn` wrapper that sets *stacklevel* to "outside PyQt-Fluent-Widgets".

    The original emitter of the warning can be obtained by patching this
    function back to `warnings.warn`, i.e. ``_warn_external =
    warnings.warn`` (or ``functools.partial(warnings.warn, stacklevel=2)``,
    etc.).
    """
    frame = sys._getframe()
    for stacklevel in itertools.count(1):  # lgtm[py/unused-loop-variable]
        if frame is None:
            # when called in embedded context may hit frame is None
            break
        if not re.match(r"\A(qfluentwidgets)(\Z|\.(?!tests\.))",
                        # Work around sphinx-gallery not setting __name__.
                        frame.f_globals.get("__name__", "")):
            break
        frame = frame.f_back
    warnings.warn(message, category, stacklevel)


def warn_deprecated(since, message='', name='', alternative='', pending=False, obj_type='', addendum='', removal=''):
    """
    Display a standardized deprecation.

    Parameters
    ----------
    since : str
        The release at which this API became deprecated.

    message : str, optional
        Override the default deprecation message.  The ``%(since)s``,
        ``%(name)s``, ``%(alternative)s``, ``%(obj_type)s``, ``%(addendum)s``,
        and ``%(removal)s`` format specifiers will be replaced by the values
        of the respective arguments passed to this function.

    name : str, optional
        The name of the deprecated object.

    alternative : str, optional
        An alternative API that the user may use in place of the deprecated
        API.  The deprecation warning will tell the user about this alternative
        if provided.

    pending : bool, optional
        If True, uses a PendingDeprecationWarning instead of a
        DeprecationWarning.  Cannot be used together with *removal*.

    obj_type : str, optional
        The object type being deprecated.

    addendum : str, optional
        Additional text appended directly to the final message.

    removal : str, optional
        The expected removal version.  With the default (an empty string), a
        removal version is automatically computed from *since*.  Set to other
        Falsy values to not schedule a removal date.  Cannot be used together
        with *pending*.

    Examples
    --------
    Basic example::

        # To warn of the deprecation of "qfluentwidgets.name_of_module"
        warn_deprecated('1.4.0', name='qfluentwidgets.name_of_module',
                        obj_type='module')
    """
    warning = _generate_deprecation_warning(
        since, message, name, alternative, pending, obj_type, addendum,
        removal=removal)

    _warn_external(warning, category=FluentDeprecationWarning)


def deprecated(since, message='', name='', alternative='', pending=False,
               obj_type=None, addendum='', removal=''):
    """
    Decorator to mark a function, a class, or a property as deprecated.

    When deprecating a classmethod, a staticmethod, or a property, the
    ``@deprecated`` decorator should go *under* ``@classmethod`` and
    ``@staticmethod`` (i.e., `deprecated` should directly decorate the
    underlying callable), but *over* ``@property``.

    Parameters
    ----------
    since : str
        The release at which this API became deprecated.

    message : str, optional
        Override the default deprecation message.  The ``%(since)s``,
        ``%(name)s``, ``%(alternative)s``, ``%(obj_type)s``, ``%(addendum)s``,
        and ``%(removal)s`` format specifiers will be replaced by the values
        of the respective arguments passed to this function.

    name : str, optional
        The name used in the deprecation message; if not provided, the name
        is automatically determined from the deprecated object.

    alternative : str, optional
        An alternative API that the user may use in place of the deprecated
        API.  The deprecation warning will tell the user about this alternative
        if provided.

    pending : bool, optional
        If True, uses a PendingDeprecationWarning instead of a
        DeprecationWarning.  Cannot be used together with *removal*.

    obj_type : str, optional
        The object type being deprecated; by default, 'class' if decorating
        a class, 'attribute' if decorating a property, 'function' otherwise.

    addendum : str, optional
        Additional text appended directly to the final message.

    removal : str, optional
        The expected removal version.  With the default (an empty string), a
        removal version is automatically computed from *since*.  Set to other
        Falsy values to not schedule a removal date.  Cannot be used together
        with *pending*.

    Examples
    --------
    Basic example::

        @deprecated('1.4.0')
        def the_function_to_deprecate():
            pass
    """

    def deprecate(obj, message=message, name=name, alternative=alternative,
                  pending=pending, obj_type=obj_type, addendum=addendum):

        if isinstance(obj, type):
            if obj_type is None:
                obj_type = "class"
            func = obj.__init__
            name = name or obj.__name__
            old_doc = obj.__doc__

            def finalize(wrapper, new_doc):
                try:
                    obj.__doc__ = new_doc
                except AttributeError:  # Can't set on some extension objects.
                    pass
                obj.__init__ = functools.wraps(obj.__init__)(wrapper)
                return obj

        elif isinstance(obj, property):
            obj_type = "attribute"
            func = None
            name = name or obj.fget.__name__
            old_doc = obj.__doc__

            class _deprecated_property(property):
                def __get__(self, instance, owner):
                    if instance is not None:
                        _warn_external(warning)
                    return super().__get__(instance, owner)

                def __set__(self, instance, value):
                    if instance is not None:
                        _warn_external(warning)
                    return super().__set__(instance, value)

                def __delete__(self, instance):
                    if instance is not None:
                        _warn_external(warning)
                    return super().__delete__(instance)

            def finalize(_, new_doc):
                return _deprecated_property(
                    fget=obj.fget, fset=obj.fset, fdel=obj.fdel, doc=new_doc)

        else:
            if obj_type is None:
                obj_type = "function"
            func = obj
            name = name or obj.__name__
            old_doc = func.__doc__

            def finalize(wrapper, new_doc):
                wrapper = functools.wraps(func)(wrapper)
                wrapper.__doc__ = new_doc
                return wrapper

        warning = _generate_deprecation_warning(
            since, message, name, alternative, pending, obj_type, addendum,
            removal=removal)

        def wrapper(*args, **kwargs):
            _warn_external(warning)
            return func(*args, **kwargs)

        old_doc = inspect.cleandoc(old_doc or '').strip('\n')

        notes_header = '\nNotes\n-----'
        new_doc = (f"[*Deprecated*] {old_doc}\n"
                   f"{notes_header if notes_header not in old_doc else ''}\n"
                   f".. deprecated:: {since}\n"
                   f"   {message.strip()}")

        if not old_doc:
            # This is to prevent a spurious 'unexpected unindent' warning from
            # docutils when the original docstring was blank.
            new_doc += r'\ '

        return finalize(wrapper, new_doc)

    return deprecate


class _deprecate_privatize_attribute:
    """
    Helper to deprecate public access to an attribute.

    This helper should only be used at class scope, as follows::

        class Foo:
            attr = _deprecate_privatize_attribute(*args, **kwargs)

    where *all* parameters are forwarded to `deprecated`.  This form makes
    ``attr`` a property which forwards access to ``self._attr`` (same name but
    with a leading underscore), with a deprecation warning.  Note that the
    attribute name is derived from *the name this helper is assigned to*.
    """

    def __init__(self, *args, **kwargs):
        self.deprecator = deprecated(*args, **kwargs)

    def __set_name__(self, owner, name):
        setattr(owner, name, self.deprecator(
            property(lambda self: getattr(self, f"_{name}")), name=name))


def _rename_parameter(since, old, new, func=None):
    """
    Decorator indicating that parameter *old* of *func* is renamed to *new*.

    The actual implementation of *func* should use *new*, not *old*.  If *old*
    is passed to *func*, a DeprecationWarning is emitted, and its value is
    used, even if *new* is also passed by keyword (this is to simplify pyplot
    wrapper functions, which always pass *new* explicitly to the Axes method).
    If *new* is also passed but positionally, a TypeError will be raised by the
    underlying function during argument binding.

    Examples
    --------
    ::

        @_rename_parameter("3.1", "bad_name", "good_name")
        def func(good_name): ...
    """

    if func is None:
        return functools.partial(_rename_parameter, since, old, new)

    signature = inspect.signature(func)
    assert old not in signature.parameters, (
        f"PyQt-Fluent-Widgets internal error: {old!r} cannot be a parameter for "
        f"{func.__name__}()")
    assert new in signature.parameters, (
        f"PyQt-Fluent-Widgets internal error: {new!r} must be a parameter for "
        f"{func.__name__}()")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if old in kwargs:
            warn_deprecated(
                since, message=f"The {old!r} parameter of {func.__name__}() "
                f"has been renamed {new!r} since PyQt-Fluent-Widgets {since}; support "
                f"for the old name will be dropped %(removal)s.")
            kwargs[new] = kwargs.pop(old)
        return func(*args, **kwargs)

    # wrapper() must keep the same documented signature as func(): if we
    # instead made both *old* and *new* appear in wrapper()'s signature, they
    # would both show up in the pyplot function for an Axes method as well and
    # pyplot would explicitly pass both arguments to the Axes method.

    return wrapper


class _deprecated_parameter_class:
    def __repr__(self):
        return "<deprecated parameter>"


_deprecated_parameter = _deprecated_parameter_class()


def _delete_parameter(since, name, func=None, **kwargs):
    """
    Decorator indicating that parameter *name* of *func* is being deprecated.

    The actual implementation of *func* should keep the *name* parameter in its
    signature, or accept a ``**kwargs`` argument (through which *name* would be
    passed).

    Parameters that come after the deprecated parameter effectively become
    keyword-only (as they cannot be passed positionally without triggering the
    DeprecationWarning on the deprecated parameter), and should be marked as
    such after the deprecation period has passed and the deprecated parameter
    is removed.

    Parameters other than *since*, *name*, and *func* are keyword-only and
    forwarded to `.warn_deprecated`.

    Examples
    --------
    ::

        @_delete_parameter("3.1", "unused")
        def func(used_arg, other_arg, unused, more_args): ...
    """

    if func is None:
        return functools.partial(_delete_parameter, since, name, **kwargs)

    signature = inspect.signature(func)
    # Name of `**kwargs` parameter of the decorated function, typically
    # "kwargs" if such a parameter exists, or None if the decorated function
    # doesn't accept `**kwargs`.
    kwargs_name = next((param.name for param in signature.parameters.values()
                        if param.kind == inspect.Parameter.VAR_KEYWORD), None)
    if name in signature.parameters:
        kind = signature.parameters[name].kind
        is_varargs = kind is inspect.Parameter.VAR_POSITIONAL
        is_varkwargs = kind is inspect.Parameter.VAR_KEYWORD
        if not is_varargs and not is_varkwargs:
            func.__signature__ = signature = signature.replace(parameters=[
                param.replace(default=_deprecated_parameter)
                if param.name == name else param
                for param in signature.parameters.values()])
    else:
        is_varargs = is_varkwargs = False
        assert kwargs_name, (
            f"PyQt-Fluent-Widgets internal error: {name!r} must be a parameter for "
            f"{func.__name__}()")

    addendum = kwargs.pop('addendum', None)

    @functools.wraps(func)
    def wrapper(*inner_args, **inner_kwargs):
        arguments = signature.bind(*inner_args, **inner_kwargs).arguments
        if is_varargs and arguments.get(name):
            warn_deprecated(
                since, message=f"Additional positional arguments to "
                f"{func.__name__}() are deprecated since %(since)s and "
                f"support for them will be removed %(removal)s.")
        elif is_varkwargs and arguments.get(name):
            warn_deprecated(
                since, message=f"Additional keyword arguments to "
                f"{func.__name__}() are deprecated since %(since)s and "
                f"support for them will be removed %(removal)s.")
        # We cannot just check `name not in arguments` because the pyplot
        # wrappers always pass all arguments explicitly.
        elif any(name in d and d[name] != _deprecated_parameter
                 for d in [arguments, arguments.get(kwargs_name, {})]):
            deprecation_addendum = (
                f"If any parameter follows {name!r}, they should be passed as "
                f"keyword, not positionally.")
            warn_deprecated(
                since,
                name=repr(name),
                obj_type=f"parameter of {func.__name__}()",
                addendum=(addendum + " " + deprecation_addendum) if addendum
                         else deprecation_addendum,
                **kwargs)
        return func(*inner_args, **inner_kwargs)

    return wrapper


def _make_keyword_only(since, name, func=None):
    """
    Decorator indicating that passing parameter *name* (or any of the following
    ones) positionally to *func* is being deprecated.
    """

    if func is None:
        return functools.partial(_make_keyword_only, since, name)

    signature = inspect.signature(func)
    POK = inspect.Parameter.POSITIONAL_OR_KEYWORD
    KWO = inspect.Parameter.KEYWORD_ONLY
    assert (name in signature.parameters
            and signature.parameters[name].kind == POK), (
        f"PyQt-Fluent-Widgets internal error: {name!r} must be a positional-or-keyword "
        f"parameter for {func.__name__}()")
    names = [*signature.parameters]
    kwonly = [name for name in names[names.index(name):]
              if signature.parameters[name].kind == POK]
    func.__signature__ = signature.replace(parameters=[
        param.replace(kind=KWO) if param.name in kwonly else param
        for param in signature.parameters.values()])

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Don't use signature.bind here, as it would fail when stacked with
        # _rename_parameter and an "old" argument name is passed in
        # (signature.bind would fail, but the actual call would succeed).
        idx = [*func.__signature__.parameters].index(name)
        if len(args) > idx:
            warn_deprecated(
                since, message="Passing the %(name)s %(obj_type)s "
                "positionally is deprecated since PyQt-Fluent-Widgets %(since)s; the "
                "parameter will become keyword-only %(removal)s.",
                name=name, obj_type=f"parameter of {func.__name__}()")
        return func(*args, **kwargs)

    return wrapper

