# memory-forward/__init__.py

__app_name__ = "memory-forward"
__version__ = "0.0.1a1"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
) = range(3)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error"
}
