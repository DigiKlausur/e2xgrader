from ..apps import E2xGrader


def get_e2xgrader_mode() -> str:
    """
    Returns the current mode of E2xGrader.

    Returns:
        str: The current mode of E2xGrader.
    """
    app = E2xGrader()
    app.initialize([])
    return app.mode
