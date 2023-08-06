import unittest
from unittest import mock
from io import StringIO
from cli import process_string, process_file, process_input


class CLITestCase(unittest.TestCase):

    @mock.patch('sys.argv', ['', '--string', 'your string'])
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_process_input_string_parameter(self, mock_stdout):
        process_input()
        self.assertEqual(mock_stdout.getvalue(), "Unique characters in string: 9\n")

    @mock.patch('sys.argv', ['', '--file', 'path/to/text_file.txt'])
    @mock.patch('cli.read_file', return_value="your file content")
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_process_input_file_parameter(self, mock_stdout, mock_read_file):
        process_input()
        mock_read_file.assert_called_with('path/to/text_file.txt')
        self.assertEqual(mock_stdout.getvalue(), "Unique characters in string: 7\n")

    @mock.patch('sys.argv', [''])
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_process_input_no_parameters(self, mock_stdout):
        process_input()
        self.assertEqual(mock_stdout.getvalue(), "Please provide either --string or --file parameter.\n")

    @mock.patch('sys.argv', ['', '--string', 'your string', '--file', 'path/to/text_file.txt'])
    @mock.patch('cli.read_file', return_value="your file content")
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_process_input_string_and_file_parameters(self, mock_stdout, mock_read_file):
        process_input()
        mock_read_file.assert_called_with('path/to/text_file.txt')
        self.assertEqual(mock_stdout.getvalue(), "Unique characters in string: 7\n")

    @mock.patch('sys.argv', ['', '--file', 'path/to/non_existing_file.txt'])
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_process_input_file_not_found(self, mock_stdout):
        with self.assertRaises(FileNotFoundError) as cm:
            process_input()
        self.assertEqual(str(cm.exception), "File not found: path/to/non_existing_file.txt")


if __name__ == '__main__':
    unittest.main()
