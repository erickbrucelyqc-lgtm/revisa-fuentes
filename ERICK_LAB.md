# Revisa fuentes · Erick Quio

**Auditor offline de referencias numeradas.** Fork de
[Vane](https://github.com/ItzCrazyKns/Vane), anteriormente Perplexica, con licencia MIT.
Este laboratorio añade una utilidad independiente para revisar respuestas de investigación.
No representa una contribución aceptada por upstream.

## Aportación local

- Detecta referencias `[1]`, `[2]`, etc., sin contar repeticiones como citas nuevas.
- Señala IDs ausentes, fuentes sin uso y URLs con formato no admitido.
- Produce una tasa de resolución estructural de referencias.
- Rechaza identificadores duplicados y estructuras de entrada inválidas.

La herramienta **no evalúa veracidad, relevancia ni calidad semántica**.
No descarga fuentes: que una URL tenga formato correcto no garantiza que exista.

## Ejecutar

Python 3.10 o posterior, sin dependencias de ejecución:

```bash
python erick_citation_audit.py erick_sample.json
```

La muestra devuelve una referencia desconocida `[9]`, una fuente sin uso `[3]`
y una tasa de resolución de `0.667`. Cuando no hay citas, la tasa es `null`.

### Contrato de entrada

```json
{
  "answer": "Una respuesta con una referencia [1].",
  "sources": [{"id": 1, "url": "https://example.org"}]
}
```

Este es un **formato propio del laboratorio**, no el contrato nativo de la API de Vane.
Adapta manualmente una respuesta y sus fuentes antes de analizarla. Las referencias
agrupadas como `[1,2]` y las notas Markdown no se interpretan en esta versión.

## Verificación

```bash
python -m pip install pytest
python -m pytest test_erick_citation_audit.py -q
```

Pruebas locales: referencias ausentes, repetidas y sin uso; ausencia de citas;
esquemas de URL inválidos; IDs duplicados y booleanos.
No se ejecutó Vane ni se realizaron consultas a un proveedor de modelos.
