# Paridade de calendário e eventos

As correções de calendário foram verificadas contra métodos e tabelas da DLL
instalada, que declara Stardew Valley 1.6.15, build 24356. Elas complementam
[as correções gerais](game-parity-corrections.md). Os testes novos ficam em
`tests/unit/test_calendar_game_rules.py`; os testes históricos continuam úteis
para os cenários que não foram invalidados por evidência do jogo.

## Evidência e alcance

- SHA-256 da DLL: `f3e97f01d3fd2b1e6094fc8d2b59950aa6cb9d6cd1bf1b39d72d58edda8aad12`.
- MVID: `46c95350-5805-4442-8e93-61092d55e101`.
- Identidade REA: `ev_b5cbd27e66569d604f3672bb8c5f6b8f41196f0531d342ea7aa9a3f706b1b731`.
- Métodos inspecionados com ILSpy 9.1.0.7988; o método do trem também foi
  conferido diretamente em CIL. As tabelas GarbageCans, LocationContexts e
  PassiveFestivals foram conferidas contra exportação pelo ContentManager.
- Os artefatos locais da investigação estão em `outputs/game-audit/`, incluindo
  `calendar-findings.txt`, `calendar-probes.json` e `calendar-railroad.il`.
  Eles não são necessários para executar os testes de regressão.

A identidade REA identifica a instalação; ela não certifica uma distribuição
oficial sem alterações. A descompilação e os probes de RNG não são execução de
uma sessão completa do jogo. Não houve observação de runtime SMAPI nem dos
patches carregados pelos mods. Por esse motivo, a alteração específica de trem
fica vinculada ao perfil dessa DLL, e resultados que dependem de sessão ou
progressão futura continuam explicitamente condicionais.

## Regras corrigidas

| Módulo | Correção | Resultado e limites |
| --- | --- | --- |
| `mine_chests` | Separa Default da seleção Remixed; conserva conversão de `gameID` para double antes de multiplicar por 512; anéis usam qualificador `(O)`. | Sem modo salvo, devolve alternativas nomeadas. A seção mostra recompensa original e informa a condição de ainda não ter sido coletada; não presume baú restante. |
| `trains` | No perfil identificado, compara os sorteios de dois dias, aplica a chance derivada de 0.09, horário 09:00 e acesso a partir do dia 32. Suprime festivais. | Sem perfil compatível, mantém o algoritmo histórico com `verification=unverified_historical_rule`. A versão textual do save não seleciona a regra instalada. |
| `weather` | Inclui neve de inverno, modificações de calendário e alternativas dos subtipos de clima que usam RNG da sessão. | Chuva/tempestade e sol/vento permanecem alternativas quando falta o estado de sessão. O clima atual salvo é fato; `weatherForTomorrow` ainda recebe modificações obrigatórias na virada do dia. |
| `trash` | Corrige o gate de Qi Bean e os draws de curto-circuito; separa flags Host/Any das flags do jogador; aplica chances float32; completa pool sazonal e lixeira do Desert Festival. | Registros por jogador são alternativas para quem procurar primeiro numa lixeira compartilhada. Sorte, contadores, progresso e ausência de modificações nas tabelas são condições do cenário. |
| `mines` | Calcula o mapa alternativo antes do tipo de andar; usa mínimo global/da missão; exige visita à mina da pedreira; representa Monster Musk. | Cavernas pré-históricas são candidatas, pois mapa/tesouro dependem da geração da sessão. Cogumelos exigem primeira geração diária e não aparecem quando o andar virou pedreira. |
| `night` | Usa a data de despertar; aplica casamento, eventos pendentes, Qi Plane, árvore do guaxinim, Fairy Rose e Got_Capsule na ordem apropriada. | Eventos são candidatos condicionais: seleção não garante alvo válido, espaço ou prioridade sobre acontecimentos futuros. Ausência de Fairy Rose em runtime gera os dois cenários. |
| `statues` | Festivais e chuva excluem Butterfly; publica bênção efetiva e condições do clima. | Coordenadas continuam candidatas, exigindo mapa compatível, tile livre e visita antes das 17h. |
| `crane` | Primeira visita ocupa a garra, independentemente do sorteio; exige cinema construído e apresenta condição de visita/filme. | O sorteio de disponibilidade continua projetável antes da construção, com essa condição explícita. |
| `calico_jack` | Separa simulação e conselho; publica ação, hits, totais, resultado e multiplicador de super bust. Chance é calculada por previsão, sem estado residual. | O plano assume os mesmos parâmetros de sorte e a mesma sequência de jogos. Estratégias não foram provadas exaustivamente para todas as combinações. |
| `gem_birds` | Nenhuma mudança de regra necessária. | Ordem, seed e shuffle conferem com os métodos inspecionados; isso não certifica alterações por mods. |

