- [Requisição para o django de uma origem diferente](#requisição-para-o-django-de-uma-origem-diferente)
- [Configurar axios](#configurar-axios)
- [Como fazer login](#como-fazer-login)
- [Endpoints](#endpoints)
    - [`/whoami`](#whoami)
    - [`/login`](#login)
    - [`/companies`](#companies)
    - [`/companies/<int:pk>`](#companiesint-pk)
    - [`/companies/simple-list`](#companiessimple-list)
---
---
# API

Para conectar uma api do frontend com o projeto, é necessário configurar o cliente http.
É possível acessar a api por meio de uma origem diferente do servidor, graças a política de cors-Origin.
É preciso estar autenticado para algumas requisições. Abaixo, encontrará como se conectar à api.
A forma de comunicação da api é por meio do trasporte de dados Json.

## Requisição para o django de uma origem diferente
É preciso salvar qual a origem das quais serão feitas a requisição.
Essas origens podem ser alteradas em people_control/settings.py :: CORS_ORIGIN_WHITELIST,
que armazena um conjunto de origens permitidas, e em people_control/settings.py :: CSRF_TRUSTED_ORIGINS.
Porém, caso seja apenas um frontend, e não haja cenários em que a api vai receber chamadas de mais de uma origem,
é mais seguro simplesmente alterar a variável FRONTEND_ORIGIN para conter o host da origem da requisição.

Exemplo: se a url do meu frontend é "https://people_control.com.br/pessoas/listagem"
basta salvar `FRONTEND_ORIGIN="https://people_control.com.br"`


## Configurar axios
O axios é com certeza uma das bibliotecas de cliente http mais usadas no frontend.
Segue um exemplo de configuração do axios para esse projeto:

```js
import axios from 'axios';

axios.defaults.xsrfHeaderName = 'x-csrftoken';
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.withCredentials = true;
axios.defaults.headers.common['Content-Type'] = 'application/json';

export const defaultBackendHttpClient = axios.create({
  // a baseUrl é o domínio do servidor
  baseURL: `http://localhost:8000/`,
  timeout: 60000,
});
```


## Como fazer login
O endpoint de login é "/login", porém, é importante notar o método de requisição é POST,
portanto, o django faz verificação de **csrf**. Então, é preciso obter o csrf antes de fazer a requisição.
Para obter o cookie de csrf, basta fazer uma chamada para "/whoami", que é uma api que retorna informações do usuário.
**whoami** é um endpoint para requisição GET, com verificação de cors, e que retorna um cookie csrf.


## Endpoints
### `/whoami`
> methods: ["GET"]
> *Retorna as informações se o usuário está logado/autenticado. Caso esteja, retorna também as informações do usuário.*
> Exemplo de retorno:
```json
# Usuário autenticado
{
  "user":{
          "id": 1,
          "username": "homem_aranha",
          "first_name": "Miles",
          "last_name": "Morales",
          "email": "o.taal.de.aranha@outlook.com"
        },
  "authenticated": true
}

```
```json
# Usuário não autenticado
{"authenticated": false}
```
---

### `/login`
> methods: ["POST"]
> *Faz login com base na senha e usuário passados.*
> Parâmetros:
> - **username**: str
> - **password**: str
---

### `/companies/`
> methods: ["GET", "POST"]
> *Retorna uma lista com informação de empresas, em método get, e salva uma company com requisição POST.*
>
> Parâmetros POST:
> - **cnpj**: str: apenas dígitos numéricos, máximo de 14 números
> - **cep**: str: apenas dígitos numéricos, máximo de 8 dígitos
> - **state_acronym**: str: apenas letras, máximo de 2 letras
> - **name**: str
>
> Exemplos de Retorno (GET)
```json
{
    "count": 37,
    "next": "http://localhost:8000/companies/?page=2",
    "previous": null,
    "results": [
        {
            "id": 2,
            "cnpj": "12.345.678/0001-99",
            "cep": "12345-678",
            "state_acronym": "SP",
            "name": "Empresa ABC Ltda.",
            "employee_count": 100,
            "is_active": true,
            "address": "Rua dos Exemplos, 123",
            "city": "São Paulo",
            "country": "Brasil"
        },
        {
            "id": 3,
            "cnpj": "98.765.432/0001-01",
            "cep": "54321-098",
            "state_acronym": "RJ",
            "name": "Indústria XYZ S/A",
            "employee_count": 500,
            "is_active": true,
            "address": "Avenida das Amostras, 456",
            "city": "Rio de Janeiro",
            "country": "Brasil"
        },
        ...
    ]
}
```
---

### `/companies/<int: pk>`
> methods: ["GET", "PUT", "PATCH"]
> *Retorna informações de uma empresa, em método get, e salva uma company com requisição PUT E PATCH(edição de dados).*
>
> Parâmetros PUT e PATCH(não obrigatórios):
> - **cnpj**: str: apenas dígitos numéricos, máximo de 14 números
> - **cep**: str: apenas dígitos numéricos, máximo de 8 dígitos
> - **state_acronym**: str: apenas letras, máximo de 2 letras
> - **name**: str
>
> Exemplos de retorno:
```json
{
    "id": 1,
    "cnpj": "12.345.671/2345-67",
    "cep": "12245-500",
    "state_acronym": "MG",
    "name": "Empresa ABC",
    "employee_count": 50,
    "is_active": true,
    "address": "Rua Principal, 123",
    "city": "Belo Horizonte",
    "country": "Brasil"
}
```
---

### `/companies/simple-list`
> methods: ["GET"]
> *Retorna uma lista de empresas com nome e id ordenado por número de funcionários e sub-ordenado por nome*
> Parâmetros:
> - **page**: int
>
> Paginação: 10 items por requisição
> Exemplo de retorno:
```json
{
  "companies": [
   { "id": 1, "name": "Company10"},
   { "id": 24, "name": "Company11"},
   { "id": 30, "name": "Company12"},
  ]
}
```
---
### `/departments/`
> methods: ["GET", "POST"]
> *Retorna informações sobre departamentos de uma empresa. Com método POST, cria um novo departamento*
> Parâmetros POST:
> - **id**: int. Id do departamento
> - **company**: int (relacionamento com a empresa associada ao departamento)
> - **cost_center**: str. Info do centro de custo.
> - **name**: str. Nome do departamento.
> - **integration_code**: str. Código de integração do departamento.
> Exemplos de retorno:
```json
{
    "count": 9,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "employee_count": 0,
            "company": 38,
            "company_name": "Granero",
            "cost_center": null,
            "name": "Department A",
            "integration_code": "IntegrationCode1"
        },
        {
            "id": 2,
            "employee_count": 0,
            "company": 39,
            "company_name": "ABC Company",
            "cost_center": null,
            "name": "Department B",
            "integration_code": "IntegrationCode2"
        },
        ...
    ]
}
```
