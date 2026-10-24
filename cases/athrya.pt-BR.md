# Athrya — uma plataforma multi-tenant para academias de artes marciais

<p align="right"><sub><a href="athrya.en.md">English</a></sub></p>

## Contexto

Academias de jiu-jitsu vivem de aulas recorrentes, frequência, progressão de faixas e famílias, já que muitos alunos são menores de idade. Muitas funcionam em rede, então a mesma pessoa pode treinar em uma unidade e dar aula ou fazer a gestão em outra. Athrya é um SaaS multi-tenant pensado para esse cenário. Cobre grade de aulas, check-in, frequência e suas correções, acompanhamento de graduação, currículo, convites, responsáveis e menores supervisionados (13 a 17 anos) e a administração de cobranças da academia.

## Desafio

- **Muitos papéis, uma única base de dados.** Alunos, professores, gestores, recepção e operadores da plataforma precisam de acessos diferentes. O acesso depende da unidade em que a pessoa está atuando.
- **Dados de menores.** Responsáveis legais, contas supervisionadas e a transição para a maioridade precisam ser modelados de forma explícita e tratados com cuidado.
- **Um único engenheiro.** A rede de segurança precisava ser automatizada e obrigatória, e não depender de convenção.
- **Um lançamento real.** Revisão das lojas, infraestrutura de produção, migrações e hypercare precisavam funcionar numa data fixa de go-live, em outubro de 2026.

## Meu papel

Fui o arquiteto e engenheiro líder, responsável pela arquitetura, implementação, qualidade e release do produto.
Cerca de 99% dos commits do repositório do produto entre agosto e outubro de 2026 são atribuídos às minhas identidades Git;
o restante vem de outros três colaboradores e de uma identidade de automação.

- Defini o modelo de domínio, as decisões de arquitetura (13 ADRs e um registro de 22 decisões) e os critérios de aceite.
- Estabeleci os controles de engenharia que toda mudança precisava passar: um gate de PR obrigatório, política de migrations e testes de fronteira de segurança.
- O desenvolvimento usou ferramentas assistidas por IA sob minha especificação, revisão e controle de merge; toda mudança passou por revisão independente antes do merge.
- Assumi cada merge e as aprovações técnica, de produto e de operações para o go-live.

## Arquitetura

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/cases/athrya-architecture-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="../assets/cases/athrya-architecture-light.svg">
  <img alt="Athrya architecture: mobile app, portal, platform admin and invite landing in production, dashboard in development; shared packages; API as the single authorization authority; managed PostgreSQL; delivery from PR gate to promote or rollback." src="../assets/cases/athrya-architecture-dark.svg" width="100%">
</picture>


Um monorepo TypeScript (npm workspaces e Turborepo) reúne **6 apps e 16 pacotes compartilhados**:

- **App mobile.** Um único app Expo / React Native para iOS, Android e web, com uma área para cada papel. É a experiência padrão para todos.
- **API.** NestJS com Prisma sobre PostgreSQL. É a única autoridade de autorização.
- **Portal e Platform Admin.** Apps Next.js para a operação da academia e para o operador do SaaS, respectivamente.
- **Landing de convite.** Leva a pessoa convidada à loja de apps certa ou ao Portal.
- **Dashboard.** Complemento de tela grande ao app. Ainda não foi publicado.

**Camadas.** Os pacotes de domínio e de aplicação são TypeScript puro, e uma regra de lint impede que frameworks de UI entrem neles. Os contratos foram escritos do domínio para fora. As telas trocaram repositórios mock pela API real um domínio de cada vez.

**Multi-tenancy.** O acesso é modelado como *papel na unidade*, então uma pessoa pode ter vários papéis em várias academias. Toda rota é protegida por padrão. O escopo de tenant é aplicado na camada de dados e verificado de novo de forma explícita. Os papéis de plataforma e os papéis de academia são separados.

**Dados.** São **129 modelos de dados e 233 migrações**. As migrações são aditivas e seguem o padrão expand/contract. Uma única etapa de deploy as executa; a API nunca migra o próprio banco.

**Infraestrutura.** O backend roda em contêineres gerenciados no Azure, com PostgreSQL gerenciado em rede privada. A infraestrutura é definida como código em Bicep, e o CI faz deploy por federação OIDC, sem chaves estáticas. As feature flags vêm de configuração gerenciada, e os logs são centralizados, com alertas. Os apps web rodam numa plataforma de hospedagem gerenciada. Os builds mobile e as atualizações over-the-air (OTA) saem pelos serviços da Expo. Os tokens de design são gerados a partir de Figma Variables, e um teste quebra o build se aparecer qualquer valor fixo de cor ou geometria.

## Decisões e trade-offs

As decisões estão registradas em **13 ADRs e num log de 22 decisões**. As principais:

