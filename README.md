## Como rodar esse projeto

### Com docker compose
Docker compose é uma forma rápida de criar ambientes docker/ containers.

1. Instale docker compose

> *Dependendo da forma de instalação, o plugin **compose** já é automaticamente instalado. Para verificar, execute `$ docker compose`*

2. Crie um arquivo **.env** com o mesmo conteúdo de **.env.example** ou simplesmente rode `$ cp .env-example .env`.

3. Rode
```shell
  $ docker compose up --build
```
4. Acesse **0.0.0.0:8000/**.

5. Para gerar dados, execute
```shell
# rode com os containers em execução
$ docker compose exec django python manage.py populate_database
```

.
OBS: Esse projeto usa imagens seguras, pode ser verificado em ./Dockerfile e ./docker-compose.yaml .

### Com poetry
O [poetry](https://python-poetry.org/docs/) é um gerenciador de dependências python.
Para instalar, recomendo usar:
```shell
  # instala poetry
$ pipx install poetry
```
além disso, você precisa subir o container do postgres:
```shell
$ cp .env-example .env
  # sobe o container do postgres
$ docker compose up -d postgresql
```

Depois disso é só executar `python manage.py runserver`
e acessar `localhost:8000`

Com o comando `python manage.py populate_database` é possível criar rapidamente um usuário
administrador com username "admin" e senha "password", além de outros dados fakes para trabalhar.

## Sobre o projeto
O template base desse projeto foi tirado do meu repositório [modelo_rapido_djavue](https://github.com/Ronald-ps/modelo_rapido_djavue).
Os endpoints e algumas outras infos da api podem ser encontradas em [API.md](./API.md)

## Sobre testes
Nesse projeto, a lib utilizada foi o [pytest-django](https://pytest-django.readthedocs.io/en/latest/).
O testes estão contidos numa app chamada "dev", o que permite uma maior organização:
é possível evoluir os testes de aplicativos e os mecanismos de teste sem poluir a organização da aplicação principal.

Os testes da aplicação principal (core) estão na pasta [tests_core](./dev/tests_core/).

O foco foi criar testes unitários, ou seja, testes que validam pequenas funcionalidades do código.
Testes unitários são melhores de manter, com eles, é mais fácil de localizar qual unidade de código gerou problema
na sua aplicação. Além de trazerem segurança para modificar código, afinal, se o teste passou, então tá beleza!

Eu testei alguns funcionalidades, como o soft delete que implementei e as views de login e companies.

Para rodar os testes, basta executa `pytest .` no terminal.
Para executar um teste específico, basta executar:
`pytest _caminho_do_arquivo_::_nome_da_função`


## Sobre as variáveis do .env/.env-example
O .env é o arquivo salva variáveis de ambientes que projeto django e mesmo o docker-compose lerá.
- POSTGRES_PORT: É a porta de conexão do banco de dados.
- POSTGRES_USER: usuário do banco de dados, para autenticação.
- POSTGRES_PASSWORD: senha do banco de dados para autenticação.
- POSTGRES_HOST: host de conexão ao banco de dados. Para o caso de ambos os projetos estarem rodando em container,
esse host é sobrescrito
- FRONTEND_ORIGIN: origem das requisições ao backend. Por políticas de cors, e mesmo de csrf, as chamadas ao backend são restritas à hosts confiáveis.
- PRINCIPAL_HOST: Host principal onde o projeto estará rodando. Se o seu site estiver hospedado em mysite.com.br, esse é o valor que deverá estar na variável.
- ENVIRONMENT: Ambiente em que a aplicação está rodando. Pode ter dois valores: "production" e "development".
   - development: ambiente de desenvolvimento
   - production: ambiente de produção
