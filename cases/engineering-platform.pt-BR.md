# Engineering Platform: representar trabalho privado sem falsificá-lo

<p align="right"><sub><a href="engineering-platform.en.md">English</a></sub></p>
## Contexto

A maior parte da minha engenharia acontece em repositórios privados do Azure DevOps. Um perfil do GitHub mostra apenas o que o GitHub enxerga, então esses commits, pull requests e revisões ficavam invisíveis ali. Copiar código, reescrever histórico ou trocar a autoria de commits distorceria o trabalho.

## Desafio

Representar a atividade de engenharia entre provedores de forma que:

- todo número possa ser rastreado até um commit real;
- nada seja reescrito, ter a autoria trocada ou ser atribuído à pessoa errada;
- nenhum código, segredo ou nome confidencial chegue a uma superfície pública;
- o sistema rode sem supervisão e avise quando não tiver certeza.

## Meu papel

Desenho e implementação da plataforma de ponta a ponta: inventário, validação de segurança, espelhamento, métricas, agregação pública, modelo de autorização e runbook de operação.

## Arquitetura

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/cases/engineering-platform-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="../assets/cases/engineering-platform-light.svg">
  <img alt="Engineering platform pipeline from Azure DevOps through inventory, security gate, private mirror, collector and public JSON to the profile, with cross-cutting controls." src="../assets/cases/engineering-platform-dark.svg" width="100%">
</picture>


```
Azure DevOps
  → inventário histórico (DAG do Git + REST, recuperação por id)
  → validação de segurança (varredura de segredos, política de caminhos sensíveis, fail-closed)
  → espelho privado de mão única (somente fast-forward)
  → coletor de métricas (deduplicação por SHA)
  → agregação pública (schema estrito, apenas agregados)
  → perfil do GitHub
```

**Inventário histórico.** Dois métodos independentes. O primeiro percorre o grafo de commits do Git em todas as refs anunciadas e busca por id os commits que o Azure DevOps ainda referencia, mas que nenhuma ref contém, recuperando trabalho de branches apagadas. O segundo lê a API REST: refs, a listagem de commits sem filtro e todos os pull requests com seus commits. Como o comportamento da listagem sem filtro não é documentado, ela foi conferida contra o grafo; os conjuntos ficaram idênticos após uma correção na recuperação por id.

**Validação de segurança.** Todo intervalo proposto para transferência passa pelo conjunto completo de regras padrão de varredura de segredos e por uma política de caminhos sensíveis. Exceções são registros por fingerprint exato, com classificação, justificativa, evidência e revisores, além de uma única regra restrita e revisada. A configuração do scanner é fixada por hash: qualquer edição bloqueia o espelhamento até nova aprovação, e um validador rejeita configurações que desativem regras ou usem allowlists globais ou sem âncora. Testes canário confirmam que segredos realistas continuam sendo detectados. Uma credencial real é rotacionada antes, ou o repositório não é espelhado.

**Espelho privado.** O Azure DevOps continua sendo a fonte da verdade. Um repositório só é espelhado a partir de uma allowlist explícita que registra categoria de autorização, aprovador, data e fundamento; código corporativo ou de terceiros sem autorização de redistribuição nunca é espelhado, e casos indefinidos ficam bloqueados. Cada push é um único refspec explícito em fast-forward: sem force, sem prune, sem reescrita. A privacidade do destino é reconferida logo antes de cada push e o resultado é verificado depois. SHAs, autores e datas são preservados; reexecuções são idempotentes.

**Coletor de métricas.** Commits de todas as plataformas são deduplicados por SHA e reportados como medidas separadas, com significados distintos: atividade de engenharia, onde o trabalho vive, fontes, entrega e contribuições oficiais do GitHub. O total do calendário oficial nunca é somado à atividade de engenharia, e commits de terceiros mantêm seus autores e nunca contam como meus.

