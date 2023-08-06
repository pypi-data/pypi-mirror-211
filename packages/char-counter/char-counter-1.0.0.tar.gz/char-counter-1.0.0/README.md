
# Char Counter

Char Counter is a command line tool that counts the number of unique characters in a text file or an input string.

## Installation

1. Clone the repository:
```bash
git clone <git@git.foxminded.ua:foxstudent102513/task-5-create-the-python-package.git>
```
2. Navigate to the project directory:
```bash
cd <task-5-create-the-python-package>
```
3. Install the project using pip:
```bash
pip install .
```

## Usage

Char Counter can be used with two arguments: `--string` and `--file`.

To count unique characters in a string, use the `--string` argument:
```bash
python -m char_counter --string "Your text here"
```

To count unique characters in a text file, use the `--file` argument:
```bash
python -m char_counter --file /path/to/your/file.txt
```

Note: Running without parameters will result in the following message: "Please provide either --string or --file parameter.".

## Author

- Uladzimir Radchanka - Uradchanka@gmail.com

## License

This project is licensed under the MIT License.

---
