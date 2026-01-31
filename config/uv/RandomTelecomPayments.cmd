:: call powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
call uv add -r requirements.txt --link-mode=copy