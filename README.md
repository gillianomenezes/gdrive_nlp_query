# Google Drive NLP Query

This is a Python script that interacts with the Google Drive API to search for specific words within documents using Natural Language Processing (NLP). The script downloads Google Docs, processes them with [spaCy](https://pypi.org/project/spacy/), and prints matching sentences.

## Prerequisites

Before running the script, ensure you have the following set up:

- **Google API Credentials:**
  - Create a service account on the Google Cloud Console and download the OAuth 2.0 JSON key file.
  - Save the JSON key file as `secrets/credentials.json` in the project directory.

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/gillianomenezes/gdrive_nlp_query.git
    cd your-repository
    ```

2. Build the Docker image:

    ```bash
    docker build -t gdrive-nlp-query .
    ```

3. Run the Docker container:

    ```bash
    docker container run -it gdrive-nlp-query python gdrive_nlp_query.py[arg1] [arg2] ...
    ```

    Example:

    ```bash
    docker container run -it gdrive-nlp-query python gdrive_nlp_query.py word1 word2
    ```

## Command-line Arguments

- `arg1`, `arg2`, ...: Words to search for in the Google Docs.

## Testing

The project includes pytest tests for some of the script functions. To run the tests:

```bash
docker run gdrive-nlp-query pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to customize this template according to your specific project details and requirements. Include any additional information or instructions that might be helpful for users or contributors.