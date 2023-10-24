# Variables
$testdata_file = "data/steps/test_data.csv"
$line_count = 0

# Obtener el directorio base
$basedir = Get-Location

# Contar las líneas en el archivo CSV
$max_iterations = (Get-Content $testdata_file | Measure-Object -Line).Lines
$max_iterations -= 2

# Bucle que va de 0 a n (max_iterations)
for ($i = 0; $i -le $max_iterations; $i++) {
    # Obtener el sufijo del directorio de resultados
    $resultdir_sufix = python data/actions/date_time.py
    
    # Definir el directorio de salida de resultados
    $results_output_dir = "results/result--$i--$resultdir_sufix"
    
    # Crear el directorio de salida de resultados
    New-Item -ItemType Directory -Path $results_output_dir -Force
    
    # Ejecutar las pruebas en la carpeta steps
    robot `
        --name "Test crear cuenta y transferir fondos" `
        --metadata robot:6.1.1 `
        --metadata python:3.11 `
        --metadata chrome:118 `
        --metadata seleniumlibrary:6.1.2 `
        --include creacion-transferencias `
        --variable ITERATION:$i `
        --variablefile ./data/variables/globals.yml `
        --outputdir $results_output_dir `
        --log creacion-transferencias `
        --output creacion-transferencias `
        tests/steps/
}
