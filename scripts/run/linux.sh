#!/bin/bash

# VARIABLES
testdata_file="data/steps/test_data.csv"
line_count=0

# Obtener el directorio base
basedir=$(pwd)

# Contar las líneas en el archivo CSV
max_iterations=$(wc -l < "$testdata_file")
max_iterations=$((max_iterations - 2))

python data/actions/create_tests_results.py

# Bucle que va de 0 a n (max_iterations)
for ((i=0; i<=max_iterations; i++)); do
    # Obtener el sufijo del directorio de resultados
    resultdir_sufix=$(python data/actions/date_time.py)
    
    # Definir el directorio de salida de resultados
    results_output_dir="output/reports/report---$i---$resultdir_sufix"
    
    # Crear el directorio de salida de resultados
    mkdir -p "$results_output_dir"
    
    # Ejecutar las pruebas en la carpeta steps
    robot \
        --name "Test crear cuenta y transferir fondos" \
        --metadata robot:6.1.1 \
        --metadata python:3.11 \
        --metadata chrome:118 \
        --metadata seleniumlibrary:6.1.2 \
        --include creacion-transferencias \
        --include general `
        --runemptysuite `
        --variable ITERATION:$i \
        --variablefile ./data/variables/globals.yml \
        --outputdir "$results_output_dir" \
        --log creacion-transferencias \
        --output creacion-transferencias \
        tests/steps/
done
