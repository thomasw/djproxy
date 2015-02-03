# import_string was appropriated from django and then rewritten for broader
# python support. The version of this method can't be imported from Django
# directly because it didn't exist until 1.7.


def import_string(dotted_path):
    """
    Import a dotted module path.

    Returns the attribute/class designated by the last name in the path.

    Raises ImportError if the import fails.

    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        raise ImportError('%s doesn\'t look like a valid path' % dotted_path)

    module = __import__(module_path, fromlist=[class_name])

    try:
        return getattr(module, class_name)
    except AttributeError:
        msg = 'Module "%s" does not define a "%s" attribute/class' % (
            dotted_path, class_name)
        raise ImportError(msg)
