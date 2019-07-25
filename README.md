[Portuguese version](README.pt-br.md)

# TempEng

TempEng is a simple template engine written in Python.
By compiling static text files in templates, it allows you to execute such templates to generate new text files with dynamic data embedded into them.


## Getting Started

You can start using TempEng just by cloning this repository on your local machine.
TempEng does not require any external dependency, having Python 3 installed is enough to run it.


## Usage

TempEng can be run by executing the `main.py` module localized in the root directory of the project.
You can start by compiling a template from a textual file, as show in the example bellow.

Here we have the content of the `static_template.html` file:
```
</p>Student: {{student.name}}</p>
</p>Grade: {{student.grade}}</p>
</p>Result: {%if student.grade >= 7 %}Approved{%endif%}{%if student.grade < 7 %}Reproved{%endif%}</p>
```
To compile this file into a template named `template.py` we run the main module passing the following arguments:
```
$ python3 main.py -c static_template.html -co template.py
```
Now we can execute the template we just compiled to generate textual files and embed dynamic data into them. But first we need a data context from which TempEng can get data to embed. TempEng works with json data files, like `data_context.json`, whose contents are shown bellow. As we can see, our data context contains an array with two json objects, one for each file to be generated:
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
To generate the text files from the template and the data context, we execute `main.py` again:
```
$ python3 -e template.py -d data_context.json
```
This results in two textual files with embedded dynamic data:

 `John.html`
```
</p>Student: Jonh</p>
</p>Grade: 6</p>
</p>Result: Reproved</p>
```
and `Mary.html`:
```
</p>Student: Mary</p>
</p>Grade: 8</p>
</p>Result: Approved</p>
```

It's also possible to do this task in a single step by running compilation and execution using just one command:
```
$ python3 main.py -c static_template.py -co template.py -d data.json -e
```

## Running the tests

TempEng contains a set of unit and integration tests which can be executed through the module `main_test.py`. The tests must be executed from the project root directory.

Run the complete set of tests:
```
$ python3 main_test.py
```
#### Unit tests

TempEng unit tests cover all the methods of the classes responsible for parsing and compiling templates, and some of the functions responsible for executing them.

Run all unit tests:
```
$ python3 main_test.py -u
```
#### Integration tests

TempEng integration tests cover the entire process of compiling and executing templates.

Run the integration tests:
```
$ python3 main_test.py -i
```

## Contributing

Contributions are very welcome. You can send feature requests or bug reports by opening a issue to discuss the subject. If your contribution contains source code or improvements to TempEng documentation, you can submit it by opening Pull Request against the master branch of this repository.

## License

This project is licensed under the terms of the **GNU General Public License v3.0**. For more details, see [LICENSE](LICENSE).

## Acknowledgments
**Ned Batchelder**, author of the chapter [A Template Engine](http://aosabook.org/en/500L/a-template-engine.html) from one of the books from the series **The Architecture of Open Source Applications**. By the time I was reading this book, I was grappling with a task that required creating a template engine, and I intended to build it based on interpretation. The first few paragraphs of this chapter convinced me that it would be more fun to write a program based on compilation.

However, it may be worthwhile stressing that the source code of TempEng was developed independently of Batchelder's template engine code - the only thing that both share is the syntax supported by the templates, which in turn is based on Django.
