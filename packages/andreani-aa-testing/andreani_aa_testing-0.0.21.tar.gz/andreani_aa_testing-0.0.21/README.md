# Andreani Advanced Analytics testing

## Instalar usando pip

```

pip install andreani-aa-testing

```

## Importación

```

import aa_testing

```

## Ejemplo de uso

- Testing

```

from aa_testing import testing

if __name__ == "__main__":

  test = Testing(function1, function2, dataset)
  test.compare_functions()
  response = test.create_response()

```

### Listado de funciones agregadas:

* Testing: Comparación de latencia entre dos funciones.

### Listado de funciones a agregar:

* Aplicar funcion de metricas.
