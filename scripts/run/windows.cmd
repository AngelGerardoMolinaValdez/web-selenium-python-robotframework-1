@echo off
setlocal enabledelayedexpansion

:: VARIABLES
set testdata_file=data/steps/test_data.csv
set /a line_count=0

for /f "delims=" %%i in ('cd') do (
    set basedir=%%i
)

for /f %%a in (%testdata_file%) do (
    set /a max_iterations+=1
)
set /a max_iterations-=2

poetry run python data/actions/create_test_results.py

:: Bucle que va de 0 a n (max_iterations)
for /l %%i in (0,1,%max_iterations%) do (
    for /f "delims=" %%a in ('poetry run python data/actions/date_time.py') do (
        set "resultdir_sufix=%%a"
    )
    set "results_output_dir=output/reports/report--%%i--!resultdir_sufix!"
    mkdir "!results_output_dir!"

    poetry run robot ^
        --name "Test crear cuenta y transferir fondos"^
        --metadata robot:6.1.1^
        --metadata python:3.11^
        --metadata chrome:118^
        --metadata seleniumlibrary:6.1.2^
        --include creacion-transferencias ^
        --include general ^
        --variable ITERATION:%%i ^
        --runemptysuite ^
        --variablefile ./data/variables/globals.yml ^
        --outputdir "!results_output_dir!" ^
        --log creacion-transferencias ^
        --output creacion-transferencias ^
        tests/steps/
)

endlocal
