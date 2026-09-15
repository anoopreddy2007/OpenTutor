def validate_response_sequence(
    responses: list[bool],
) -> list[bool]:
    """Validate and return a learner response sequence."""

    if not isinstance(responses, list):
        raise TypeError("responses must be a list")

    for response in responses:
        if not isinstance(response, bool):
            raise ValueError(
                "Each response must be True or False"
            )

    return responses