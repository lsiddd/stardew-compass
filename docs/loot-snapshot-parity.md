# Segunda revisão de loot e lojas — 2026-11-02

Referência: Stardew Valley 1.6.15.24356 instalado, DLL SHA-256
`f3e97f01d3fd2b1e6094fc8d2b59950aa6cb9d6cd1bf1b39d72d58edda8aad12`.
Os caminhos C# abaixo se referem à descompilação ILSpy preservada em
`outputs/game-audit/decompiled/`. Inspeção estática e testes Python não são
execução do jogo. Nenhuma partida foi iniciada, e o save não foi alterado.

| Previsão | Fonte do jogo e verificação | Resultado e limite |
| --- | --- | --- |
| Mystery Boxes | `Utility.cs:6616–6765`; incremento em `GeodeMenu.cs:251–255`; regressões de Fishing, mastery e sementes sazonais | A próxima abertura usa contador salvo +1. As três colunas são cenários de tipo/mastery. Seasonal Seeds expõe os IDs possíveis e dependência de `Game1.random`; a ordem futura mantém `GotMysteryBook` do snapshot, explicitamente. Sem oráculo runtime de Mystery Boxes nesta revisão. |
| Encantamentos | `BaseEnchantment.cs:126–168`, `ReachingToolEnchantment.cs:12–18`, `Tool.cs:1435–1441`; 54 casos capturados dos métodos reais | Pools e resultados coincidem para Hoe, WateringCan e Pan, níveis 0/3/4, três históricos e dois modos RNG. Linhas por slot usam nível, encantamentos atuais e histórico ordenado. Os outros quatro tipos mantêm verificação estática das regras. Não foi executada uma animação de forja. |
| Prize Tickets | `PrizeTicketMenu.cs:40–43,64–131,185`; inspeção dos 22 prêmios iniciais e ciclo de nove, testes de casa/data/IDs | O próximo nível é o contador antes de entregar o prêmio; ordinal público é contador +1. Hats e plantas conservam IDs qualificados. Sementes assumem recebimento na data salva; data ausente produz quatro cenários. Sem execução runtime do menu. |
| Guaxinins | `Raccoon.cs:71–142,149–247,254–355`; regressões de estação fixa, entrega, cooldown e pools ponderados | Pedido atual respeita `seasonOfCurrentRaccoonBundle` e slots entregues; ativação após dia 21 usa a próxima estação. Espera de sete dias usa a data absoluta salva. Pedidos futuros e sementes de recompensa continuam condicionais. O item não enviado também depende do cache da sessão. Sem runtime do menu de bundles. |
| Carrinho | `Shops.json`, loja `Traveler`; `ShopBuilder` e `ItemQueryResolver`; regressões de deduplicação, empate de prioridades e revisões de flags/calendário | Ordem, preços e garantia foram comparados estaticamente com os dados instalados. Janela padrão é futura, conforme o orquestrador. Disponibilidade futura depende da progressão salva. Não foi executada uma loja no jogo nesta revisão. |
| Krobus | `Shops.json`, `ShadowShop`; `Utility` para `SYNCED_RANDOM`; três vetores de pão e seed negativa | Inclui game ID no sorteio do pão e divisão inteira no RNG diário. O catálogo calculado é a seleção aleatória; não simula compras anteriores naquele dia. Sem runtime da loja. |
| Sandy | `Shops.json`, `Sandy`; `ItemQueryResolver.RANDOM_ITEMS`; testes de empate e IDs de camisa | Ordem estável e filtro de venda da tabela instalada. Acesso à loja e alterações de mods não são reconstruídos por esse seletor. Sem runtime da loja. |
| Wallpaper/Flooring | `Shops.json`, `SeedShop`/`Joja`; tipo de item e seletor; regressões de calendário e disponibilidade | Sorteio de textura verificado estaticamente, com empates preservados. As revisões do orquestrador e do builder aplicam a janela e os estados de abertura. Sem runtime da loja. |
| Bookseller | `Shops.json`, `Bookseller`; revisão anterior de sorteios/datas e testes de datas/preços/seed negativa | Continua coberto por inspeção estática e regressões; esta segunda revisão não executou o Bookseller original nem ampliou seu escopo. |

