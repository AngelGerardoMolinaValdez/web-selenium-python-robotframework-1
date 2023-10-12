Feature: Inicio de sesion
    Como un usuario normal
    Busco iniciar sesion con credenciales correctas

    Scenario: Iniciar sesion
        Given Estoy en la url de la aplicacion
        When Escribo las credenciales en los campos
        And Doy clic en iniciar sesion
        Then Puedo ver el mensaje "Welcome"
