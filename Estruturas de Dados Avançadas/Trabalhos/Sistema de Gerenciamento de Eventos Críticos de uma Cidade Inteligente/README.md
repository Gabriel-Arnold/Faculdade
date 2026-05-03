# Sistema de Gerenciamento de Eventos Críticos de uma Cidade Inteligente

Projeto acadêmico em linguagem C que implementa um sistema textual para registrar, consultar, atualizar, priorizar e remover eventos críticos urbanos usando uma **Árvore AVL** como estrutura principal.

## Descrição geral

Cada nó da árvore representa um evento crítico de uma cidade inteligente. A chave primária de ordenação é o **ID do evento**.

Cada evento possui:

- ID do evento
- Tipo do evento
- Nível de severidade de 1 a 5
- Data e hora do registro
- Região da cidade
- Status: Ativo ou Resolvido
- Altura do nó
- Ponteiros esquerdo e direito

A Árvore AVL garante que a árvore permaneça balanceada após inserções e remoções, mantendo operações de busca, inserção e remoção com boa eficiência.

## Funcionalidades implementadas

### Gerenciamento da AVL

- Inserção de eventos por ID
- Cálculo do fator de balanceamento
- Rotações simples e duplas
- Remoção de eventos, permitida apenas para eventos com status `Resolvido`
- Rebalanceamento obrigatório após remoção
- Busca de evento por ID

### Consultas avançadas

- Listagem de eventos ativos por intervalo de severidade
- Relatório de eventos ativos por região
- Busca por intervalo de ID
- Listagem geral em ordem crescente de ID

### Atualizações

- Alteração de status de `Ativo` para `Resolvido`
- Atualização de severidade apenas para eventos ativos

### Métricas

- Altura total da árvore
- Número total de nós
- Número de eventos ativos
- Fator de balanceamento médio absoluto
- Quantidade total de rotações realizadas desde o início da execução
