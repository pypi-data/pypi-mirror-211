"""
Módulo de acordes.

O módulo de acordes conta com funções e feramentas necessárias para a geração de acordes.
"""
from notas_musicais.escalas import NOTAS, escala


def _menor(cifra):
    nota, _ = cifra.split('m')
    if '+' in cifra:
        tonica, terca, quinta = triade(nota, 'menor')
        notas = [tonica, terca, semiton(quinta, intervalo=+1)]
        graus = ['I', 'III-', 'V+']
    else:
        notas = triade(nota, 'menor')
        graus = ['I', 'III-', 'V']
    return notas, graus


def semiton(nota, intervalo) -> list[str]:
    """
    Calcula a distancia em semitons entre duas notas usando intervalos.

    Parameters:
        nota: Nota de referência
        intervalo: Intervalo em semitons

    Returns:
        Uma nota correspondente ao intervalo dado

    Examples:
        >>> semiton('C', intervalo=+1)
        'C#'

        >>> semiton('C', intervalo=-1)
        'B'
    """
    pos = NOTAS.index(nota.upper())
    return NOTAS[(pos + intervalo) % len(NOTAS)]


def triade(nota, tonalidade) -> list[str]:
    """
    Gera tríades de uma nota tônica e uma tonalidade.

    Parameters:
        nota: Uma nota da qual se deseja obter a tríade
        tonalidade: Uma tonalidade na qual será formado o acorde

    Returns:
        A tríade do acorde referente a nota e tonalidade

    Examples:
        >>> triade('C', 'maior')
        ['C', 'E', 'G']

        >>> triade('C', 'menor')
        ['C', 'D#', 'G']
    """
    graus = (0, 2, 4)
    notas_da_escala, _ = escala(nota, tonalidade).values()

    return [notas_da_escala[grau] for grau in graus]


def acorde(cifra: str) -> dict[str, list[str]]:
    """
    Gera as notas de um acorde a partir de uma cifra

    Parameters:
        cifra: Cifra de um acorde

    Returns:
        Um dicionário com as notas e graus do acorde

    Examples:
        >>> acorde('C')
        {'notas': ['C', 'E', 'G'], 'graus': ['I', 'III', 'V']}

        >>> acorde('Cm')
        {'notas': ['C', 'D#', 'G'], 'graus': ['I', 'III-', 'V']}

        >>> acorde('C°')
        {'notas': ['C', 'D#', 'F#'], 'graus': ['I', 'III-', 'V-']}

        >>> acorde('C+')
        {'notas': ['C', 'E', 'G#'], 'graus': ['I', 'III', 'V+']}

        >>> acorde('Cm+')
        {'notas': ['C', 'D#', 'G#'], 'graus': ['I', 'III-', 'V+']}
    """
    graus = (0, 2, 4)
    if 'm' in cifra:
        notas, graus = _menor(cifra)

    elif '°' in cifra:
        nota, _ = cifra.split('°')
        tonica, terca, quinta = triade(nota, 'menor')
        notas = [tonica, terca, semiton(quinta, intervalo=-1)]
        graus = ['I', 'III-', 'V-']

    elif '+' in cifra:
        nota, _ = cifra.split('+')
        tonica, terca, quinta = triade(nota, 'maior')
        notas = [tonica, terca, semiton(quinta, intervalo=+1)]
        graus = ['I', 'III', 'V+']

    else:
        notas = triade(cifra, 'maior')
        graus = ['I', 'III', 'V']

    return {'notas': notas, 'graus': graus}
