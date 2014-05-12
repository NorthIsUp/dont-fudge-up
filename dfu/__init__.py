try:
    VERSION = __import__('pkg_resources').get_distribution('dont-fudge-up').version
except Exception:  # pragma: no cover
    VERSION = 'unknown'