- **Um app universal em vez de três.** Isso dá uma presença nas lojas e um único trem de release. O custo é mais cuidado com a navegação por papel.
- **NestJS em vez de Express puro.** Os guards e providers se encaixam no isolamento entre tenants.
- **Prisma.** Escolhido pelas migrações em arquivo, fáceis de revisar.
- **Estado do servidor no TanStack Query.** Não há store global no cliente. Valores monetários são guardados como centavos inteiros.
- **O front-end nunca é fronteira de segurança.** A API verifica tudo de novo.
- **Sem processamento de pagamento online no MVP.** A cobrança é administrativa: configuração de chave de pagamento, cobranças e comprovantes manuais. Isso evitou uma grande carga de compliance. Os módulos de cobrança estão construídos e ficam atrás de feature flags.
- **"Nenhum dado inventado."** Valores de negócio ainda não decididos aparecem como estados explícitos de *não configurado*, e não como padrões plausíveis.
- **"Mergeado não é homologado."** As integrações com parceiros entram inertes e só são ativadas depois da certificação do parceiro.
- **Uma topologia de ambientes enxuta**, dimensionada para um teto de orçamento mensal fixo.
- **Um gate de PR em vez de quatro.** Motivado em parte pela concorrência limitada do CI.
- **Sem segundo revisor humano obrigatório.** Uma escolha consciente enquanto o time é um único engenheiro; o gate de PR obrigatório continua sendo a régua de qualidade aplicada a toda mudança.

## Práticas de engenharia

- **Um único gate obrigatório de PR.** Ele roda:
  - auditoria de dependências, lint, typecheck e varredura de segredos;
  - testes unitários com cobertura;
  - migrações a partir do zero;
  - testes de fronteira de segurança para acesso entre tenants e escalada de papel;
  - testes de integração contra um PostgreSQL efêmero;
  - testes end-to-end com Playwright;
  - verificação das dependências mobile.
- **Suíte de testes.** Cerca de **880 arquivos de teste automatizado** entre apps e pacotes, 406 deles na API.
- **Governança de release.** Squash merges, aprovação obrigatória para produção, uma trava contra execuções de release desatualizadas, um gate de compatibilidade para OTA e uma árvore de decisão de rollback para cada camada.
- **Deploy da API em etapas.** Cada revisão passa por smoke test e só então é promovida, com rollback automático.
- **Auditoria de segurança pré-lançamento.** Gerou **42 achados**, tratados em ondas por prioridade.
- **Observabilidade.** IDs de correlação e telemetria de release em todo log da API, e cada instância em execução informa a versão do build.

## Resultados

- Go-live em **outubro de 2026**, com cinco superfícies em produção.
- O app mobile está publicado na **App Store e no Google Play**.
- **8 atualizações OTA** foram publicadas durante o hypercare, todas pelo mesmo gate. O rollback automático da API nunca precisou ser acionado.
- Depois do lançamento, os fluxos de responsáveis e menores supervisionados foram mergeados. A cobrança e a base para integrações com parceiros entraram atrás de flags, desligadas por padrão.

Não publico números de uso, receita ou crescimento. Quando este texto foi escrito, a revisão formal de encerramento do hypercare ainda estava em aberto.

## Status atual

| Componente | Status | Tipo de evidência |
|---|---|---|
| App mobile (iOS / Android) | Production | Páginas na App Store e no Google Play |
| API | Production | Pipeline de deploy com revisão em etapas e promoção |
| Portal | Production | Host no ar e pipeline de deploy |
| Platform Admin | Production | Pipeline de deploy com aprovação |
| Landing de convite | Production | Pipeline de deploy |
| Dashboard | In development | Apenas repositório; não publicado |
| Cobrança da academia | In development (construída, atrás de feature flags) | Código mergeado; ativação em produção não verificada |
| Integrações com parceiros de benefícios | In development | Mergeadas inertes; não homologadas |
| Protótipo separado de plataforma de treinamento | In development (pausado) | Repositório anterior; sem evidência de deploy |

## Lições aprendidas

- **Um gate automatizado vale mais que convenções.** Com um time pequeno, a régua de qualidade precisa estar na automação, não na memória.
- **Trabalho em paralelo precisa de isolamento e de um integrador.** Uma regra de "um escritor por vez" evita que a reconciliação consuma o ganho de velocidade.
- **Contratos a partir do domínio compensam.** Junto com a troca de mocks pela API real, eles deixaram o produto avançar antes do backend, sem retrabalho.
- **Mergeado, publicado e ativado são estados diferentes.** As flags permitem integrar trabalho inacabado sem expô-lo.
- **Migrações precisam de uma única autoridade.** Isso tira da aplicação o passo mais arriscado de um release.
- **Instrumente todas as plataformas antes do lançamento.** No lançamento, a telemetria de crashes não estava igualmente completa nas duas plataformas mobile.
- **Assuma o bus factor abertamente.** Um modelo com um único engenheiro depende de decisões e runbooks escritos.

## O que intencionalmente não é mostrado

- **Código-fonte.** É privado e continua privado.
- **Identidade de clientes.** Nenhuma academia, localidade ou pessoa é citada. As capturas de tela só serão mostradas depois de refeitas com dados neutros.
- **Identificadores de infraestrutura.** Hosts, recursos, IDs de projeto e identificadores de app ficaram de fora.
- **Detalhes de segurança.** O desenho dos controles, os achados da auditoria e o endurecimento ainda pendente não são descritos além do nível desta página.
- **Números de negócio.** Não há números de usuários, receita, adoção ou orçamento.

---
<sub>Estudo de caso sanitizado. O código-fonte é privado; esta página mostra apenas arquitetura, decisões e estado verificável. · <a href="../README.pt-BR.md">Voltar ao perfil</a></sub>
