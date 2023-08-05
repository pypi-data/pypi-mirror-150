from nbconvert.utils.pandoc import pandoc


def convert_pandoc(source, from_format, to_format, extra_args=None):
    """Convert between any two formats using pandoc.

    This function will raise an error if pandoc is not installed.
    Any error messages generated by pandoc are printed to stderr.

    Parameters
    ----------
    source : string
        Input string, assumed to be valid in from_format.
    from_format : string
        Pandoc format of source.
    to_format : string
        Pandoc format for output.

    Returns
    -------
    out : string
        Output as returned by pandoc.
    """
    return pandoc(source, from_format, to_format, extra_args=extra_args)
