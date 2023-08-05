def docstring(amount_args=1):
    """
    Makes a docstring, dependend on what you put in.
    It will be formatted like this docstring.
    When a enter is passed instead of an input, no text will be displayed.
    Default values should be passed by the argument type.

    Parameters:
    --------------------
    amount_args : int (default = 1)
        The amount of arguments used in the function

    Returns:
    --------------------
    docstring : str
        The docstring following the information given and following this format
    """

    # If-statement for checking the type passed for amount_args
    if isinstance(amount_args, int):
        # Values are being made by using inputs
        # input for summary of the function
        summary = input("Write the summary of your function: ")

        # input for the arguments, making sure
        # that x amount_args are being called and filled
        arguments = []
        argument_expl = []
        for x in range(1, amount_args + 1):
            # input for arguments, type, default values and explanations
            arg = input(f"Write the name of parameter {x}: ")
            typ = input(f"Write the type of parameter {x}: ")
            default = input(f"Write the (default = x) of parameter {x}: ")
            typ_def = f'{typ} {default}'
            arguments.append((arg, typ_def))
            expl = input(f"Write the explanation of parameter {x}: ")
            argument_expl.append(expl)

        # input for return value name, type and explanation
        return_name = input("Write the name of the returned value: ")
        return_type = input("Write the type of the returned value: ")
        return_expl = input("Write the explanation of the returned value: ")

        # Assembling the docstring
        doc = f'\n    """\n    {summary}\n\n'
        doc += '    Parameters:'
        doc += '\n    ' + '-' * 20 + '\n'
        for argument, explain in zip(arguments, argument_expl):
            doc += f'    {argument[0]} : {argument[1]}\n        {explain}\n\n'
        doc += '    Returns:'
        doc += '\n    ' + '-' * 20 + '\n'
        doc += f'    {return_name} : {return_type}\n        {return_expl}\n'
        doc += '    """'

        return print(doc)

    # Raises an error when amount_args != an integer
    else:
        raise ValueError(f'The amount of arguments {amount_args} \
                         is not an integer, please refrain from \
                         trying non-integers')
