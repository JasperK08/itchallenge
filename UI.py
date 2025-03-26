import tkinter as tk
from tkinter import ttk, messagebox
from haber_bosch_simulatie import HaberBoschSimulatie

class HaberBoschApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Haber-Bosch Simulatie")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Titel label
        ttk.Label(root, text="🌿 Haber-Bosch Simulatie 🌿", font=("Arial", 14, "bold")).pack(pady=10)

        # Frame voor sliders
        frame = ttk.Frame(root)
        frame.pack(pady=10)

        # Parameters, limieten en standaardwaarden
        self.labels = [
            "Druk (atm)", 
            "Temperatuur (°C)", 
            "Stroomsnelheid (m³/u)", 
            "Zuivering (%)", 
            "Koeling (°C)"
        ]
        self.limieten = [
            (100, 1000, 200),  # (min, max, default)
            (200, 600, 450),
            (10600, 16600, 16000),
            (0, 100, 25),
            (-150, 90, 20)
        ]
        self.sliders = []
        self.values = []

        for i, (label, (min_w, max_w, default)) in enumerate(zip(self.labels, self.limieten)):
            ttk.Label(frame, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            slider = ttk.Scale(frame, from_=min_w, to=max_w, orient="horizontal", command=lambda val, idx=i: self.update_label(val, idx))
            slider.set(default)
            slider.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            value_label = ttk.Label(frame, text=f"{default:.0f}")
            value_label.grid(row=i, column=2, padx=10, pady=5, sticky="w")
            self.sliders.append(slider)
            self.values.append(value_label)

        # Katalysator-keuzemenu
        ttk.Label(frame, text="Katalysator").grid(row=len(self.labels), column=0, padx=10, pady=5, sticky="w")
        self.katalysator_var = tk.StringVar(value="normaal")
        ttk.Combobox(frame, textvariable=self.katalysator_var, values=["normaal", "verbeterd", "erg goed"], state="readonly").grid(row=len(self.labels), column=1, padx=10, pady=5)

        # Bereken-knop
        ttk.Button(root, text="Bereken", command=self.bereken).pack(pady=15)

        # Resultaat-weergave
        self.resultaat_label = ttk.Label(root, text="", font=("Arial", 12), justify="left")
        self.resultaat_label.pack(pady=10)

    def update_label(self, value, index):
        """Update het label bij de slider om de huidige waarde weer te geven."""
        self.values[index].config(text=f"{float(value):.0f}")

    def bereken(self):
        try:
            # Invoer verzamelen van sliders
            waarden = [slider.get() for slider in self.sliders]

            # Simulatie uitvoeren
            simulatie = HaberBoschSimulatie(*waarden, self.katalysator_var.get())
            resultaten = simulatie.bereken_resultaten()

            # Resultaat tonen
            opbrengst = resultaten['opbrengst_ton']
            omzet = resultaten['omzet_duizend']
            totale_kosten = resultaten['totale_kosten_duizend']
            winst = resultaten['winst_duizend']

            resultaat_tekst = f"""
            🌍 Opbrengst: {opbrengst:.2f} ton
            💰 Omzet: €{omzet:.2f}K
            📉 Totale kosten: €{totale_kosten:.2f}K
            📈 Winst: €{winst:.2f}K
            """
            
            # Kleur afhankelijk van winst of verlies
            if winst < 0:
                kleur = "red"
            else:
                kleur = "green"

            self.resultaat_label.config(text=resultaat_tekst, foreground=kleur)

        except ValueError as e:
            messagebox.showerror("Foutmelding", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = HaberBoschApp(root)
    root.mainloop()

