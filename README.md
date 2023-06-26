# EmoTouch™ scripts

Here are some python scripts to parse the output data from the EmoTouch web application.

---

## Usage

The files to be processed must be in the folder `input/` (whose content is't uploaded to the repo, but keeps the file structure).

Specifically the files are the **Zeitreihendaten** in **csv** format.

1. Activate virtual environment.

    ```shell
    source .venv/bin/activate
    ```

1. Run main script:

    ```shell
    python emotouch.py
    ```

1. Choose `emoTouch` file to process (`TAB`, then click on file).

1. The resulting `.csv` file, and the respective plot will be saved in the `output/` folder.
