"""Módulo responsável pela criação de campos harmônicos."""
from notas_musicais.acordes import triade
from notas_musicais.escalas import escala


def _triade_na_escala(nota, nota_da_escala) -> list[str]:
    """
    Saber se as notas de um acorde estão na escala.

    Examples:
        >>> _triade_na_escala('C', ['C', 'D', 'E', 'F', 'G', 'A', 'B'])
        'C'
        >>> _triade_na_escala('D', ['C', 'D', 'E', 'F', 'G', 'A', 'B'])
        'Dm'
        >>> _triade_na_escala('B', ['C', 'D', 'E', 'F', 'G', 'A', 'B'])
        'B°'
    """
    tonica, terca, quinta = triade(nota, 'maior')
    match terca in nota_da_escala, quinta in nota_da_escala:
        case True, True:
            return tonica
        case False, True:
            return f'{tonica}m'
        case False, False:
            return f'{tonica}°'
    pass


def _converte_graus(cifra, grau):
    """
    Convert o grau relativo à cifra.

    Parameters:
        cifra: Cifra da música.
        grau: Grau em forma maior.

    Examples:
        >>> _converte_graus('C', 'I')
        'I'
        >>> _converte_graus('Cm', 'I')
        'i'
        >>> _converte_graus('C°', 'I')
        'i°'
    """
    if 'm' in cifra:
        return grau.lower()
    elif '°' in cifra:
        return f'{grau.lower()}°'
    return grau


def campo_harmonico(tonica: str, tonalidade: str) -> dict[str, list[str]]:
    """
    Gera um campo hamonico com base em uma tônica e uma tonalidade.

    Parameters:
        tonica: Tônica da escala.
        tonalidade: Tonalidade da escala.

    Returns:
        Um campo harmonico.

    Examples:
        >>> campo_harmonico('C', 'maior')
        {'acordes': ['C', 'Dm', 'Em', 'F', 'G', 'Am', 'B°'], 'graus': ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°']}

        >>> campo_harmonico('C', 'menor')
        {'acordes': ['Cm', 'D°', 'D#', 'Fm', 'Gm', 'G#', 'A#'], 'graus': ['i', 'ii°', 'III', 'iv', 'v', 'VI', 'VII']}
    """
    notas, _graus = escala(tonica, tonalidade).values()
    acordes = [_triade_na_escala(nota, notas) for nota in notas]
    graus = [
        _converte_graus(acorde, grau) for acorde, grau in zip(acordes, _graus)
    ]
    return {'acordes': acordes, 'graus': graus}
