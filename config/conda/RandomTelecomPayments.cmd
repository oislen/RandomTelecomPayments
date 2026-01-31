:: list all available conda environments
call conda env list

:: create and activate new environment
call conda deactivate
call conda env remove --name RandomTelecomPayments --yes
call conda env list
call conda create --name RandomTelecomPayments python=3.12 --yes
call conda activate RandomTelecomPayments
call conda list

:: install relevant libraries
call pip install -r ..\requirements.txt

:: list all installed libraries
call conda list