"""
Módulo das escalas

Attributes:

    ESCALAS: Escalas implementadas usando a notação de intervalos.
    NOTAS: Notas musicais.
# ESCALAS

As escalas estão implementadas em uma constante chamada escalas, que é um dicionário onde as chaves são os nomes das escalas. Se quiser ver todas as escalas implementadas pode usar:

```py title="No meu shell interativo"
>>> from notas_musicais.escalas import ESCALAS
>>> ESCALAS
{'maior': (0, 2, 4, 5, 7, 9, 11), 'menor': (0, 2, 3, 5, 7, 8, 10)}

```

A notação inteira para as escalas foi retirada da página [List of musical scales and modes](https://en.wikipedia.org/wiki/List_of_musical_scales_and_modes) na wikipedia.

tip: Dica!
    Você pode contribuir com novas escalas usando a notação inteira:
    [Escalas wikipedia](https://en.wikipedia.org/wiki/List_of_musical_scales_and_modes).
    Todos os Pull Requests serão bem vindos! :heart:

# NOTAS

As notas estão sendo definidas em uma constante `NOTAS`. Foi optado por manter somentr as notas no formato Natural e o Sustenido (#). As notas bemol (b) não foram implementadas por questões de simplicidade para a simplificação do fluxo de trabalho.

```py title="No meu shell interativo"
>>> from notas_musicais.escalas import NOTAS
>>> NOTAS
['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

```
"""

NOTAS = 'C C# D D# E F F# G G# A A# B'.split()
ESCALAS = {'maior': (0, 2, 4, 5, 7, 9, 11), 'menor': (0, 2, 3, 5, 7, 8, 10)}


def escala(tonica: str, tonalidade: str) -> dict[str, list[str]]:
    """
    Gera uma escala a partir de uma tonica e uma tonalidade.

    Parameters:
        tonica: Nota que será a tônica da escala.
        tonalidade: Tonaliade da escala.

    Returns:
        Um dicionário com as notas e os graus da escala.

    Raises:
        ValueError: Caso a tônica não seja uma nota valida.
        KeyError: Caso a tonalidade não exista ou não tenha sido implementada.

    Examples:
        >>> escala('C', 'maior')
        {'notas': ['C', 'D', 'E', 'F', 'G', 'A', 'B'], 'graus': ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']}

        >>> escala('a', 'maior')
        {'notas': ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'], 'graus': ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']}
    """
    tonica = tonica.upper()
    try:
        intervalos = ESCALAS[tonalidade]
        toinca_pos = NOTAS.index(tonica)
    except ValueError:
        raise ValueError(f'Essa nota não existe, tente uma dessas {NOTAS}')
    except KeyError:
        raise KeyError(
            'Essa escala não existe ou não foi implementada,'
            f' tente uma dessas {list(ESCALAS.keys())}'
        )
    temp = []
    for intervalo in intervalos:
        _nota = (toinca_pos + intervalo) % len(NOTAS)
        temp.append(NOTAS[_nota])
    return {'notas': temp, 'graus': ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']}
