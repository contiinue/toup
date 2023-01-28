class HHError(Exception):
    """
    for possible errors related to the HeadHunter.
    All list of errors response can see on
    https://github.com/hhru/api/blob/master/docs/errors.md#negotiations
    """


class AuthError(HHError):
    """
    If access token expired or invalid
    """


class ToContinueError(HHError):
    """
    For errors related to a specific job and not related to an error in the resume
    """


class ToBreakError(HHError):
    """
    For errors related to resumes or response requests
    """
