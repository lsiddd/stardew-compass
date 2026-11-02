# Correções de paridade com o jogo — 2026-11-02

As correções usam a DLL instalada, declarada como 1.6.15.24356, SHA-256
`f3e97f01d3fd2b1e6094fc8d2b59950aa6cb9d6cd1bf1b39d72d58edda8aad12`.
REA confirmou identidade e metadados (evidência
`ev_b5cbd27e66569d604f3672bb8c5f6b8f41196f0531d342ea7aa9a3f706b1b731`).
As regras foram inspecionadas com ILSpy; sementes foram executadas diretamente
pelos métodos `Utility.CreateRandomSeed` e `CreateRandom` do jogo em .NET 6 e 8.
Não foi iniciada uma partida nem modificado um save.

O número da versão não comprova que toda instalação tenha o mesmo código.
A regra de trem encontrada nesta DLL só é selecionada quando o hash consta
na proveniência dos dados exportados. Outros perfis preservam a regra histórica
com a limitação indicada no resultado. Patches de mods em execução não foram
capturados; as regras não prometem paridade com SMAPI/mods.

## Mudanças de resultado

| Área | Correção |
| --- | --- |
| Sementes | Conversão para `double` antes do resto, truncamento em direção a zero no modo legacy e divisão inteira nos pontos em que o C# a usa. Vetores de fronteira incluem IDs Int64 positivos e negativos. |
| Festival do Deserto | Duas operações de semente para o cacto; filtro de camisa/chapéu equipados antes de selecionar a roupa; ordem e gênero das peças da tabela exportada. |
| Estrela Invernal | Remoção do destinatário e dos NPCs divorciados antes do sorteio do doador. |
| Geodos | Overrides de Clint para o primeiro coco dourado e para artefatos antes de `artifactFound`; flags pendentes; quantidade de Qi Beans determinada pelo sorteio correto. |
| Caixas misteriosas | Requisito de nível de pesca 6; maestria de Agricultura; alternativas explícitas quando falta o nível salvo. |
| Prêmios | Cama de casal no sexto prêmio quando a casa está melhorada. |
| Guaxinins | Rejeição de matéria-prima repetida entre produtos; quarta recompensa com 5 Fairy Dust. |
| Lojas | Game ID no sorteio sincronizado de Krobus; garantia do repolho sem duplicação nem draws adicionais; ordenação estável quando prioridades aleatórias empatam. |
| Minas | Default/Remixed nos baús; identificação de recompensas originais; layouts alternativos após alcançar o fundo; visita à mina da pedreira; cenários de Monster Musk. |
| Calendário e eventos | Regra do trem por perfil; filtros e prioridade das lixeiras; neve; alternativas para clima/eventos dependentes da sessão; datas e flags dos eventos noturnos; restrições de borboleta e primeira visita ao cinema; pagamento do Calico Jack. |
| Bolhas/frenesi | Chance da praia, duração mínima, peixe capturado e data real; ocupação salva; linhas do tempo alternativas quando uma tentativa de frenesi pode falhar. |
| Artefatos | Sorte efetiva com amuleto, distinção entre host e jogadores online, escavação individual, acesso ao Festival do Deserto e substituição por Calico Eggs. |
| Mapas | Índices globais de tiles, distância até a borda e seis tiles `NoFishing`, com proveniência dos mapas inspecionados. |

## Estado e apresentação

As entradas incluem correio recebido/pendente, relações de divórcio, roupa,
maestria, nível de pesca, melhoria da casa, modo dos baús e flags globais.
Flags de host, jogador selecionado e qualquer jogador são tratadas conforme
os pontos de chamada inspecionados.

O exportador Python lê também `Shops`, `Characters`, `GarbageCans`,
`LocationContexts` e `MakeoverOutfits`. Os cinco resultados reais foram
comparados com o `ContentManager` original do MonoGame e coincidiram.
O manifesto verifica hashes das tabelas opcionais. A seleção de roupas usa
`MakeoverOutfits`; as demais regras continuam delimitadas às tabelas base
inspecionadas, sem um interpretador genérico de regras de mods.

Previsões futuras mantêm equipamentos e flags do snapshot, salvo alternativas
explicitamente indicadas. Cada linha de geodo é uma abertura hipotética em
Clint; não se atualizam flags pela abertura das linhas anteriores. Cada ponto
de artefato é a próxima escavação do host; não é uma rota sequencial.

Uma frenesia pode alterar a duração e todos os sorteios posteriores.
Por isso, o campo `scenario` identifica uma linha do tempo completa. Não se
podem juntar eventos de cenários distintos. Há um limite de 64 cenários:
quando a expansão ultrapassa esse limite, o cálculo informa indisponibilidade.
Sorte média de multiplayer requer conhecimento dos jogadores online; o domínio
aceita índices explícitos, mas a CLI não infere quem estava conectado.

Encantamentos oferecem cenários para ferramenta nova de irídio e previsões
por slot do inventário. Estas usam o nível, os encantamentos atuais e o histórico
ordenado salvo. Quando os dados necessários faltam, a saída não apresenta uma
seleção exata. Cada tentativa hipotética conserva esse histórico; não simula
reencantar a mesma ferramenta repetidamente. `fresh_enchantment` pertence ao
cenário genérico e não identifica o resultado da ferramenta equipada.

