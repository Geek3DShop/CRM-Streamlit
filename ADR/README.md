# Índice de decisões arquiteturais

> **Status:** atual · verificado em 2026-08-13

## Decisões registradas

| #    | Título                                                                                        | Status              | Data       |
| ---- | --------------------------------------------------------------------------------------------- | ------------------- | ---------- |
| 0001 | [Adotar arquitetura em camadas (Layered Architecture)](0001-adotar-arquitetura-em-camadas.md) | aceito - retroativo | 13-08-2026 |

## Regra de numeração

1. Reserve o próximo número de quatro dígitos nesta tabela **antes** de criar o arquivo.
2. Nunca renumere um ADR já criados. Em colisão, use sufixos como `0007-a` e `0007-b`.
3. Estado válido: `proposto`, `aceito`, `descontinuado` ou `substituído por <arquivo>`.
4. ADR retroativo registra a data comprovada da decisão;

## Quando criar um ADR

Escopo do processo de ADR
Os membros do projeto devem criar um ADR para cada decisão arquitetonicamente significativa que afete o projeto ou produto de software, incluindo o seguinte (Richards e Ford 2020):

1. Estrutura (por exemplo, padrões como microsserviços)
2. Non-functional requisitos (segurança, alta disponibilidade e tolerância a falhas)
3. Dependências (acoplamento de componentes)
4. Interfaces (APIs e contratos publicados)
5. Técnicas de construção (bibliotecas, estruturas, ferramentas e processos)
6. Requisitos funcionais e não funcionais são as entradas mais comuns para o processo de ADR.

## Template do ADR

```markdown
# Título

# Status

# Data

# Contexto

# Decisão

# Consequências

1. Positivas
2. Negativas

# Conformidade

# Observações

Autor:
Versão: 0.1
Changelog:
0.1: versão inicial proposta
```
