# Currency Converter

Converte valores entre as moedas: BRL, USD, EUR, BTC, ETH

## Tech Stack

- Django, Django Rest Framework
- VueJS
- MySQL
- NGINX
- Docker

## Instalar e executar o projeto

- Clone o projeto

- Dentro do diretório, execute: ```docker compose up --build -d```

- Aguarde até que finalize a instalação dos pacotes do Python e do VueJS

  - Acompanhe, se necessário, com ```docker compose logs -t -f```

- Acesso front-end http://localhost

- Acesso API(opcional), exemplo: http://localhost/api/convert/BRL/EUR/100

- Para executar testes unitários: ```docker compose exec -ti app python3 manage.py test```