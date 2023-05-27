# API

- [Conectar uma api do frontend com o projeto](#conectar-uma-api-do-frontend-com-o-projeto)
- [Requisição para o django de uma origem diferente](#requisição-para-o-django-de-uma-origem-diferente)
- [Configurar axios](#configurar-axios)
- [Como fazer login](#como-fazer-login)
- [Endpoints](#endpoints)
  - [/whoami](#whoami)
  - [/login](#login)
  - [/companies/](#companies)
  - [/companies/<int: pk>](#companiesint-pk)
  - [/companies/simple-list](#companiessimple-list)
  - [/departments/](#departments)
  - [/departments/<int: pk>](#departmentsint-pk)
  - [/employees/](#employees)
  - [/employees/<int: pk>](#employeesint-pk)
  - [/employees/inactivated/<int: pk>](#employeesinactivatedint-pk)
- [Django-filters](#django-filters)
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
A maioria dos endpoints desse projeto são permitidas apenas para usuários logados.
O endpoint de login é "/login", porém, é importante notar que o método de requisição é POST,
portanto, o django faz verificação de **csrf**. É preciso obter o cookie de csrf antes de fazer a requisição.
Para obter, basta fazer uma chamada para "/whoami", que é um endpoint que retorna informações do usuário.
**whoami** é um endpoint para requisição GET, com verificação de cors, e que retorna um cookie csrf.

## Endpoints
### `/whoami`
> methods: ["GET"]
> *Retorna as informações se o usuário está logado/autenticado. Caso esteja, retorna também as informações do usuário.*
>
> Exemplos de retorno:
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
            "cnpj": "12345678000199",
            "cep": "12345678",
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
            "cnpj": "98765432000101",
            "cep": "54321098",
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
> methods: ["GET", "PUT", "PATCH", "DELETE"]
> *Retorna informações de uma empresa, em método get, e salva uma company com requisição PUT E PATCH(edição de dados).*
> *Com método DELETE, deleta a company (soft-delete)*
>
> Parâmetros PUT e PATCH(não obrigatórios):
> - **cnpj**: str: apenas dígitos numéricos, máximo de 14 números
> - **cep**: str: apenas dígitos numéricos, máximo de 8 dígitos
> - **state_acronym**: str: apenas letras, máximo de 2 letras
> - **name**: str: nome da empresa.
> - **is_active**: bool. Indica se a empresa é ativa ou não.
>
> Exemplos de retorno:
```json
{
    "id": 1,
    "cnpj": "12345671234567",
    "cep": "12245500",
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
>
> Exemplos de retorno:
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
> - **name**: str. Nome do departamento.
> - **integration_code**: str. Código de integração do departamento.
>
> Exemplos de retorno:
```json
{
    "count": 9,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "employee_count": 3,
            "company": 38,
            "company_name": "Granero",
            "name": "Department A",
            "integration_code": "IntegrationCode1"
        },
        {
            "id": 2,
            "employee_count": 4,
            "company": 39,
            "company_name": "ABC Company",
            "name": "Department B",
            "integration_code": "IntegrationCode2"
        },
        ...
    ]
}
```
---
### `/departments/<int: pk>`
> methods: ["GET", "PUT", "PATCH", "DELETE"]
> *Retorna informações sobre departamentos de uma empresa. Com método PATCH, edita um departamento*
> *Com método DELETE, deleta o departamento (soft-delete)*
>
> Parâmetros PATCH(parâmetros não obrigatórios):
> - **id**: int. Id do departamento
> - **company**: int (relacionamento com a empresa associada ao departamento)
> - **name**: str. Nome do departamento.
> - **integration_code**: str. Código de integração do departamento.
> - **is_active**: bool. Indica se o departamento é ativo ou não.
>
> Exemplos de retorno:
```json
{
    "id": 1,
    "employee_count": 19,
    "company": 38,
    "company_name": "Granero",
    "name": "Department A",
    "integration_code": "IntegrationCode1"
}
```
### `/employees/`
> methods: ["GET", "POST"]
> *Retorna informações sobre funcionários de uma empresa ou departamento. Com método POST, cria um novo funcionário*
> Parâmetros POST:
> - id: int. Id do funcionário.
> - company: int. Relacionamento com a empresa associada ao departamento.
> - department: int. Relacionamento com o departamento.
> - first_name: str. Primeiro nome.
> - last_name: str. Sobrenome.
> - email: str. Endereço de e-mail.
> - phone: str. Número de telefone.
> - date_of_birth: str. Data de nascimento.
> - date_of_entry: str. Data de entrada.
> - date_of_departure: str. Data de saída.
> - city: str. Cidade.
>
> Parâmetros GET:
>> Alguns parâmetros de filtragem e ordenação podem ser passados para a api.
>> Essa filtragem é baseada em [django-filters](https://django-filter.readthedocs.io/en/stable/)
>> Para saber mais sobre como filtra, veja a [seção django-filters](#django-filters)
>> mas esses segue um exemplo da estrutura de uma url para filtragem:
>> http://localhost:8000/employees/?company__id=3&ordering=first_name&date_of_entry__gte=22%2F01%2F2022
>> repare nos parâmetros company__id=3, ordering=first_name e date_of_entry__gte=22%2F01%2F2022
>
> Exemplos de retorno:
```json
{
    "count": 34,
    "next": "http://localhost:8000/employees/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "company": 47,
            "company_name": "OpenAI Technologies",
            "department": 10,
            "department_name": "Engineering",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "551234567890",
            "date_of_birth": "1990-01-01",
            "date_of_entry": "2021-01-01",
            "date_of_departure": null,
            "city": "San Francisco"
        },
        {
            "id": 2,
            "company": 49,
            "company_name": "Acme Corporation",
            "department": 11,
            "department_name": "Sales",
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "phone": "19876543210",
            "date_of_birth": "2022-12-31",
            "date_of_entry": "2022-12-31",
            "date_of_departure": null,
            "city": "New York City"
        }
        ...
    ]
}

```
---
### `/employees/<int: pk>`
> methods: ["GET", "PUT", "PATCH", "DELETE"]
> *Retorna informações sobre UM funcionário de uma empresa ou departamento. Com método PATCH, edita os dados do funcionário*
> *Com método DELETE, deleta o funcionário (soft-delete)*
>
> Parâmetros PATCH(parâmetros opcionais):
> - id: int. Id do funcionário.
> - company: int. Relacionamento com a empresa associada ao departamento.
> - department: int. Relacionamento com o departamento.
> - first_name: str. Primeiro nome.
> - last_name: str. Sobrenome.
> - email: str. Endereço de e-mail.
> - phone: str. Número de telefone.
> - date_of_birth: str. Data de nascimento.
> - date_of_entry: str. Data de entrada.
> - date_of_departure: str. Data de saída.
> - city: str. Cidade.
> - **is_active**: bool. Indica se o funcionário é ativo ou não.
>
> Exemplos de retorno:
```json
{
    "id": 1,
    "company": 47,
    "company_name": "OpenAI Technologies",
    "department": 10,
    "department_name": "Engineering",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "551234567890",
    "date_of_birth": "1990-01-01",
    "date_of_entry": "2021-01-01",
    "date_of_departure": null,
    "city": "San Francisco"
}
```
---

### `/employees/inactivated/<int: pk>`
> methods: ["GET", "PUT", "PATCH"]
> *Retorna informações sobre UM funcionário de uma empresa ou departamento, mas apenas se o funcionário for inativado. Com método PATCH, edita os dados do funcionário, inclusive, reativa-o.*
>
> Parâmetros PATCH(parâmetros opcionais):
> - id: int. Id do funcionário.
> - company: int. Relacionamento com a empresa associada ao departamento.
> - department: int. Relacionamento com o departamento.
> - first_name: str. Primeiro nome.
> - last_name: str. Sobrenome.
> - email: str. Endereço de e-mail.
> - phone: str. Número de telefone.
> - date_of_birth: str. Data de nascimento.
> - date_of_entry: str. Data de entrada.
> - date_of_departure: str. Data de saída.
> - city: str. Cidade.
> - **is_active**: bool. Indica se o funcionário é ativo ou não.
>
> Exemplos de retorno:
```json
{
    "id": 1,
    "company": 47,
    "company_name": "OpenAI Technologies",
    "department": 10,
    "department_name": "Engineering",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "551234567890",
    "date_of_birth": "1990-01-01",
    "date_of_entry": "2021-01-01",
    "date_of_departure": null,
    "city": "San Francisco"
}
```
---

## Django-filters
Ao utilizar o Django Filters, você pode passar uma variedade de parâmetros na URL para pesquisar e filtrar os  dados. Os parâmetros GET mais comuns que podem ser usados com o Django Filters são:
- `exact`: Filtra os registros onde o campo é exatamente igual ao valor fornecido.
- `iexact`: Filtra os registros onde o campo é exatamente igual ao valor fornecido, ignorando diferenças de maiúsculas e minúsculas.
- `contains`: Filtra os registros onde o campo contém o valor fornecido.
- `icontains`: Filtra os registros onde o campo contém o valor fornecido, ignorando diferenças de maiúsculas e minúsculas.
- `in`: Filtra os registros onde o campo está entre uma lista de valores fornecidos.
- `gt`: Filtra os registros onde o campo é maior que o valor fornecido.
- `gte`: Filtra os registros onde o campo é maior ou igual ao valor fornecido.
Ex: http://localhost:8000/employees/?date_of_entry__gte=22%2F01%2F2022
- `lt`: Filtra os registros onde o campo é menor que o valor fornecido.
- `lte`: Filtra os registros onde o campo é menor ou igual ao valor fornecido.
- `startswith`: Filtra os registros onde o campo começa com o valor fornecido.
- `istartswith`: Filtra os registros onde o campo começa com o valor fornecido, ignorando diferenças de maiúsculas e minúsculas.
- `endswith`: Filtra os registros onde o campo termina com o valor fornecido.
- `iendswith`: Filtra os registros onde o campo termina com o valor fornecido, ignorando diferenças de maiúsculas e minúsculas.
- `isnull`: Filtra os registros onde o campo é nulo.
