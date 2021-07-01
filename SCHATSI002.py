import os
import csv
import pdftotext


# At first: open the Output-File --> "SCHATSI_included.csv"
# local path for testing: "SCHATSI_included.csv"
output = open("/data/output/SCHATSI_included.csv", 'w', newline='')
# create a writer object, which is used to write the lines into the csv
file = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)
# onetime writing of a headline into the csv
kopfzeile = ["filename", "type", "included", "excluded"]
file.writerow(kopfzeile)


# For all paths, subdirectories and files in the input-folder do:
# local path for testing: "r'/home/h/Github/Testpdfs'"
for path, subdirs, files in os.walk(r'/data/input'):
    for filename in files:

        # with data path
        g = os.path.join(path, filename)

        # Filename in 'Schatsi_included.txt' schreiben, ohne den Dateipfad/ in csv-Datei
        f = os.path.join(filename)

        # try to read in a pdf and extract text from it
        try:
            with open(g, "rb") as pdffile:
                # create an object which is filled with a raw byte stream, which contains the text from the pdf
                pdf = pdftotext.PDF(pdffile)
                # force python to turn the byte stream into a string
                text = "\n\n".join(pdf)
                # print the text into a terminal for testing
                print(text)

        # if it fails do:
        # if there is an exception or an error, they will be catched and the file wont be included in the next steps
        except:
            if f.endswith(".pdf"):
                datatype = "pdf"
            elif f.endswith(".txt"):
                datatype = "txt"
            elif f.endswith(".csv"):
                datatype = "csv"
            elif f.endswith(".docx"):
                datatype = "docx"
            elif f.endswith(".odt"):
                datatype = "odt"
            else:
                datatype = "unknown datatype"
            zeile = [f, datatype, "__", "X"]

        # if it succeeds do:
        else:
            if f.endswith(".pdf"):
                datatype = "pdf"
            elif f.endswith(".txt"):
                datatype = "txt"
            elif f.endswith(".csv"):
                datatype = "csv"
            elif f.endswith(".docx"):
                datatype = "docx"
            elif f.endswith(".odt"):
                datatype = "odt"
            else:
                datatype = "unknown datatype"
            zeile = [f, datatype, "X", "__"]

        file.writerow(zeile)
        # the outputfile will get a layout like this
        """
        filename | type | included | excluded
        --------------------------------------
        abc.pdf  | pdf  |     X    |    __        <-- The text of this document could be extracted without any problems
        err.pdf  | pdf  |    __    |     X        <-- There was a problem and the document text could not be extracted,
        ...                                           the files wont be included in the next steps 
        ...
        """

output.close()


