<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banners/hero-animated-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/banners/hero-animated-light.svg">
  <img alt="Célio Crisólogo — Arquitecto de Software, Tech Lead, Ingeniería de IA Aplicada. Arquitecto sistemas. Construyo productos. Diseño inteligencia. (Texto de la imagen en inglés.)" src="assets/banners/hero-animated-dark.svg" width="100%">
</picture>

<p align="right"><a href="README.md">English</a> | <a href="README.pt-BR.md">Português (Brasil)</a> | <b>Español</b></p>

**Tech Lead · Arquitecto de Software · Cloud e IA aplicada · Sistemas distribuidos · Ingeniería de backend y plataformas.** Diseño plataformas, las llevo a producción y construyo sistemas de IA con las salvaguardas que requieren. Más de 8 años de experiencia en banca, telecomunicaciones, el área fiscal del sector público y plataformas corporativas; hoy lidero la entrega técnica en proyectos de clientes y construyo productos en [Includlab](https://includlab.com.br), mi software house.

<sub>El código fuente de los sistemas que siguen es privado. Aquí se muestran vistas de arquitectura sanitizadas, estado verificable y métricas agregadas, nunca la implementación.</sub>

## Ingeniería destacada

### 01 · Athrya — arquitectura de plataforma &nbsp;<sub><code>PRODUCCIÓN</code></sub>

SaaS multi-tenant para academias de jiu-jitsu: horario de clases, check-in, asistencia, progresión de cinturones, tutores y menores supervisados. Una app móvil (App Store y Google Play), portales web y una API, en producción desde octubre de 2026.
**Decisión:** el dominio, los casos de uso y los contratos viven en paquetes TypeScript compartidos de los que depende cada superficie, de modo que las reglas de negocio se escriben una sola vez; la API es la única autoridad de autorización y el alcance del tenant se aplica en la capa de datos. **Entrega:** un gate de PR obligatorio, migraciones aditivas mediante un pipeline dedicado, despliegues por etapas con rollback. Soy responsable de la arquitectura, de los controles de ingeniería, de cada merge y de las aprobaciones de go-live. → [Leer el caso](cases/athrya.es.md)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cases/athrya-architecture-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/cases/athrya-architecture-light.svg">
  <img alt="Arquitectura de Athrya: app móvil, portal, platform admin y landing de invitación en producción, dashboard en desarrollo; paquetes compartidos; API como única autoridad de autorización; PostgreSQL administrado; entrega desde el gate de PR hasta el promote o el rollback. (Texto de la imagen en inglés.)" src="assets/cases/athrya-architecture-dark.svg" width="100%">
</picture>

### 02 · AI-Assist — ingeniería de IA aplicada &nbsp;<sub><code>PROTOTIPO</code></sub>

Clientes Apple Watch e iPhone se comunican con un gateway de IA privado que concentra la identidad del dispositivo, el presupuesto y el kill switch, los límites de tasa y las claves de los proveedores; un enrutador de modelos **sin fallback silencioso** elige el adaptador.
**Estado real:** validado en simuladores con 187/187 pruebas del gateway y 136/136 de base de datos; toda respuesta hasta hoy provino de un proveedor mock o simulado; los adaptadores de Anthropic y OpenAI están listos, pero nunca se han invocado; no está desplegado ni en la App Store. → [Leer el caso](cases/ai-assist.es.md)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cases/ai-assist-architecture-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/cases/ai-assist-architecture-light.svg">
  <img alt="Arquitectura y estado real de AI-Assist: clientes de reloj y teléfono, gateway de IA privado, enrutador de modelos sin fallback silencioso, adaptador mock activo, adaptadores de Anthropic y OpenAI listos pero nunca invocados, laboratorio de infraestructura mantenido en una copia separada. (Texto de la imagen en inglés.)" src="assets/cases/ai-assist-architecture-dark.svg" width="100%">
</picture>

### 03 · Plataforma de ingeniería — DevOps intelligence &nbsp;<sub><code>OPERATIVO</code></sub>

La mayor parte de mi trabajo vive en repositorios privados de Azure DevOps. Esta plataforma lo hace visible **sin falsear nada**: un inventario de todo el historial, un gate de escaneo de secretos que falla en modo cerrado, un espejo privado unidireccional solo por fast-forward que conserva el SHA, el autor y la fecha de cada commit autorizado que replica (los commits excluidos por seguridad nunca se replican), y un recolector que deduplica por SHA y publica únicamente agregados mediante un schema estricto. Es el origen de los números que siguen. → [Leer el caso](cases/engineering-platform.es.md)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cases/engineering-platform-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/cases/engineering-platform-light.svg">
  <img alt="Pipeline de la plataforma de ingeniería: Azure DevOps, inventario, gate de seguridad, espejo privado, recolector, JSON público y perfil; con privilegio mínimo, health checks y alertas, programación consciente del costo y revisión independiente. (Texto de la imagen en inglés.)" src="assets/cases/engineering-platform-dark.svg" width="100%">
</picture>

## Evidencias de ingeniería

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/metrics/v2/031-activity-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/metrics/v2/031-activity-light.svg">
  <img alt="Actividad de ingeniería en todas las ramas: commits únicos atribuidos a mis identidades Git en 7 días, 30 días, 12 meses y todo el historial, divididos entre la rama por defecto, otras ramas activas y ramas eliminadas recuperadas por id. (Texto de la imagen en inglés.)" src="assets/metrics/v2/031-activity-dark.svg" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/metrics/v2/034-delivery-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/metrics/v2/034-delivery-light.svg">
  <img alt="Entrega en 12 meses: pull requests abiertos, completados tras el gate obligatorio, abiertos y abandonados, revisiones y squash merges. (Texto de la imagen en inglés.)" src="assets/metrics/v2/034-delivery-dark.svg" width="100%">
</picture>

<details>
<summary><b>Dónde vive el trabajo · fuentes · contribuciones en GitHub · cómo se producen los números</b></summary>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/metrics/v2/032-monthly-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/metrics/v2/032-monthly-light.svg">
  <img alt="Commits únicos por mes en 12 meses, divididos entre la rama por defecto y otras refs. (Texto de la imagen en inglés.)" src="assets/metrics/v2/032-monthly-dark.svg" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/metrics/v2/033-sources-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/metrics/v2/033-sources-light.svg">
  <img alt="Fuentes en 12 meses: commits solo en Azure DevOps, en ambas plataformas con el mismo SHA (contados una vez) y solo en GitHub. (Texto de la imagen en inglés.)" src="assets/metrics/v2/033-sources-dark.svg" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/metrics/v2/035-contributions-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/metrics/v2/035-contributions-light.svg">
  <img alt="Contribuciones en GitHub en 12 meses: total del calendario oficial, commits replicados elegibles y cuántos de ellos el calendario comprobadamente aún no muestra. (Texto de la imagen en inglés.)" src="assets/metrics/v2/035-contributions-dark.svg" width="100%">
</picture>

- Los conteos de commits se basan en identidades Git de autor verificadas, deduplicadas por SHA entre GitHub y Azure DevOps. Miden la actividad en los repositorios, no líneas escritas a mano ni la productividad individual.
- **Cuatro significados, nunca sumados:** actividad de ingeniería (cualquier rama), dónde vive el trabajo, entrega (pull requests y revisiones) y contribuciones en GitHub (lo que el propio GitHub reconoce, según sus reglas).
- **Fuentes:** API REST e historial Git de Azure DevOps y API de GitHub, recolectados en un pipeline privado; esta página recibe solo agregados ([`data/public-metrics-v2.json`](data/public-metrics-v2.json)). No se reescribió ningún historial ni se creó ningún commit para llenar el calendario.

</details>

## Tecnología y liderazgo

- **Arquitectura** sistemas distribuidos · microservicios · fronteras orientadas al dominio · integración orientada a eventos · modernización de sistemas legados · registros de decisiones
- **Backend** Java · Go · TypeScript/Node.js (NestJS) · Python · PostgreSQL · Kafka · Redis
- **Plataforma** Azure · AWS · Kubernetes · Docker · Bicep/Terraform · Azure DevOps · GitHub Actions · CI/CD · observabilidad
- **IA aplicada** agentes de IA · integración de LLM · gateways de LLM · enrutamiento multiproveedor · salvaguardas de costo y seguridad · diseño de evaluaciones
- **Liderazgo** dirección técnica hands-on · estándares de ingeniería · quality gates · gobernanza de releases · mentoría y contratación

## Contacto

[Portafolio](https://www.celiocrisologo.com.br/en) · [LinkedIn](https://www.linkedin.com/in/celioguimaraes117) · [celio@includlab.com.br](mailto:celio@includlab.com.br) · [Includlab](https://includlab.com.br) · [Links](https://linktr.ee/celio_rguimaraes)

Desde Brasil · trabajo remoto · portugués, inglés, español.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/brand/signature-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/brand/signature-light.svg">
  <img alt="Célio Crisólogo / Software Architecture / Backend / Applied AI" src="assets/brand/signature-dark.svg" width="380">
</picture>
