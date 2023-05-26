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
4. Acesse **localhost:8000/**.

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

## Sobre o projeto
O template base desse projeto foi tirado do meu repositório [modelo_rapido_djavue](https://github.com/Ronald-ps/modelo_rapido_djavue).
Os endpoints e algumas outras infos da api podem ser encontradas em [API.md](./API.md)
