import logging

import uvicorn

from config.base import settings

reload_ignore_files = ["__pycache__", ".pytest_cache", "*.pyc", ".git", "*.tmp"]


def main():
    uvicorn.run(
        app="api.app:application",
        host=settings.HOST,
        port=settings.PORT,
        log_level=logging.DEBUG,
        reload=settings.DEBUG,
        debug=settings.DEBUG,
        reload_excludes=reload_ignore_files,
        use_colors=True,
    )


if __name__ == "__main__":
    main()