## Validação

Os fixtures históricos medem compatibilidade com preditores anteriores, não
com o jogo. Comparações demonstradamente inválidas foram retiradas da exigência
de igualdade, com motivos específicos; seus arquivos originais foram preservados.
Novos testes verificam os ramos corrigidos e vetores capturados da DLL. Nenhum
fixture antigo foi regravado automaticamente usando a nova implementação.

A suíte inclui testes de geodos, lojas, calendários, mapas, artefatos, sementes,
filtros de roupa, relações, manifesto e contratos públicos. A execução normal
não requer DLL do jogo, .NET, decompilador ou save pessoal. O relatório de execução
local fica em `outputs/game-audit/`, junto dos programas e evidências da auditoria.

Primeira verificação local: pacote wheel instalado fora do checkout em Python 3.11
e 3.13, com **2.835 testes e 2 subtestes aprovados em cada versão**. Há 916
comparações históricas desativadas com justificativa (842 de mapas/bolhas e 74
de previsões do relatório). Ruff, formatação, mypy e build passaram.

O Sunny da Primavera 11, Ano 2, gerou 27 seções de progresso, 22 de previsão,
694 registros de previsão, 27 eventos de bolhas e 11 pontos de artefatos, sem
diagnósticos de indisponibilidade. O JSON foi validado pelo schema público.
Os dois arquivos ficam em `outputs/sunny_390938626/report.txt` e `report.json`.
O hash do save original permaneceu
`7fef458a91961f40b630f3670ca2e6a5a4b477fa758a49a6dbc849500ebd0955`.

## Segunda passagem: próximas ações e cobertura real

A observação do usuário confirmou um erro na janela padrão: o Sunny tinha
467 aberturas e a saída começava em 461, devido ao arredondamento para o início
da página. Agora começa em **468 e termina em 487**, mesmo sem `--count`.
`openings_ahead: 1` identifica a próxima abertura; `sequence` é o número de
abertura, separado do ID do item. Mystery Boxes também incrementam o contador
de geodos em Clint, embora seu loot use `MysteryBoxesOpened`.

Todos os contadores passam a começar no valor salvo + 1. Calendários mostram
o dia salvo em diante; festivais anuais usam a próxima edição ainda não encerrada.
Uma consulta com `--start` explícito continua podendo recuperar o histórico.

Nesta passagem foram comparados **240 resultados da função original
`Utility.getTreasureFromGeode`**, em .NET 6: 20 posições, seis recipientes e
dois modos de RNG. IDs e quantidades coincidiram. O fixture
`tests/fixtures/game-geode-results.json` identifica a DLL, Objects.xnb e os
parâmetros completos. Isso cobre as condições capturadas, sem afirmar uma
prova de todas as combinações possíveis ou uma sequência inteira de gameplay.
Encantamentos acrescentam 54 observações dos métodos originais de pool/RNG;
contextos de artefatos acrescentam 80 mapas e um limiar de `RANDOM` observado.

Também foram corrigidos nível/histórico de encantamentos, estação/entregas do
pedido ativo dos guaxinins, contexto de verão do deserto, classificação de
Caldera, precisão float32 de `RANDOM`, prioridades de eventos noturnos, clima de
Trout Derby/SquidFest, condições dos catálogos e acesso a papel de parede.
Um roundtrip com o `XmlSerializer` original confirmou listas vazias omitidas
e elementos repetidos nas ferramentas; o parser agora lê esse formato e o
wrapper legado. Quatro vetores adicionais da DLL protegem a divisão inteira
na semente das lixeiras. Sementes sazonais dependentes da sessão passam a
ter alternativas estruturadas; IDs de chapéus e plantas dos prêmios são explícitos.
Os documentos de calendário e mapas detalham seus contraexemplos e limites.

A matriz completa das 22 seções e dos dois módulos de mapa, com a forma de
validação e limitações de cada um, fica em
`outputs/game-audit/second-verification.txt`. Ela distingue inspeção de código,
testes do preditor e execução dos métodos originais. Nenhum desses resultados
equivale a observar todas as ações de uma partida completa.

Validação final da segunda passagem: wheel instalado fora do checkout em
**Python 3.11 e 3.13**, com **3.087 testes e 2 subtestes aprovados em cada
versão**, além dos 916 skips históricos justificados. Ruff, formatação, mypy
configurado, build e diff-check passaram. O Sunny final contém 857 registros de
previsão, 27 eventos de bolhas e 11 manchas, sem indisponibilidade; JSON validado
no schema. O texto tem 2.569 linhas. Os arquivos `report.txt` e `report.json`
foram atualizados e o hash do save original permaneceu igual.

A documentação complementar de loot e serialização é
[loot-snapshot-parity.md](loot-snapshot-parity.md). A integração com o Sunny
confirma as próximas aberturas 468–487, Hoe → Archaeologist e Gold Watering Can
→ Bottomless sob o estado salvo. O oráculo de geodos e os testes não alteram
as premissas explícitas de sorte e estado futuro do relatório.
