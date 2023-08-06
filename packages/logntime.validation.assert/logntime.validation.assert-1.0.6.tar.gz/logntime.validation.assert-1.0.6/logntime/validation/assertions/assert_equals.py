from logntime.validation.assertions.transform import bypass, to_caped_str


def assert_equals(reference: object, subject: object, custom_message: str = "", accumulator: list = None, format_data=to_caped_str):
    """
    Validates equality between objects.

    :param reference: Source of truth to compare equality
    :param subject: Object under analysis
    :param custom_message: Clarification sentence at the beginning of the error message thrown if the validation fails.
    :param accumulator: List used to aggregate error messages. If not None and the validation fails, no exception is thrown.
    :param format_data: transform the reference and subject before formatting the message. The default is to_caped_str.

    :raises Exception: If the reference and the subject are not equal
    """
    if reference is subject: return
    if reference == subject: return

    message = f"{custom_message}Subject is not equal to reference.\n    Reference: {format_data(reference)}\n    Subject: {format_data(subject)}"
    error = Exception(message)

    if accumulator is None:
        raise error
    else:
        accumulator.append(message)


def assert_not_equals(reference: object, subject: object, custom_message: str = "", accumulator: list = None, format_data=to_caped_str):
    """
    Validates that two objects not are equal.

    :param reference: Source of truth to compare equality
    :param subject: Object under analysis
    :param custom_message: Clarification sentence at the beginning of the error message thrown if the validation fails.
    :param accumulator: List used to aggregate error messages. If not None and the validation fails, no exception is thrown.
    :param format_data: transform the reference and subject before formatting the message. The default is to_caped_str.

    :raises Exception: If the reference and the subject are not equal
    """

    if reference != subject: return
    message = f"{custom_message}Subject is equal to reference.\n    Reference: {format_data(reference)}\n    Subject: {format_data(subject)}"
    error = Exception(message)

    if accumulator is None:
        raise error
    else:
        accumulator.append(message)
