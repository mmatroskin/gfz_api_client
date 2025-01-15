class ExternalServiceCommonError(Exception):
    """External service Error"""


class ExternalServiceNetworkError(ExternalServiceCommonError):
    """External service HTTP request Error"""


class InternalServiceError(Exception):
    """Inernal Error"""
