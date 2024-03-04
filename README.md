# Currency Converter

Converte valores entre as moedas: BRL, USD, EUR, BTC, ETH

Os valores são obtidos utilizando a Awesome API: https://docs.awesomeapi.com.br/api-de-moedas

Obs: Obtem-se apenas os preços de cada moeda em dólar e a conversão é feita de forma local, no back-end do projeto.

Obs2: Foi criado um cache para que os valores não sejam consultados a todo momento. O tempo de validade do cache pode ser configurado em ```converter/services.py``` na variável ```CACHE_TTL``` e está originalmente configurado para 10 segundos.

## Tech Stack

- Django, Django Rest Framework
- VueJS
- MariaDB
- NGINX
- Docker

## Funcionamento docker

A aplicação foi dividida em 4 contêineres:

- app(Django)
- vue-app(VueJS)
- db(MariaDB)
- nginx(NGINX)

Todo o acesso é feito normalmente pela porta 80, tendo o NGINX atuando como gateway/proxy, direcionando o acesso para o conteiner correto.

## Instalar e executar o projeto

- Clone o projeto

- Dentro do diretório, execute: ```docker compose up --build -d```

- Aguarde até que finalize a instalação dos pacotes do Python e do VueJS

  - Acompanhe, se necessário, com ```docker compose logs -t -f```

- Acesso front-end http://localhost

- Acesso API(opcional), exemplo: http://localhost/api/convert/BRL/EUR/100

- Para executar testes unitários: ```docker compose exec -ti app python manage.py test```