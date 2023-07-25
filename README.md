# Dólar Câmbio

Sistema para consulta de cotação do Real, Euro e Iene em relação ao Dólar.
Os usuários podem visualizar através de um gráfico um período de 5 dias úteis
da cotação de uma moeda.

Os dados são coletados da API do [vatcomply](https://www.vatcomply.com/documentation) e salvos no banco de dados Postgres da aplicação. Na API do vatcomply, os dados de cotação
só existem a partir da data `04/01/1999`, e consequentemente, na aplicação, somente datas
a partir desta poderão ser consultadas.

A aplicação está hospedada na cloud do Google (GCP) e pode ser acessada através do link:
[https://cotacoes-image-2qiqrd5tla-rj.a.run.app/](https://cotacoes-image-2qiqrd5tla-rj.a.run.app/)

## Detalhes do funcionamento

A aplicação é bem simples e foi implementada usando o framework Django, contendo apenas uma única página com o gráfico de cotação
das moedas em relação ao dólar americano. A moeda exibida por padrão é o `Real`, mas
o usuário pode selecionar outras 2 moedas: `Euro` e `Iene`.

Por padrão, o gráfico é gerado com as cotações dos últimos 5 dias úteis presentes no banco
de dados. No entanto, as datas também podem ser manipuladas pelos usuários.

O usuário pode definir a `data de início` ou a `data final`. Como um dos requisitos do teste
é que o intervalo de consulta dos usuários não ultrapasse 5 dias, ao selecionar a `data de início`,
automaticamente a `data final` é preenchida com 5 dias úteis para frente e, da mesma forma, ao
selecionar a `data final`, automaticamente a `data de início` é preenchida com 5 dias para trás.
Dessa forma, o usuário não consegue selecionar um intervalo maior que 5 dias.

A aplicação também possui uma API usando o Django Rest Framework, na qual os usuários podem ter acesso
aos dados de todas as cotações existentes no banco de dados. Para acessar o endpoint da API, basta clicar
[aqui](https://cotacoes-image-2qiqrd5tla-rj.a.run.app/api/cotacoes/).
A API possui paginação, com 100 objetos retornados por página, e está disponível apenas para leitura dos dados.
Possui também a possibilidade de filtrar os dados pelos campos `moeda`, `data` e `sigla`.
[Aqui](https://cotacoes-image-2qiqrd5tla-rj.a.run.app/api/cotacoes/?moeda=Real) esta um exemplo de filtro pela moeda Real.
Além disso, a API possui outro endpoint que é utilizado para atualizar o banco de dados, buscando as cotações
diariamente e permitindo que os usuários tenham acesso aos dados mais atualizados de cotações.

Essa atualização dos dados ocorre da seguinte forma:
Um job do serviço `Cloud Scheduler` do GCP foi criado para realizar uma chamada ao endpoint
de atualização dos dados a cada hora, conforme mencionado acima.
Esse endpoint executa um código que consulta na API do vatcomply os dados das cotações do dia em questão e
quando encontra um resultado válido, salva no banco de dados.
Assim, de forma descentralizada, usando o serviço `Cloud Scheduler` do Google, os dados na aplicação estarão
sempre atualizados.

#### *Observação*
Uma nova requisição só é feita para consultar novas datas quando o usuário clica no botão `Consultar`.
Para visualizar os valores de outras moedas na mesma data já carregada, somente o gráfico é atualizado
sem precisar fazer uma nova request para o backend.

## Pré-requisitos para execução local

Certifique-se de ter instalado os seguintes requisitos antes de executar o projeto:

- Docker
- Docker Compose
- Make

## Instalação

1. Clone o repositório:

   ```bash
   git clone git@github.com:Augusto94/dolar_cambio.git
   ```

2. Acesse o diretório do projeto:

    ```bash
    cd dolar_cambio
    ```
3. Criei um arquivo chamado `.env` baseado no arquivo `.env-example`.

4. Execute o comando do Docker Compose para construir e iniciar o projeto:

    ```bash
    docker-compose up
    ```
    ou
    ```bash
    make start

Nesse momento, a aplicação web implementada utilizando o framework Django estará
rodando e disponível no endereço: `http://localhost:8000/`.

Para popular o banco de dados basta rodar os seguintes comandos na raiz do projeto:
1. `make shell`
2. `from cotacoes.populate_db import popular_banco`
3. `popular_banco()`

## Explicação do Projeto
Como já dito anteriormente, o projeto web foi desenvolvido utilizando o framework Django e a API
para consulta dos dados foi feita utilizando o Django Rest Framework.

O gráfico para visualização das cotações no frontend foi criado utilizando o `Highcharts`.
Já os calendários exibidos para os usuários selecionarem a data foram criados utilizando o `Pikaday`.
O preenchimento automático das datas, explicado anteriormente, foi feito utilizando JavaScript.

O deploy da aplicação em produção foi realizado usando os serviços do `Cloud Build` e `Cloud Run`.
Em resumo, o Cloud Build foi configurado para ser executado sempre que houver uma modificação na branch `master` do repositório no GitHub. Conforme descrito no arquivo `cloudbuild.yaml` na raiz do projeto, é criada uma
imagem docker para a aplicação que é armazenada no serviço `Artifact Registry`.
Após criar a imagem, o Cloud Build realiza o deploy do sistema no serviço `Cloud Run`.

O banco de dados utilizado no ambiente de produção também está hospedado no Google, através do serviço `Cloud SQL`,
onde uma instância do PostgreSQL está sendo executada.

Foi feito uso do pre-commit para padronização e garantir uma qualidade no código. Também foi utilizado type hint e escrita de
docstrings no padrão do Google nas funções, facilitando o entendimento do código.

O gerenciamento das dependências Python do projeto são feitas utilizando o `Poetry`.

Os testes unitários foram implementados usando o pytest.

# Testes

Para executar os testes automatizados, utilize o seguinte comando:
```bash
docker-compose run --rm web pytest --cov --cov-report term-missing --cov-fail-under 95 --disable-pytest-warnings
```
ou simplesmente:
```bash
make test
```

A cobertura mínima dos testes definida é de 95% e no momente da entrega do desafio esta em 98%.

## Observações e análise do projeto

#### *Stack das principais tecnologias/serviços utilizados*
 - Django
 - Django Rest Framework
 - Cloud Build
 - Cloud Run
 - Cloud Scheduler
 - PostgreSQL
 - Docker
 - Docker Compose
 - Pytest
 - Poetry
 - pre-commit

#### Possíveis melhorias

 - Melhorar a tela onde o gráfico é exibido, utilizando ferramentas de frontend mais avançadas. Uma opção seria adotar um framework de frontend, como o React, que oferece recursos modernos e uma melhor experiência ao usuário.

 - Fazer uso de alguma ferramenta de CI (Githb Actions, Travis CI, etc) para realizar a integração contínua do projeto.

 - Utilizar Celery Beat para execução de tarefas agendadas e Celery para execução de tarefas em segundo plano que possam demorar, evitando travamentos na aplicação e garantindo uma melhor performance.

 - Fazer o deploy da aplicação usando Kubernetes, proporcionando maior gerenciamento, escalabilidade, resiliência e diversos outros benefícios oferecidos pelo Kubernetes. Isso permitirá um ambiente mais robusto e de fácil manutenção.

## Contato

`email`: **augustoarl@gmail.com** 

`redes sociais`: **@augustoarl**