Os mapas alternativos das minas são ativados a partir de 1.6.4, conforme as
[notas oficiais dessa versão](https://www.stardewvalley.net/stardew-valley-1-6-4-full-patch-notes/).
A regra detalhada foi conferida na DLL 1.6.15 instalada. Caminhos históricos
anteriores continuam separados; esta investigação não certifica todas as
revisões intermediárias do jogo.

## Exemplos de regressão

Os exemplos usam seed `390938626`, versão `1.6.15`, RNG não legado e progresso
explícito no contexto de teste, salvo indicação diferente. Dias são contados
com Primavera 1 do ano 1 igual a 1. Os vetores não dependem do arquivo pessoal
do save.

- Baús Default: andares 10/20/50/90/110 dão Leather Boots, Steel Smallsword,
  Tundra Boots, Obsidian Edge e Space Boots. Para Remixed, seeds 6 e 10 no
  andar 20 produzem respectivamente `(O)517` e `(O)519`.
- Trem no perfil instalado: dia 124 às 09:00; no cenário histórico sem
  verificação, 13:20. O dia 136 não admite trem por ser festival.
- Clima: dia 198 tem Snow; dia 126 tem alternativas Rain/Storm. Dia 41
  (Verão 13) recebe Storm mesmo se o valor bruto salvo para amanhã for Sun.
- Minas: dia 119/andar 78 usa mapa 58 e pode ser infestado; dia 130/andar 7
  usa mapa 60 e não pode. Dia 127/andar 106 perde cogumelos quando a
  classificação de pedreira se aplica.
- Noite: seed 104, dia 28, não admite Fairy porque o despertar é dia 1 de
  verão. Got_Capsule bloqueia a cápsula candidata do dia 144. Seed 42,
  dia 123, distingue Fairy de ausência de evento conforme Fairy Rose.
- Lixo: com missão Qi ativa, dia 123 na lixeira EmilyAndHaley falha o
  sorteio-base e não pode produzir Qi Bean. A lixeira do Desert Festival
  existe já no ano 1 se o ônibus foi reparado; com 100 lixeiras verificadas,
  sorte -0.075 e missão Qi inativa, dia 127 dá oito Calico Eggs.
- Estátua: dia 92 é festival; a bênção aplicável é Fangs, sem candidatos
  de Butterfly.
- Garra: a primeira visita no dia 123 continua ocupada apesar do sorteio
  normalmente favorável.
- Calico Jack: dia 123, jogo 154, ficar em 12 vence com multiplicador 3.
  A mesma previsão calculada sozinha ou dentro de um lote deve coincidir.

## Contratos de entrada e saída

`calendar_rules.py` centraliza partes do calendário e CreateDaySaveRandom,
respeitando a divisão inteira de `uniqueIDForThisGame` antes dos doubles.
As datas efetivas incluem `dayAdjust`. Novos campos de entrada vêm do parser
compartilhado de saves; quando um fato depende de runtime ou está ausente,
o módulo não o transforma silenciosamente em fato observado.

Campos relevantes incluem `game_profile`, `shuffleMineChests`,
`lowestMineLevel`, `lowestMineLevelForOrder`, `quarryMineVisited`,
`anyOnlineFarmerHasMonsterMusk`, `hostTheaterUnlocked`, `hostDesertUnlocked`,
`anyCcComplete`, `anyDesertUnlocked`, `timesReachedMineBottom`,
`hasQuartzGlobeRecipe`, `weatherOverrides`, `weddingDays`, `pendingNightEvents`,
`gotCapsule`, `raccoonTreeFallen`, `sawQiPlane`,
`gotFirstBillboardPrizeTicketAny`, `hasMatureFairyRoseTonight`,
`theaterDayFirstEntered` e `theaterBuilt`.

As saídas mantêm os campos anteriores quando ainda descrevem um cenário
válido e adicionam condições de uso:

- `verification`/`ruleProfile` distinguem perfil do trem e fallback histórico.
- `weatherAlternatives`, `source` e `certainty` separam fato salvo, calendário,
  cálculo por seed e subtipo dependente de sessão.
- `rewardMode`, `rewardAlternatives` e `availabilityCondition` explicam baús.
- `alternateLayouts`, `monsterMuskAlternative` e `dinoLevelConditions`
  explicam cenários das minas. A alternativa com Musk inclui sua própria
  lista de cogumelos quando a classificação de pedreira muda.
- `eventCandidates`, `wakingDay` e `conditions` qualificam eventos noturnos.
- `availability`/`availabilityIfBuilt` qualificam a garra.
- `plan` contém a ação e o resultado econômico de Calico Jack.

A implementação corresponde às tabelas verificadas, sem implementar um
interpretador universal de GameStateQuery ou de mods. As condições de
calendário fixas não substituem a leitura de novas tabelas quando a versão
suportada mudar. Mudanças futuras devem ter novos vetores derivados do jogo,
sem atualizar snapshots históricos apenas para aceitar o resultado novo.

## Validação

```sh
uv run --no-sync pytest -q tests/unit/test_calendar_game_rules.py
```

São 69 testes focados, cobrindo as regressões acima, prioridades, informações
faltantes, offset de dias, divisão inteira negativa contra vetores da DLL, escopos multiplayer e preservação de quantidade e
localização na conversão para registros públicos. A suíte histórica aplica
projeções apenas a metadados novos e documenta os cenários invalidados em
`tests/fixtures/README.md`.


## Segunda revisão: próximas previsões e disponibilidade

A segunda revisão atravessou também o parser, planejamento de janelas e
conversão pública. Corrigiu os seguintes pontos, além das regras individuais:

- O padrão das seções diárias começa no dia salvo, inclusive no último dia
  do mês. Lojas semanais cobrem sete dias e calendário mensal cobre 28;
  `start` explícito continua permitindo consulta histórica.
- Winter Star e Desert Festival usam a próxima edição ainda não encerrada.
  No dia 16 ou 17 da primavera, registros dos dias anteriores do festival
  são omitidos; o resumo anual do cactus continua visível. `count` sozinho
  conserva esse início e conta edições anuais.
- Reparos noturnos usam `mailForTomorrow`, sem reutilizar cartas já entregues
  em `mailbox`. As três peças do barco, a ativação do papagaio e a abertura
  do Joja abandonado em manhã chuvosa agora respeitam suas prioridades.
- Trout Derby e SquidFest não forçam Sun: suas entradas em PassiveFestivals
  não substituem mapas. Entre os festivais passivos verificados, apenas
  Night Market substitui um mapa no contexto do vale e força tempo limpo.
- Desert Festival sem acesso salvo ao deserto é apresentado como cenário
  condicionado à reparação do ônibus, incluindo vendedores, roupas e cactus.

A tabela abaixo registra cobertura, não uma certificação de gameplay completo.
Os artefatos complementares são `outputs/game-audit/calendar-second-findings.txt`
e `calendar-second-probes.json`.

| Features | Evidência adicional | Limite remanescente |
| --- | --- | --- |
| minas, trem, clima, lixo, noite, garra, estátuas | API pública sem opções e fronteiras de mês; comparação com métodos já auditados | Estado de sessão e evolução entre dias não são reconstruídos; consultar condições dos registros. |
| cart | Shops/Traveler, GSQ de rotas CC/Joja, Forest e calendário de festivais | Estoque projetado não garante acesso no horário, saldo, estoque restante ou regras alteradas por mods. |
| Krobus, Sandy | Faixas e RNG dos itens variáveis em Shops; nova janela a partir de hoje | São previsões de estoque variável, não inventários integrais das lojas; acesso individual e estoque restante exigem estado adicional. |
| wallpaper | lockedDoorWarp, AreStoresClosedForFestival e evento de qualquer jogador | Acesso com Key To The Town continua condicionado ao atendimento de Pierre. |
| Bookseller | Utility.getDaysOfBooksellerThisSeason e slots aleatórios em Shops | Lista os slots variáveis verificados, sem alegar cobertura de todas as compras permanentes ou já esgotadas. |
| Winter Star | Seleção já auditada e próxima edição anual | Progresso, divórcios e NPCs futuros podem mudar a lista; presentes permanecem alternativas. |
| Desert Festival | SetupFestivalDay, PassiveFestivals, acesso e próxima edição anual | Agenda/NPCs/equipamento usam snapshot; atendimento e makeover exigem espaço e disponibilidade. Cactus descreve aparência anual, sem provar que ainda pode ser coletado. |
| Calico Jack | Constructor e Club.timesPlayedCalicoJack | Contador é de sessão e reinicia ao retornar ao título, não a cada dia; o padrão jogo 1 pressupõe nova sessão, e a API aceita game_start explícito. |
| minechest, gembirds | Recompensas originais e identidade fixa do puzzle | Não são sequências de próximas ações. Coleta anterior de baú ou resolução do puzzle não altera o resultado original exibido. |

A integração final acrescentou quatro vetores numéricos capturados da DLL
para a semente das lixeiras (`game-trash-seeds.json`). `CreateDaySaveRandom`
divide o game ID como inteiro antes de criar o double; um ID pequeno ímpar em
legacy com soma final negativa e um ID acima de 2^53 detectam diferenças que
não aparecem no Sunny, cujo ID é par. O gerador das lixeiras usa essa mesma
ordem de operações.