**Agregação pública.** O arquivo público é montado campo a campo e validado contra um schema estrito que falha fechado diante de chaves, strings ou faixas desconhecidas. Só agregados são publicados. Um validador do repositório público bloqueia nomes confidenciais comparando hashes truncados, de modo que a própria lista de bloqueio nunca é publicada.

## Controles transversais

- **Tokens de menor privilégio por job.** Cada job recebe seu próprio token granular, com validade limitada e restrito ao que precisa. Tokens nunca aparecem em URLs, argumentos, configuração ou logs, e todo registro de log passa por redação.
- **Health checks e alertas.** Cada espelho é classificado (sincronizado, pendente, defasado, divergente, ausente, não privado). Qualquer problema abre ou atualiza um alerta privado; só uma execução saudável o fecha. Verificações inconclusivas nunca fecham alertas.
- **Agendamento consciente de custo.** A reconciliação roda em intervalo fixo, com timeouts por job que limitam o pior caso de uso de runners e kill switches separados para espelhamento e métricas. Código privado é clonado do zero a cada execução, sem cache compartilhado.
- **Revisão independente.** As exceções da varredura de segredos são registradas uma a uma, com justificativa, e revisadas de forma independente antes de valer; a configuração do scanner é fixada por hash, então qualquer mudança nela é explícita.

## Decisões e trade-offs

- **Representação acima de aparência.** Com squash merges, commits de feature branches nunca chegam à branch padrão e, portanto, não podem aparecer no calendário do GitHub. Eles são contados no dashboard, separados das contribuições oficiais.
- **Sem reescrita de histórico.** Reescrever mudaria todos os SHAs. O custo: um achado bloqueia o repositório até a triagem.
- **Destino privado não é autorização.** Espelhar em privado não substitui a permissão do dono do código.
- **Falhar fechado.** Falta de autorização, destino não privado, divergência, bloqueio do scanner ou campo público desconhecido interrompem o pipeline em vez de degradá-lo.

## Resultados

- **3.414** commits inventariados, **0** irrecuperáveis.
- **Mais de 4.300** commits únicos atribuídos às minhas identidades Git, consolidados entre plataformas (todo o histórico até outubro de 2026, deduplicados por SHA; o número vivo está no dashboard).
- Os commits elegíveis na branch padrão para contribuições oficiais do GitHub, e quantos o calendário ainda não mostra, estão no dashboard.
- **Mais de 150** testes automatizados.

## Status atual e estado residual

- Os repositórios aprovados estão espelhados, e seus conjuntos de commits são verificados contra o Azure DevOps por SHA, com as exclusões de política aplicadas.
- Regras de repositório nos espelhos permitem apenas as atualizações fast-forward do próprio espelho; automações de terceiros não conseguem criar branches nem pull requests ali, e qualquer tentativa é monitorada.
- O calendário oficial é comparado dia a dia com os commits elegíveis: o dashboard mostra o máximo que ele pode estar exibindo e quantos ele comprovadamente ainda não exibe. A diferença é reportada, não arredondada.

## Lições aprendidas

- Dois métodos independentes de inventário valeram o esforço extra: só coincidiram depois da correção de um bug na recuperação por id.
- Números que medem populações diferentes não são comparáveis sem uma tabela de reconciliação explícita.
- Um espelho replica mais do que código. A automação do repositório vem junto, então espelhos precisam de controles próprios.
- Inconclusivo é um estado próprio: uma verificação que não consegue confirmar nunca deve reportar recuperação.

## O que não é mostrado de propósito

Nomes de repositórios e organizações (além de Azure DevOps), nomes de clientes, endereços de e-mail, nomes e escopos de tokens, fingerprints de varredura, commits excluídos, detalhes de incidentes, código-fonte e capturas de tela.

---
<sub>Estudo de caso sanitizado. O código-fonte é privado; esta página mostra apenas arquitetura, decisões e estado verificável. · <a href="../README.pt-BR.md">Voltar ao perfil</a></sub>
