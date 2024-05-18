# webcompanion

## Overview
This Flask application, named WebCompanion, provides a simple web interface for managing tasks.

## Requirements
- Python 3.x
- Flask
- Waitress

## Installation
1. Clone this repository to your local machine:
2. Navigate to the project directory:
3. Install the required Python packages using pip:

    `pip install -r requirements.txt`


## Usage
To run the WebCompanion Flask app with Waitress, follow these steps:

1. Make sure you are in the project directory.

2. Open a terminal or command prompt.
    Run the following command to start the Flask app with 
    * For Development
        * You run `python app.py`
    * For Production
        * `waitress-serve --listen="0.0.0.0:5000" app:app`


4. Once the server starts, you should see output indicating that the server is running and listening on a certain port (usually 8080 by default).

5. Open your web browser and navigate to `http://localhost:8080` to access the WebCompanion application.

## Configuration
You can configure the Flask application by modifying the `config.py` file in the `WebCompanion` directory. This file contains settings such as the database connection string, secret key, etc.

## Contributing
If you'd like to contribute to this project, please fork the repository, make your changes, and submit a pull request. We welcome contributions of all kinds, including bug fixes, feature enhancements, and documentation improvements.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

