call cd ..
call uv run python -m unittest discover generator\unittests\utilities
call uv run python -m unittest discover generator\unittests\objects
call uv run python -m unittest discover generator\unittests\app
call cd generator