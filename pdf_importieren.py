# Skript zum Laden einer, bisher noch im selben Ordner wie das Skript befindlichen, PDF-Datei
# Anschlißend soll der Text aus der PDF-Datei extrahiert werden
# Der Text wird anschließend untersucht hinsichtlich seiner Form und der Korrektheit der Extraktion
# Weiterhin solll geprüft werden, ob nicht benötigte Textbausteine (Inhaltsverzeichnis/ Referenzen/...) bei der Extraktion entfernt werden können

# Import aller benoetigten Bibliotheken
from PyPDF2 import PdfFileReader
from tkinter import *
from tkinter import filedialog

ws = Tk()
ws.title('PDF importieren')
ws.geometry('1200x900')
ws.config(bg='#D9653B')

def choose_pdf():

    filename = filedialog.askopenfilename(
    initialdir = "/",   # for Linux and Mac users
    # initialdir = "C:/",   for windows users
    title = "Select a File",
    filetypes = (("PDF files","*.pdf*"),("all files","*.*")))
    if filename:
        return filename


def read_pdf():
    # Zur bestimmung des File-Namens wird die Funktion "choose_pdf" aufgerufen
    # In der Variable "filename" wird der Dateipfad bis zur Datei gespeichert
    filename = choose_pdf()
    # Erstellung eines PDFFileReader-Objektes
    reader = PdfFileReader(filename)
    # Bestimmung der Seitenanzahl und Speichern in pageObj
    pageObj = reader.getNumPages()

    # Für jede Seite wird nacheinander durchgeführt:
    # Ein objekt erstellen, welches die jeweilige Seite mit allen Inhalten enthält
    # Die Textdaten aus dem Seitenobjekt extrahieren und in ein weiteres Objekt speichern
    # Den Inhalt des Objektes in die Textbox einnfügen
    for page_count in range(pageObj):
        page = reader.getPage(page_count)
        page_data = page.extractText()
        textbox.insert(END, page_data)


def copy_pdf_text():
    content = textbox.get(1.0, "end-1c")
    ws.withdraw()
    ws.clipboard_clear()
    ws.clipboard_append(content)
    ws.update()
    ws.destroy()

# Grafische Oberfläche
textbox = Text(
    ws,
    height=50,
    width=150,
    wrap='word',
    bg='#D9BDAD'
)
textbox.pack(expand=True)

Button(
    ws,
    text='Choose Pdf File',
    padx=20,
    pady=10,
    bg='#262626',
    fg='white',
    # Aufruf der Funktion "read_pdf" bei Betaetigung des Buttons
    command=read_pdf
).pack(expand=True, side=LEFT, pady=10)

Button(
    ws,
    text="Copy Text",
    padx=20,
    pady=10,
    bg='#262626',
    fg='white',
    # Aufruf der Funktion "copy_pdf_text" bei Betaetigung des Buttons
    command=copy_pdf_text
).pack(expand=True, side=LEFT, pady=10)

# Bei Ausführung des Skriptes wird das Programm hier gestartet
ws.mainloop()

