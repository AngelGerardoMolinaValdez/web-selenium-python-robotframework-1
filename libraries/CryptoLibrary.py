import cryptocode

class CryptoLibrary:
    """CryptoLibrary es una librería para encriptar y desencriptar texto.
    Se utiliza la librería cryptocode para realizar la encriptación y desencriptación.

    Para más información sobre cryptocode, visita: https://pypi.org/project/cryptocode/
    """

    def encrypt_string(self, text: str, key: str ="robot framework is amazing") -> str:
        """Encripta un texto utilizando una llave.
        
        === Descripción de los argumentos ===
        - text (str): Texto a encriptar.
        - key (str): Llave para encriptar el texto. Por defecto, es "robot framework is amazing".

        === Ejemplo de uso ===
        | ${encrypted_text} = | Encrypt String | Hello, World! | my secret key |
        | ${ENCRYPTED_TEXT} = | Encrypt String | Hello, World! |

        === Consideraciones ===
        - Si no se especifica una llave, se utilizará la llave por defecto.
        - La llave debe ser la misma para encriptar y desencriptar un texto.
        """
        return cryptocode.encrypt(text, key)
    
    def decrypt_string(self, text: str, key: str ="robot framework is amazing") -> str:
        """Desencripta un texto utilizando una llave.

        === Descripción de los argumentos ===
        - text (str): Texto a desencriptar.
        - key (str): Llave para desencriptar el texto. Por defecto, es "robot framework is amazing".

        === Ejemplo de uso ===
        | ${decrypted_text} = | Decrypt String | 5e8ff9bf | my secret key |
        | ${DECRYPTED_TEXT} = | Decrypt String | 5e8ff9bf |

        === Consideraciones ===
        - Si no se especifica una llave, se utilizará la llave por defecto.
        - La llave debe ser la misma para encriptar y desencriptar un texto.
        - Si la llave es incorrecta, el texto no se desencriptará correctamente.
        """
        return cryptocode.decrypt(text, key)
