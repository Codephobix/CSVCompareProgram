import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# ----------------------------------
# Funktion zur CSV-Verarbeitung
# ----------------------------------

def compare_csv(av_files, mon_files, av_column, mon_column):
    av_df_list = []
    mon_df_list = []

    # CSV-Dateien einlesen und die angegebenen Spalten verwenden
    try:
        for av_file in av_files:
            if os.path.exists(av_file):
                av_df = pd.read_csv(av_file, usecols=[av_column])
                av_df.columns = ['Name']
                av_df_list.append(av_df)

        for mon_file in mon_files:
            if os.path.exists(mon_file):
                mon_df = pd.read_csv(mon_file, usecols=[mon_column])
                mon_df.columns = ['Name']
                mon_df_list.append(mon_df)

        if not av_df_list or not mon_df_list:
            return "Fehler: Mindestens eine Datei konnte nicht eingelesen werden."
    except Exception as e:
        return f"Fehler beim Einlesen der CSV-Dateien: {e}"

    # Daten kombinieren
    av_df = pd.concat(av_df_list)
    mon_df = pd.concat(mon_df_list)

    # Leere Zeilen entfernen
    av_df.dropna(subset=['Name'], inplace=True)
    mon_df.dropna(subset=['Name'], inplace=True)

    # Alphabetisch sortieren
    av_df.sort_values('Name', inplace=True)
    mon_df.sort_values('Name', inplace=True)

    # Zusammenführen der Daten
    merged_df = pd.merge(av_df, mon_df, on='Name', how='outer', indicator=True)

    # Fehlt Monitoring oder Antivirus?
    merged_df['Fehlt'] = merged_df['_merge'].apply(lambda x: 'Monitoring' if x == 'right_only' else ('Antivirus' if x == 'left_only' else ''))

    # Nur fehlende Einträge speichern
    missing_df = merged_df[merged_df['Fehlt'] != '']

    if missing_df.empty:
        return "Alle Geräte sind vollständig."

    result_text = ""
    for _, row in missing_df.iterrows():
        result_text += f"Gerätename: {row['Name']} | Fehlt: {row['Fehlt']}\n"

    return result_text

# ----------------------------------
# GUI-Teil
# ----------------------------------

def select_files(label, file_list):
    filenames = filedialog.askopenfilenames(filetypes=[("CSV-Dateien", "*.csv")])
    if filenames:
        file_list.extend(filenames)
        label.config(text="; ".join(file_list))

def reset_files(label, file_list):
    file_list.clear()
    label.config(text="Keine Datei ausgewählt")

def compare_csv_gui():
    if not av_files or not mon_files:
        messagebox.showerror("Fehler", "Bitte mindestens eine Antivirus- und eine Monitoring-CSV-Datei auswählen!")
        return

    # Prüfen, ob bereits ein Vergleich durchgeführt wurde
    global comparison_done
    global reset_done

    if comparison_done and not reset_done:
        if not messagebox.askyesno("Warnung", "Die bisherigen Dateien wurden nicht zurückgesetzt. Möchten Sie fortfahren?"):
            return

    av_column = av_column_entry.get()
    mon_column = mon_column_entry.get()

    if not av_column or not mon_column:
        messagebox.showerror("Fehler", "Bitte beide Spaltennamen eingeben!")
        return

    result_text = compare_csv(av_files, mon_files, av_column, mon_column)

    # Ergebnis in Text-Widget anzeigen
    result_output.delete(1.0, tk.END)  # Vorherige Ausgabe löschen
    result_output.insert(tk.END, result_text)  # Neue Ausgabe einfügen

    # Vergleich wurde durchgeführt
    comparison_done = True
    reset_done = False

# GUI erstellen
root = tk.Tk()
root.title("CSV Vergleich Tool")

# Dateilisten speichern
av_files = []
mon_files = []

# Vergleichsstatus speichern
comparison_done = False
reset_done = True

# Antivirus-Bereich
av_frame = tk.Frame(root)
av_frame.pack(pady=5, padx=10, anchor="w")

tk.Button(av_frame, text="Antivirus CSV(s) hinzufügen", command=lambda: select_files(av_file_label, av_files)).grid(row=0, column=0, padx=5)
av_file_label = tk.Label(av_frame, text="Keine Datei ausgewählt", width=50, anchor="w")
av_file_label.grid(row=0, column=1, padx=5)
tk.Button(av_frame, text="Zurücksetzen", command=lambda: [reset_files(av_file_label, av_files), globals().update(reset_done=True)]).grid(row=0, column=2, padx=5)

av_column_entry = tk.Entry(av_frame, width=40)
av_column_entry.grid(row=1, column=1, pady=5)
av_column_entry.insert(0, "Name")

# Monitoring-Bereich
mon_frame = tk.Frame(root)
mon_frame.pack(pady=5, padx=10, anchor="w")

tk.Button(mon_frame, text="Monitoring CSV(s) hinzufügen", command=lambda: select_files(mon_file_label, mon_files)).grid(row=0, column=0, padx=5)
mon_file_label = tk.Label(mon_frame, text="Keine Datei ausgewählt", width=50, anchor="w")
mon_file_label.grid(row=0, column=1, padx=5)
tk.Button(mon_frame, text="Zurücksetzen", command=lambda: [reset_files(mon_file_label, mon_files), globals().update(reset_done=True)]).grid(row=0, column=2, padx=5)

mon_column_entry = tk.Entry(mon_frame, width=40)
mon_column_entry.grid(row=1, column=1, pady=5)
mon_column_entry.insert(0, "Name")

# Button zum Ausführen des Skripts
run_button = tk.Button(root, text="Vergleich ausführen", command=compare_csv_gui)
run_button.pack(pady=20)

# Text-Widget für die Ausgabe
result_output = tk.Text(root, height=20, width=100)
result_output.pack(pady=10, padx=10)

# Copyright-Label hinzufügen
copyright_label = tk.Label(root, text="Copyright (C) 2025 CSVCompareprogram; Codephobia (Codephobix)\nLicensed under GPL-3.0 and Commercial use with permission.", anchor="center", font=("Arial", 8), fg="gray")
copyright_label.pack(side=tk.BOTTOM, pady=5)

# GUI starten
root.mainloop()
