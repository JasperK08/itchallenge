  import tkinter as tk
from tkinter import ttk
from haber_bosch_simulatie import bereken_opbrengst

class HaberBoschUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Haber-Bosch Simulatie")
        self.root.geometry("600x600")
        
        # Parameterinstellingen
        self.parameters = {
            "Druk (atm)": {"min": 100, "max": 300, "value": 200},
            "Temperatuur (°C)": {"min": 400, "max": 500, "value": 450},
            "Stroomsnelheid (m³/u)": {"min": 10000, "max": 20000, "value": 16000},
            "Zuivering (%)": {"min": 20, "max": 50, "value": 25},
            "Koeling (°C)": {"min": -150, "max": 90, "value": 20},
        }

        self.entries = {}  # Synchronisatie sliders en invoervelden

        # Maak de UI-elementen
        for idx, (param, values) in enumerate(self.parameters.items()):
            frame = ttk.Frame(self.root)
            frame.pack(pady=10, fill="x")

            # Parameternaam
            label = ttk.Label(frame, text=param)
            label.grid(row=0, column=0, sticky="w")

            # Slider
            slider = ttk.Scale(
                frame,
                from_=values["min"],
                to=values["max"],
                orient="horizontal",
                command=lambda val, p=param: self.update_entry(p, val),
            )
            slider.set(values["value"])
            slider.grid(row=1, column=0, sticky="we", padx=5)

            # Invoerveld
            entry = ttk.Entry(frame, justify="center")
            entry.insert(0, values["value"])
            entry.grid(row=1, column=1, padx=5)
            entry.bind(
                "<FocusOut>",
                lambda event, p=param, s=slider: self.update_slider(p, s),
            )

            


            # Synchroniseer sliders en invoervelden
            self.entries[param] = (slider, entry)
            frame.columnconfigure(0, weight=1)

        # Bereken knop
        calculate_button = ttk.Button(self.root, text="Bereken", command=self.calculate)
        calculate_button.pack(pady=20)

        # Output voor berekening
        self.result_label = ttk.Label(self.root, text="Resultaat:")
        self.result_label.pack(pady=10)
        self.output_frame = ttk.Frame(self.root)
        self.output_frame.pack(pady=10)

    def update_entry(self, param, value):
        """Synchroniseer invoerveld als slider wordt aangepast."""
        slider, entry = self.entries[param]
        entry.delete(0, tk.END)
        entry.insert(0, f"{float(value):.0f}")

    def update_slider(self, param, slider):
        """Synchroniseer slider als invoerveld wordt aangepast."""
        slider, entry = self.entries[param]
        try:
            value = float(entry.get())
            if self.parameters[param]["min"] <= value <= self.parameters[param]["max"]:
                slider.set(value)
            else:
                raise ValueError("Waarde buiten bereik")
        except ValueError:
            # Reset invoerveld naar huidige sliderwaarde
            entry.delete(0, tk.END)
            entry.insert(0, f"{slider.get():.0f}")

    def calculate(self):
        """Verzamel waarden en roep berekeningen aan."""
        values = {}
        for param, (slider, _) in self.entries.items():
            values[param] = float(slider.get())
        
        # Berekeningen doorgeven aan haber_bosch_simulatie
        resultaat = bereken_opbrengst(
            druk=values["Druk (atm)"],
            temperatuur=values["Temperatuur (°C)"],
            stroomsnelheid=values["Stroomsnelheid (m³/u)"],
            zuivering=values["Zuivering (%)"],
            koeling=values["Koeling (°C)"],
        )
        
        # Toon resultaten
        for widget in self.output_frame.winfo_children():
            widget.destroy()

        # Maak een frame voor de resultaten
        results_frame = ttk.Frame(self.output_frame)
        results_frame.pack(pady=10)

        # Labels voor opbrengsten
        opbrengst_labels = [
            f"Opbrengst: {resultaat['opbrengst_ton']:.2f} ton ammoniak",
            f"Omzet: €{resultaat['omzet']:.2f} k"  # Marktprijs blijft in euro's
        ]

        # Labels voor kosten (in duizenden euro's)
        variabele_kosten = resultaat['opbrengst_ton'] * 170 / 1000  # Variabele kosten in duizenden euro's
        vaste_kosten = 40000 / 1000  # Vaste kosten in duizenden euro's
        totale_kosten = resultaat['totale_kosten'] / 1000  # Totale kosten in duizenden euro's

        kosten_labels = [
            f"Variabele kosten: €{variabele_kosten:.2f} K",
            f"Vaste kosten: €{vaste_kosten:.2f} K",
            f"Totaal kosten: €{(vaste_kosten + variabele_kosten):.2f} K",
        ]

        # Voeg kopteksten toe
        opbrengst_header = ttk.Label(results_frame, text="Opbrengsten", font=("Arial", 12, "bold"))
        opbrengst_header.grid(row=0, column=0, sticky="w", pady=5)

        kosten_header = ttk.Label(results_frame, text="Kosten", font=("Arial", 12, "bold"))
        kosten_header.grid(row=0, column=1, sticky="w", pady=5)

        # Voeg opbrengst labels toe aan het frame
        for idx, label_text in enumerate(opbrengst_labels):
            label = ttk.Label(results_frame, text=label_text)
            label.grid(row=idx + 1, column=0, sticky="w", padx=10)

        # Voeg kosten labels toe aan het frame
        for idx, label_text in enumerate(kosten_labels):
            label = ttk.Label(results_frame, text=label_text)
            label.grid(row=idx + 1, column=1, sticky="w", padx=10)

        # Winst label met kleur
        winst_label_text = f"Winst: €{resultaat['winst']:.2f} K"
        winst_label = ttk.Label(self.output_frame, text=winst_label_text, font=("Arial", 16, "bold"))

        if resultaat['winst'] >= 0:
            winst_label.config(foreground="green")  # Groene kleur voor positieve winst
        else:
            winst_label.config(foreground="red")    # Rode kleur voor negatieve winst

        winst_label.pack(anchor="center", pady=(20, 0))  # Ruimte boven de winst

# Start de UI
if __name__ == "__main__":
    root = tk.Tk()
    app = HaberBoschUI(root)
    root.mainloop()
