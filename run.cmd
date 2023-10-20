@echo off
setlocal enabledelayedexpansion

:: VARIABLES
set testdata_file=data/steps/test_data.csv
set /a line_count=0

:: cuenta las líneas en el archivo CSV
for /f %%a in (%testdata_file%) do (
    set /a max_iterations+=1
)
set /a max_iterations-=2

:: Bucle que va de 0 a n (max_iterations)
for /l %%i in (0,1,%max_iterations%) do (
    set "results_output_dir=results/result-%%i"
    mkdir "!results_output_dir!"
    :: Ejecuta las pruebas en la carpeta steps
    robot ^
        --name "Test crear cuenta y transferir fondos"^
        --metadata robot:6.1.1^
        --metadata python:3.11^
        --metadata chrome:118^
        --metadata seleniumlibrary:6.1.2^
        --include creacion-transferencias ^
        --variable ITERATION:%%i ^
        --variablefile ./data/variables/globals.yml ^
        --outputdir "!results_output_dir!" ^
        --log creacion-transferencias ^
        --output creacion-transferencias ^
        tests/steps/
)

endlocal
