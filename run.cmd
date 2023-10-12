@echo off
setlocal enabledelayedexpansion

:: Limpieza de pantalla
cls

:: Establece el número total de iteraciones
set "max_iterations=0"

:: Bucle que va de 0 a n (max_iterations)
for /l %%i in (0,1,%max_iterations%) do (
    :: Ejecuta las pruebas en la carpeta steps
    robot ^
        --name "Test crear cuenta y transferir fondos" ^
        --metadata robot:6.1.1^
        --metadata python:3.11^
        --metadata chrome:118^
        --metadata seleniumlibrary:6.1.2^
        --include creacion-transferencias ^
        --variable ITERATION:%%i ^
        --variablefile ./data/variables/globals.yml ^
        --outputdir ./results/ ^
        --log creacion-transferencias ^
        --report creacion-transferencias ^
        --output creacion-transferencias ^
        tests/steps/
)

endlocal
