Feature: Creacion de cuenta
    Como un usuario autenticado
    Quiero crear una cuenta
    Y obtener el numero de cuenta que se ha creado

    Scenario: Crear una cuenta
        Given Que estoy en el home page de la aplicacion
        And Selecciono el link "Open New Account"
        When Ingreso el tipo de cuenta y la cuenta de referencia
        And Doy clic en el boton "Open New Account"
        Then Obtengo el numero de cuenta creada
