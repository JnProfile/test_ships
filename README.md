# Ship Database Randomizer and Testing

This project is designed to create a database of ships and their components (weapons, hulls, engines), randomize their attributes, and run automated tests to verify data integrity and expected behavior.

## Requirements

- **Python**: 3.12 or higher
- **Dependencies**: Managed via `requirements.txt`

## Project Structure

- **`tables.py`**: Defines the database models (`Ship`, `Weapon`, `Hull`, `Engine`) and randomization logic.
- **`create_and_fill_db.py`**: Script to initialize and populate the database with initial data.
- **`test_ships.py`**: Test suite to validate database changes and randomization logic.
- **`requirements.txt`**: Specifies required Python packages.

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install dependencies
   ```bash
    pip install -r requirements.txt
   ```

3. Create and fill original database
   ```bash
   python create_and_fill_db.py
   ```

4. Run tests
   ```bash
   pytest test_ships.py
   ```