<img src="./docs/assets/logo_notas_musicais.png" width="200">

# Notas Musicais

[![Documentation Status](https://readthedocs.org/projects/notas-musicais-kylefelipe/badge/?version=latest)](https://notas-musicais-kylefelipe.readthedocs.io/en/latest/?badge=latest) 
![CI](https://github.com/kylefelipe/notas-musicais/actions/workflows/pipeline.yaml/badge.svg) 
[![codecov](https://codecov.io/github/kylefelipe/notas-musicais/branch/main/graph/badge.svg?token=8TS8VMT18N)](https://codecov.io/github/kylefelipe/notas-musicais)

Notas musicais é um CLI para ajudar na formação de escalas, acordes e campos hamônicos.

Toda a aplicação é baseada em um comando chamado `notas-musicais`. Esse comando tem um subcmando relacionando a cada ação que a aplicação pode realizar. Comando `escalas`, `acordes` e `campo-harmonico`.

## Instalação

Para a instalação do projeto recomendamos que use o `pipx` para fazer essa instalação:

```bash
pipx install notas-musicais
```

Embora isso seja somente uma recomendação! Você pode usar o gerenciador de sua preferência. Como o `pip`

```bash
pip install notas-musicais
```

## Como usar?

### Escalas

Você pode usar as escalas via linha de comando. Por exemplo:

```bash
notas-musicais escala
```

Retornando os graus e as notas correspondentes a essa escala:

```bash
┏━━━┳━━━━┳━━━━━┳━━━━┳━━━┳━━━━┳━━━━━┓
┃ I ┃ II ┃ III ┃ IV ┃ V ┃ VI ┃ VII ┃
┡━━━╇━━━━╇━━━━━╇━━━━╇━━━╇━━━━╇━━━━━┩
│ C │ D  │ E   │ F  │ G │ A  │ B   │
└───┴────┴─────┴────┴───┴────┴─────┘
```

#### Alteração da tônica da escala

O primeiro parâmetro do CLI é a tônica da escala que deseja exibir. Desta forma, você pode alterar a escala a ser retornada. Por exemplo, a escala de `F#`:

```bash
notas-musicais escala F#
```

Resultando em:

```bash
┏━━━━┳━━━━┳━━━━━┳━━━━┳━━━━┳━━━━┳━━━━━┓
┃ I  ┃ II ┃ III ┃ IV ┃ V  ┃ VI ┃ VII ┃
┡━━━━╇━━━━╇━━━━━╇━━━━╇━━━━╇━━━━╇━━━━━┩
│ F# │ G# │ A#  │ B  │ C# │ D# │ F   │
└────┴────┴─────┴────┴────┴────┴─────┘
```

#### Ateralção na tonalidade da escala

Você pode alterar a tonalidade da escala também! Esse é o segundo parametro da linha de comando. Por exemplo, a escala de `D#` maior

```bash
notas-musicais escala D# maior
```

Resultando em:

```bash
┏━━━━┳━━━━┳━━━━━┳━━━━┳━━━━┳━━━━┳━━━━━┓
┃ I  ┃ II ┃ III ┃ IV ┃ V  ┃ VI ┃ VII ┃
┡━━━━╇━━━━╇━━━━━╇━━━━╇━━━━╇━━━━╇━━━━━┩
│ D# │ F  │ G   │ G# │ A# │ C  │ D   │
└────┴────┴─────┴────┴────┴────┴─────┘
```

## Acordes

Uso básico:

```bash
notas-musicais acorde
┏━━━┳━━━━━┳━━━┓
┃ I ┃ III ┃ V ┃
┡━━━╇━━━━━╇━━━┩
│ C │ E   │ G │
└───┴─────┴───┘
```

### Variações na cifra

```bash
notas-musicais acorde C+
┏━━━┳━━━━━┳━━━━┓
┃ I ┃ III ┃ V+ ┃
┡━━━╇━━━━━╇━━━━┩
│ C │ E   │ G# │
└───┴─────┴────┘
```

```bash
notas-musicais acorde C°
```

Irá retornar:

```bash
┏━━━┳━━━━━━┳━━━━┓
┃ I ┃ III- ┃ V- ┃
┡━━━╇━━━━━━╇━━━━┩
│ C │ D#   │ F# │
└───┴──────┴────┘
```

Até o momento você pode usar acordes maiores, menores (`m`), aumentados (`+`) e diminutos (`°`)

## Campo hamônico

Você pode chamar os campos harmônicos via o subcomando `campo-harmonico`. Por exemplo:

```bash
notas-musicais campo-hamonico
```

### Alteração na tônica do campo

Um exemplo com o campo harmônico de `E`:

```bash
notas-musicais E

┏━━━┳━━━━━┳━━━━━┳━━━━┳━━━┳━━━━━┳━━━━━━┓
┃ I ┃ ii  ┃ iii ┃ IV ┃ V ┃ vi  ┃ vii° ┃
┡━━━╇━━━━━╇━━━━━╇━━━━╇━━━╇━━━━━╇━━━━━━┩
│ E │ F#m │ G#m │ A  │ B │ C#m │ D#°  │
└───┴─────┴─────┴────┴───┴─────┴──────┘
```

### Alteração da tonalidade de campo

Um exemplo utilizando o campo harmonico de `E` na tonalidade `menor`:

```bash
notas-musicais campo-harmonico E menor

┏━━━━┳━━━━━┳━━━━━┳━━━━┳━━━━┳━━━━┳━━━━━┓
┃ i  ┃ ii° ┃ III ┃ iv ┃ v  ┃ VI ┃ VII ┃
┡━━━━╇━━━━━╇━━━━━╇━━━━╇━━━━╇━━━━╇━━━━━┩
│ Em │ F#° │ G   │ Am │ Bm │ C  │ D   │
└────┴─────┴─────┴────┴────┴────┴─────┘
```

## Mais informações sobre o CLI

Para descobir outras opções, você pode usar a flag `--help`:

```bash
notas-musicais --help

 Usage: notas-musicais [OPTIONS] [TONICA] [TONALIDADE]                                                 
                                                                                                
╭─ Commands ───────────────────────────────────────────────────╮
│ acorde                                                       │
│ campo-harmonico                                              │
│ escala                                                       │
╰──────────────────────────────────────────────────────────────╯
```

### Mais informações sobre os subcomandos

As informações sobre os subcomandos podem ser acessadas usando a flag `--help` após o nome do parâmentro. Um exemplo do uso do `help` nos campos hamrônicos:

```bash
 Usage: notas-musicais campo-harmonico [OPTIONS] [TONICA] [TONALIDADE]               
                                                                                     
╭─ Arguments ───────────────────────────────────────────────────────────────────────╮
│   tonica          [TONICA]      Tonica do campo harmonico [default: C]            │
│   tonalidade      [TONALIDADE]  Tonalidade do campo harmonico [default: maior]    │
╰───────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                       │
╰───────────────────────────────────────────────────────────────────────────────────╯
```
