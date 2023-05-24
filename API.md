# API

Para conectar uma api do frontend com o projeto, é necessário configurar o cliente http.
É possível acessar a api por meio de uma origem diferente do servidor, graças a política de cors-Origin.
É preciso estar autenticado para algumas requisições. Abaixo, encontrará como se conectar à api.

## Requisição para o django de uma origem diferente
É preciso salvar qual a origem das quais serão feitas a requisição.
Essas origens podem ser alteradas em people_control/settings.py :: CORS_ORIGIN_WHITELIST,
que armazena um conjunto de origens permitidas.
Porém, caso seja apenas um frontend, e não haja cenários em que a api vai receber chamadas de mais de uma origem,
é possível simplesmente alterar a variável FRONTEND_ORIGIN para conter o host da origem da requisição.

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
  baseURL: `http://localhost:8000/`,
  timeout: 60000,
});
```

## Endpoints
- `/login`
> methods: ["POST"]
> *Faz login com base na senha e usuários passados.*
>> Parâmetros:
>> - username: str
>> - password: str
