"""This package contains tools to annotate transform outputs with a content type."""
from dataclasses import dataclass

COMMON_MIMETYPES = {
    'jpg': 'image/jpeg',
    'mp3': 'audio/mpeg',
    'mp4': 'video/mp4',
    'png': 'image/png',
    'svg': 'image/svg+xml',
    'wav': 'audio/wav',
}


@dataclass(frozen=True)
class ContentType:
    """The Content Type class."""

    mimetype: str


def content_type(mimetype: str) -> ContentType:
    """The ContentType factory.

    Parameters:
        mimetype: The MIME type used in the content type.

    Returns:
        The ContentType instance associated with the mime type.

    Examples:
        >>> content_type('wav')
        ContentType(mimetype='audio/wav')
        >>> content_type('text/csv')
        ContentType(mimetype='text/csv')
    """
    mimetype = mimetype.lower()
    try:
        mimetype = COMMON_MIMETYPES[mimetype]
    except KeyError:
        pass
    return ContentType(mimetype)
