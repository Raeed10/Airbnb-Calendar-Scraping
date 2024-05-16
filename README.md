
# Airbnb Calendar Scraping

This project scrapes calendar data from Airbnb listings.

## Prerequisites

Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

## Getting Started

Follow these steps to set up and run the project:

### 1. Clone the Repository

First, clone this repository to your local machine:

```sh
git clone https://github.com/zeidzen/Airbnb-Calendar-Scraping.git
cd Airbnb-Calendar-Scraping
```

### 2. Set Up Virtual Environment

It is recommended to use a virtual environment to manage your project dependencies.

#### Install `venv`

If you don't have `venv` installed, you can install it using the following command:

```sh
pip install virtualenv
```

#### Create Virtual Environment

Create a virtual environment in the project directory:

```sh
python -m venv venv
```

#### Activate Virtual Environment

Activate the virtual environment using the following commands:

- On Windows:

    ```sh
    venv\Scripts\activate
    ```

- On macOS and Linux:

    ```sh
    source venv/bin/activate
    ```

### 3. Install Required Libraries

Install the required libraries from the `requirements.txt` file:

```sh
pip install -r requirements.txt
```

### 4. Run the Scraper

Run the Airbnb scraper script:

```sh
python scrape_airbnb.py
```

## Deactivating the Virtual Environment

Once you are done, you can deactivate the virtual environment with the following command:

```sh
deactivate
```

## Additional Information

For more information on how to use the scraper or contribute to the project, please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
