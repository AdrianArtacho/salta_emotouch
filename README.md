# EmoTouch™ script

Here are some python scripts to parse the output data from the EmoTouch web application.

---

## Running the script

The files to be processed must be in the folder `INPUT/`
(whose content isn't uploaded to the repo, but kept in the file structure).

1. Activate virtual environment.
   
   ```shell
   source .venv/bin/activate
   ```

2. Run main script:
   
   ```shell
   python EMOTOUCH.py
   ```

3. Choose `emoTouch` file to process (`TAB`, then click on file).

4. The resulting `.csv` file, and the respective plot will be saved
   in the `OUTPUT/` folder.

---

## Exporting emoTouch session data

Go to the study / session, and click `export`.

1. Go to [EmoTouch Web](https://ri.emotouch.de/en/home)

2. Click on the play ▶ icon

3. Go to *realisations* (click on a specific one)

4. Go to *sessions*

5. Click on one of the sessions

6. Click on `EXPORT`

Specifically download the file called **Zeitreihendaten** (*Complete Timeline data*)
in **csv** format. Leave all options unchanged!

- Line terminator char `Windows (CR LF)`
- Delimiter `Semicolon`
- Quote char: `"`
- Decimal separator `Dot`
- Thousands separator `None`

![export-dialog.png](images/emoto_export-dialog.png)

---

## Metadata.json

Besides the individual `.csv` and `.png` files corresponding to the segmentation
plot, metadata is also stored in the `metadata.json` file.

If that `metadata.json` file doesn't exist, the script will create it.
It is therefore recommended to rename the json file after a session,
so that the next one starts with a clean slate.

---

## Stats

The main script also generates a wealth of statistical data
for each of the test annotations.
These will be stored also in the 'OUTPUT/' folder, with the .json extension.

---

## measure the length of a video WITH PRECISION

You can run the `MOVIE_LENGTH.py` script, with the path to the video file as argument.
NOTE: The result will be in seconds, but `cached_info.csv` expects it in milliseconds!

---

## METAPLOTS

Running the `METAPLOTS.py` script will generate different plots.
