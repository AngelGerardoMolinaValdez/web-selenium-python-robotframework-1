Feature: Transferencia de fondos
    Como un usuario autenticado
    Busco transferir cierta cantidad de una cuenta de referencia a otra

Scenario: Transferir fondos
    Given que estoy en el home page de la aplicacion
    And selecciono el link "Transfer funds"
    When Ingreso el monto de transferencia
    And selecciono la cuenta emisora y de destino
    Then Puedo ver el mensaje "$XXX has been transferred from account #XXX to account #XXX."
