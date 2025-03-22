# 9GAG Downloader Tests

This directory contains unit tests for the 9GAG Downloader application.

## Test Files

- `test_html_parser.py`: Tests for the HTML parser module
- `test_downloader.py`: Tests for the download handler module
- `test_settings_manager.py`: Tests for the settings manager module

## Test Data

- `test_9gag_data_simplified.html`: A simplified 9GAG HTML export file for testing

## Running Tests

You can run all tests using the `run_tests.py` script:

```bash
python tests/run_tests.py
```

Or you can run individual test files:

```bash
python -m unittest tests/test_html_parser.py
python -m unittest tests/test_downloader.py
python -m unittest tests/test_settings_manager.py
```

## Test Coverage

The tests cover the following components of the application:

### HTML Parser Tests

- Parsing saved gags from the HTML export file
- Parsing upvoted gags from the HTML export file
- Extracting both saved and upvoted gags
- Error handling for non-existent files

### Downloader Tests

- Video download functionality
- Image download functionality
- Proper error handling for various HTTP status codes
- Title sanitization
- Downloading in the correct order (video first, then image as fallback)

### Settings Manager Tests

- Saving and loading settings
- Updating source file, destination folder, and checkbox settings
- Handling window size updates
- Managing recent files with a limit of 5
- Error handling for corrupted or non-existent settings files

## Adding Tests

To add new tests:

1. Create a new test file following the pattern `test_*.py`
2. Extend the `unittest.TestCase` class
3. Add test methods that begin with `test_`

Your tests will be automatically discovered by the test runner.
