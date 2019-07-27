[Versão em inglês](README.md)

# TempEng

TempEng é um template engine simples desenvolvido em Python. Através dele é possível gerar arquivos textuais acrescidos de dados inseridos dinamicamente por meio da compilação e execução de templates.

## Obtendo o programa

Para começar a utilizar TempEng basta clonar este repositório em sua máquina local.
TempEng não requer qualquer dependência externa, ter Python 3 instalado é o único requisito para executar o programa.



## Uso
TempEng deve ser executado a partir do módulo main.py localizado no diretório raiz do projeto.
A primeira etapa no uso do programa é a compilação de um template a partir de um arquivo textual, como demonstrado no seguinte exemplo:

Abaixo temos o conteúdo do arquivo `static_template.html`:
```
<p>Student: {{student.name}}</p>
<p>Grade: {{student.grade}}</p>
<p>Result: {%if student.grade >= 7 %}Approved{%endif%}{%if student.grade < 7 %}Reproved{%endif%}</p>
```
Para compilar este arquivo em um template nomeado `template.py` executamos:
```
$ python3 main.py -c static_template.html -co template.py
```
Podemos então executar o template compilado para gerar arquivos textuais com dados dinâmicos. Mas para isso precisamos de um contexto de dados, na forma de um arquivo json. O arquivo `data_context.json` contém uma array com dois objetos json, um para cada arquivo a ser gerado:
```
[
  {
    "student": {
      "name": "Jonh",
      "grade": 6
    },
    "$file_name$": "John.html"
  },
  {
    "student": {
      "name": "Mary",
      "grade": 8
    },
    "$file_name$": "Mary.html"
  }
]
```
Para gerar os arquivos a partir do template e do contexto de dados, executamos novamente `main.py`:
```
$ python3 -e template.py -d data_context.json
```
Com isso, obtemos dois arquivos textuais com dados inseridos dinamicamente:

 `John.html`
```
<p>Student: Jonh</p>
<p>Grade: 6</p>
<p>Result: Reproved</p>
```
e `Mary.html`:
```
<p>Student: Mary</p>
<p>Grade: 8</p>
<p>Result: Approved</p>
```

Também é possível realizar esta tarefa em um único passo, operando a compilação e execução a partir de um só comando:
```
$ python3 main.py -c static_template.py -co template.py -d data.json -e
```

## Executando os testes

TempEng contém um conjunto de testes unitários e de integração que podem ser executados através da módulo `main_test.py`.
Os testes devem ser executados através do diretório raíz do programa.

Para rodar o conjunto completo de testes:
```
$ python3 main_test.py
```
#### Testes unitários

Os testes unitários cobrem todos os métodos das classes responsáveis pelo parsing e compilação de templates, e alguns dos métodos envolvidos na execução dos mesmos.

Para executar o conjunto de testes unitários:
```
$ python3 main_test.py -u
```
#### Testes de integração

Os testes de integração cobrem todo o processo de compilação e execução de templates.

Para executar os testes de integração:
```
$ python3 main_test.py -i
```

## Contribuindo

Sugestões, pedidos ou implementações de funcionalidades e relatórios de possíveis bugs são bem-vindos. Se desejar contribuir de alguma dessas formas, simplesmente abra um issue para tratar do assunto, ou submeta um PR se for uma contribuição de código fonte.

## Licença

Este projeto está licenciado sob a GNU General Public License v3.0. Para mais detalhes, veja [LICENSE](LICENSE).

## Agradecimentos
**Ned Batchelder**, autor do capítulo [A Template Engine](http://aosabook.org/en/500L/a-template-engine.html) em um dos livros da série **The Architecture of Open Source Applications**. Na época em que eu folheava este livro, eu estava às voltas com uma tarefa que exigia a criação de um template engine, e pretendia construí-lo baseado em interpretação. A leitura dos primeiros parágrafos deste capítulo me convenceram de que seria mais divertido desenvolver um programa baseado em compilação.

Contudo, vale ressaltar que o código contido aqui foi **desenvolvido independentemente** do código de Batchelder - a única coisa que os dois compartilham é a sintaxe suportada pelos templates, que por sua vez é inspirada em Django.
