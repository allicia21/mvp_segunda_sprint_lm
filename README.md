# mvp_segunda_sprint_lm
api e front para treinamento de um modelo de apredizagem de maquina para avaliação da segunda sprint do cuso de pós graduação de enegenharia de software


## estrutura e tecnologias do projeto
Este projeto tem duas pastas uma responsavel pelo front end e uma responsavel pelo back end.
Para construção da api foi utlizado a linguagem python com flask, e sqlAlchime como banco de dados.
Para a construção do front foi utilizado html e css para estilização.

## Como executar o front
basta abrir o arquivo index.html no seu navegador, ou abrir o link no console quando rodar o projeto banck end(http://127.0.0.1:5000/).

## Como executar a api

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