## Erros corrigidos nesta revisão

`Reaching` só participa do pool de Hoe, WateringCan e Pan no nível irídio.
No Sunny, a primeira rolagem é `0.32247487144659964`: a enxada básica recebe
Archaeologist e o regador de ouro recebe Bottomless. Antes, o pool sempre
incluía Reaching e informava Generous/Reaching. Isso foi confirmado executando
`BaseEnchantment.GetAvailableEnchantmentsForItem` e `Utility.CreateRandom`
originais em objetos de ferramenta criados em memória.

O novo helper `loot/tool_state.py` lê os dados já disponíveis no snapshot,
incluindo os nomes internos `Expansive` e `Auto-Hook` e a ordem de
`previousEnchantments`. Um roundtrip com o `XmlSerializer` e tipos originais
confirmou que listas vazias são omitidas e que listas preenchidas usam elementos
repetidos. O loader aceita esse formato e os wrappers das fixtures anteriores.
Ausência dessas listas significa histórico vazio; nível necessário ausente ou
marcação explícita de histórico nulo não produz um encantamento exato.
As linhas genéricas continuam disponíveis e indicam
explicitamente uma ferramenta nova de irídio, sem histórico. Linhas de slots
reais são hipóteses independentes com o estado salvo: não simulam reencantar
a mesma ferramenta sucessivamente.

Guaxinins agora distinguem pedido atual, futuro, passado, espera e ativação
na data salva. Uma estação já fixada não muda com a estação atual; um pedido
ainda não ativado só usa a estação calculada sob a condição de ativação hoje.
Ingredientes já entregues não reaparecem como pendências. As sementes de
recompensa dependem da data de recebimento, não da estação fixada do pedido.

`Crop.getRandomLowGradeCropForThisSeason` usa o RNG da sessão. Por isso, caixas
com Seasonal Seeds apresentam quatro opções na Primavera/Verão/Outono e a
união de onze IDs no Inverno, sem eleger uma delas como certeza.
`Utility.getRaccoonSeedForCurrentTimeOfYear` muda de semente após Primavera23
ou dia20 nas demais estações. Mystery Boxes e Prize Tickets indicam a hipótese
de recebimento na data salva; recompensas de pedidos futuros preservam os
quatro intervalos possíveis. Ganhar o primeiro Book of Mysteries muda uma flag
durante a sessão, e as próximas linhas deixam explícito que não simulam essa
aquisição intermediária.

## Reproduções e validação

- `outputs/game-audit/loot-enchant-probe/Program.cs`: chamada dos métodos reais,
  sem carregar save ou iniciar jogo gráfico.
- `tests/fixtures/game-enchantment-rules.json`: 54 casos sintéticos capturados
  dessa execução em .NET 6, com hash e origem; não foram gerados por Python.
- `tests/fixtures/game-tool-serialization.json`: XML e estado restaurado de
  ferramentas vazias e encantadas, capturados com os tipos originais. Os testes
  verificam também o pool e o resultado após esse roundtrip.
- `tests/unit/test_loot_game_rules.py`: comparação dos pools e resultados do
  oráculo, regressões das novas condições e os testes anteriores preservados.
- `tests/unit/test_report_predictions.py`: igualdade histórica apenas nos
  cenários válidos; metadados novos são projetados fora da captura antiga.

Validação conjunta local desses dois arquivos: **277 testes aprovados e
74 comparações históricas justificadamente desativadas**. Ruff e o comando
mypy configurado do projeto passaram. A matriz delimita a evidência disponível;
não afirma cobertura runtime de todas as lojas, branches ou versões anteriores.
