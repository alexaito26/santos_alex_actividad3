<table style="width: 100%; border: none; border-collapse: collapse; background-color: transparent;">
  <tr style="border: none; background-color: transparent;">
    <td style="width: 120px; border: none; padding: 10px; vertical-align: middle; background-color: transparent;">
      <img src="logo-puce-manabi.png" alt="Logo PUCE Manabi" style="width: 100px; height: auto;" />
    </td>
    <td style="border: none; padding: 10px; vertical-align: middle; line-height: 1.5; background-color: transparent;">
      <h2 style="margin: 0; color: #1e3a8a; font-family: Arial, sans-serif; font-weight: bold;">
        Pontificia Universidad Católica del Ecuador Sede Manabí
      </h2>
      <h3 style="margin: 5px 0 0 0; color: #475569; font-family: Arial, sans-serif; font-weight: normal;">
        Carrera de Ingeniería de Software
      </h3>
    </td>
  </tr>
</table>

---

# Guía Rápida: Bibliotecas Estándar de Pruebas en Python

* **Asignatura:** Desarrollo de Sistemas de Información
* **Docente:** Ing. José Naranjo, M.Eng.
* **Período:** 2026-1 | Parcial 3

---

Esta guía rápida resume las herramientas nativas que Python incluye en su biblioteca estándar para realizar pruebas de software, eliminando la necesidad de instalar dependencias externas.

---

## 1. El Módulo unittest

Es la herramienta principal para escribir pruebas. Está basada en el estándar xUnit (común en otros lenguajes como JUnit en Java).

### Conceptos Clave
* **TestCase**: Clase base de la que heredan todas nuestras clases de prueba. Cada método dentro de esta clase que comience con la palabra `test_` será ejecutado como una prueba individual.
* **Assertions (Aserciones)**: Métodos que verifican si una condición se cumple. Si la condición falla, la prueba se marca como FAILED.
* **Test Suite y Test Runner**: Mecanismos que agrupan y ejecutan las pruebas (ej. la consola o un IDE).

### Estructura Básica
```python
import unittest

def sumar(a, b):
    return a + b

class TestOperaciones(unittest.TestCase):
    def test_sumar_positivos(self):
        # Aserción para comparar el resultado
        self.assertEqual(sumar(2, 3), 5)

if __name__ == '__main__':
    unittest.main()
```

### Métodos de Aserción más Comunes
| Método | Lo que verifica |
| :--- | :--- |
| `self.assertEqual(a, b)` | Compara si `a == b` |
| `self.assertNotEqual(a, b)` | Compara si `a != b` |
| `self.assertTrue(x)` | Verifica si la expresión `x` es verdadera (`True`) |
| `self.assertFalse(x)` | Verifica si la expresión `x` es falsa (`False`) |
| `self.assertIsNone(x)` | Verifica si `x` es exactamente `None` |
| `self.assertIsNotNone(x)` | Verifica si `x` no es `None` |
| `self.assertIn(elemento, coleccion)` | Verifica si un elemento pertenece a una lista, diccionario, etc. |
| `self.assertRaises(Excepcion)` | Verifica que un bloque de código lance una excepción específica |

### Ciclo de Vida: setUp y tearDown
Permiten ejecutar código antes y después de cada prueba para preparar y limpiar bases de datos, archivos o estados de la memoria.

```python
class TestConexion(unittest.TestCase):
    def setUp(self):
        # Se ejecuta ANTES de cada método test_
        self.conexion = abrir_base_datos()

    def tearDown(self):
        # Se ejecuta DESPUÉS de cada método test_
        self.conexion.cerrar()

    def test_consulta(self):
        # Utiliza self.conexion
        pass
```

---

## 2. El Módulo unittest.mock

Permite simular componentes externos, APIs de terceros, bases de datos o servicios lentos de red para mantener las pruebas unitarias rápidas y aisladas.

### Objeto Mock y return_value
Un `Mock` registra qué métodos se llamaron sobre él y qué argumentos recibió.

```python
from unittest.mock import Mock
import unittest

class TestMockBasico(unittest.TestCase):
    def test_simulador(self):
        # Crear simulador
        servicio_externo = Mock()
        
        # Configurar retorno de llamada
        servicio_externo.obtener_clima.return_value = "Soleado"
        
        # Usar el mock
        resultado = servicio_externo.obtener_clima("Quito")
        
        # Verificar comportamiento
        self.assertEqual(resultado, "Soleado")
        
        # Validar si el carrito o código realmente llamó a ese método
        servicio_externo.obtener_clima.assert_called_once_with("Quito")
```

### Parchear con patch
La función `patch` (utilizable como decorador o manejador de contexto) reemplaza temporalmente un objeto en otro módulo con un Mock durante el transcurso de una prueba.

```python
from unittest.mock import patch
import unittest
import requests  # Imaginemos que nuestro código interno usa requests

class TestApi(unittest.TestCase):
    @patch('requests.get') # Parcheamos la llamada externa
    def test_llamar_api(self, mock_get):
        # Configuramos la respuesta del mock
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"status": "ok"}
        
        # El código bajo prueba llamará al mock, no a internet real
        response = requests.get("https://api.servicio.com/data")
        
        self.assertEqual(response.json(), {"status": "ok"})
```

---

## 3. El Módulo doctest

Es una herramienta alternativa muy ligera. Ejecuta fragmentos de código interactivos que han sido escritos directamente dentro de las cadenas de documentación (docstrings) de tus funciones para verificar que la documentación no esté obsoleta.

### Ejemplo de Doctest
```python
def multiplicar(a, b):
    """
    Multiplica dos números enteros.

    Ejemplos de uso dentro de la documentación:
    >>> multiplicar(2, 3)
    6
    >>> multiplicar(-1, 5)
    -5
    """
    return a * b

if __name__ == '__main__':
    import doctest
    doctest.testmod() # Busca doctests en el módulo actual y los ejecuta
```

Si ejecutas este script y todo coincide con los resultados especificados en los bloques `>>>`, el programa correrá de forma silenciosa. Si un valor no coincide, te mostrará un reporte detallado del error.
