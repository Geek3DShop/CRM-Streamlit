# Adotar arquitetura em camadas (Layered Architecture)

# Status

Aceito - retroativo

# Data

13-08-2026

# Contexto

O projeto GEEK3d consiste em uma aplicação CRM simples para gerenciamento de clientes e vendas relacionados a um negócio de impressão 3D.

A aplicação utiliza Streamlit como camada de interface e Pandas para manipulação e análise dos dados. À medida que o sistema evolui, torna-se necessário organizar o código de forma que a interface e as regras de negócio não fiquem diretamente acoplados.

A ausência dessa separação poderia aumentar o acoplamento entre componentes, dificultar a manutenção, tornar os testes mais complexos e dificultar futuras alterações na tecnologia utilizada para persistência, interface ou análise dos dados.

A estrutura proposta anteriormente para o projeto já apresenta uma separação entre `pages`, `services` e `tests`, caracterizando uma organização baseada em responsabilidades distintas.

# Decisão

Adotar Arquitetura em Camadas (Layered Architecture) como modelo arquitetural principal do GEEK3d, com uma organização simples e orientada às responsabilidades reais do sistema.

A estrutura atual será organizada conceitualmente nas seguintes áreas:

```text
pages/
    Camada de apresentação.
    Responsável pela interface e interação com o usuário utilizando Streamlit.

services/
    Camada de serviços
    Responsável pelas operações e regras de negócio da aplicação.

data/
    Camada de contrato de dados
    Define o padrão estrutural esperado para o arquivo Excel.

tests/
    Camada de testes
    Contém os testes automatizados das regras e funcionalidades da aplicação.
```

Os serviços deverão ser organizados por responsabilidade funcional. A estrutura inicial poderá utilizar arquivos simples:

```text
services/
    calculator.py
    auth.py
```

Caso algum serviço cresça em complexidade, ele poderá posteriormente ser transformado em um módulo próprio:

```text
services/
    calculator/
        cost.py
        pricing.py
        profit.py
```

A comunicação entre as camadas deverá ocorrer de maneira organizada, evitando que a camada de apresentação acesse diretamente mecanismos de persistência ou implemente regras de negócio que pertençam a outras camadas.

A arquitetura deverá permanecer simples e proporcional ao tamanho e à complexidade do projeto. A adoção de camadas não implica a utilização de padrões ou tecnologias adicionais sem necessidade.

A decisão é registrada retroativamente em razão de a estrutura arquitetural já ter sido definida e adotada antes da formalização deste ADR.

# Consequências

## 1. Positivas

1. **Separação de responsabilidades:** cada parte do sistema possui uma responsabilidade principal bem definida.

2. **Maior manutenibilidade:** alterações em uma camada tendem a exigir menos modificações nas demais.

3. **Menor acoplamento:** a interface não precisa conhecer diretamente os detalhes de persistência ou das regras internas do sistema.

4. **Facilidade de testes:** regras de negócio e cálculos podem ser testados independentemente da interface do Streamlit.

5. **Facilidade de evolução:** a arquitetura permite substituir ou modificar componentes específicos com menor impacto no restante do sistema.

6. **Preparação para crescimento:** a estrutura permite incorporar novas funcionalidades, como análises de clientes e recomendações baseadas em dados, sem concentrar toda a lógica na interface.

7. **Organização do projeto:** a estrutura de diretórios torna mais explícito onde cada tipo de código deve ser implementado.

## 2. Negativas

1. **Responsabilidade arquitetural sobre os serviços:** à medida que o projeto crescer, será necessário evitar que os arquivos de services/ se tornem excessivamente grandes.

2. **Evolução da estrutura:** a simplicidade atual poderá exigir novas camadas ou abstrações no futuro.

3. **Dependência do Excel:** enquanto o Excel for a fonte de dados principal, limitações desse formato poderão influenciar a arquitetura e o desempenho da aplicação.

4. **Possível necessidade de abstrações futuras:** caso o domínio se torne mais complexo, poderá ser necessário introduzir modelos, interfaces, enums ou uma camada específica de persistência.

## Conformidade

Novas funcionalidades devem respeitar a separação de responsabilidades definida nesta decisão.

Os arquivos em pages/ devem concentrar a apresentação e a interação com o usuário. Regras de negócio e operações do sistema devem ser delegadas aos serviços apropriados.

Os arquivos em services/ devem concentrar as regras e operações relacionadas às funcionalidades do sistema, incluindo autenticação, clientes, vendas e cálculos.

A manipulação dos dados persistidos deve respeitar a estrutura
definida para o padrão do Excel, evitando que cada página ou
serviço implemente mecanismos próprios e inconsistentes de
leitura ou gravação dos dados.

Novas pastas ou camadas somente devem ser introduzidas quando houver uma necessidade concreta de separação de responsabilidades, aumento de complexidade ou requisito arquitetural que justifique a abstração.

Alterações significativas nesta decisão deverão ser registradas em um novo ADR, preservando o histórico desta decisão.

# Observações

Autor: Fernando Chaves e Gustavo Ferreira </br>
Versão: 0.1 </br>
Changelog: </br>
0.1: versão inicial proposta e registrada retroativamente.
