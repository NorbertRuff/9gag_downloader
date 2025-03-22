# Project Structure

This document outlines the organization of the 9GAG Downloader project.

## Overview

The project has been restructured to provide a clear separation of concerns between the following parts:

- **Core Logic**: Business logic, data parsing, downloading, etc.
- **UI Components**: User interface elements
- **Configuration**: Application settings
- **Utilities**: Helper functions and logging

## Directory Structure

```
src/
├── core/                   # Core business logic
│   ├── downloader/         # Download functionality
│   │   └── download_handler.py
│   ├── parser/             # HTML/data parsing 
│   │   └── html_parser.py
│   └── models/             # Data models
│       └── gag.py
├── ui/                     # UI components
│   ├── frames/             # UI frames
│   │   ├── checkboxes_frame.py
│   │   ├── destination_folder_frame.py
│   │   ├── download_frame.py
│   │   ├── header_frame.py
│   │   ├── progress_bar_frame.py
│   │   └── source_file_frame.py
│   ├── components/         # Reusable UI components
│   └── app.py              # Main app class
├── utils/                  # Utilities
│   ├── logging/            # Logging functionality
│   │   └── logger.py
│   └── helpers/            # Helper functions
│       └── file_utils.py
├── config/                 # Configuration settings
│   ├── colors.py           # Color definitions
│   └── theme.py            # UI theme settings
├── __init__.py
└── __main__.py             # Entry point
```

## Package Responsibilities

### Core

The `core` package contains the business logic of the application:

- **models**: Data classes representing the entities in the application
- **parser**: Code for parsing HTML data exports from 9GAG
- **downloader**: Code for downloading content from 9GAG

### UI

The `ui` package contains the user interface components:

- **frames**: Frame components that make up the application UI
- **components**: Reusable UI components
- **app.py**: The main application class that ties everything together

### Utils

The `utils` package contains utility functions and classes:

- **logging**: Logging functionality
- **helpers**: Helper functions for file operations, etc.

### Config

The `config` package contains configuration settings:

- **colors.py**: Color definitions
- **theme.py**: UI theme settings

## Benefits of the New Structure

This new structure offers several benefits:

1. **Clear Separation of Concerns**: Each module has a specific responsibility
2. **Improved Maintainability**: Changes in one area don't affect others
3. **Better Testability**: Components can be tested in isolation
4. **More Flexible**: Easier to extend or replace parts of the system
5. **Better Organization**: Code is organized logically by function
6. **Type Safety**: Proper type annotations throughout the codebase
