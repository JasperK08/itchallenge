import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  
from haber_bosch_simulatie import HaberBoschSimulatie
import time  

class RoundedFrame(ttk.Frame):
    """Een frame met afgeronde hoeken"""
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(borderwidth=10, relief="ridge")

class RoundedButton(ttk.Button):
    """Een knop met afgeronde hoeken"""
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs, style="Rounded.TButton")

class HaberBoschApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Haber-Bosch Simulatie")
        self.root.geometry("1920x1080")  
        self.root.resizable(False, False)

        # 🎨 **Stijlen**
        style = ttk.Style()
        style.configure("Rounded.TButton", font=("Arial", 14), padding=10, relief="flat")
        style.configure("Rounded.TFrame", borderwidth=5, relief="ridge")
        style.configure("TLabel", font=("Arial", 14), background="white", padding=5)

        # 🖼️ **Achtergrondafbeelding**
        self.background_image = Image.open("new-logo.png")  
        self.background_image = self.background_image.resize((1920, 1080), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.background_image)

        self.bg_label = ttk.Label(root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  

        # 📽️ **GIF laden**
        self.gif_frames = []
        self.current_frame = 0
        self.load_gif("haberbosch.gif")

        # Label voor de GIF
        self.gif_label = ttk.Label(root, background="white")
        self.gif_label.place(relx=0.85, rely=0.2, anchor="center")  
        self.gif_label.lower()  

        # 🗓️ **Dagweergave**
        self.dag = 1
        self.dag_label = ttk.Label(root, text=f"📅 Dag {self.dag}", font=("Arial", 16, "bold"), foreground="black", background="white", padding=10)
        self.dag_label.place(x=20, y=20)

        # 🌿 **Titel**
        ttk.Label(root, text="🌿 Haber-Bosch Simulatie 🌿", font=("Arial", 24, "bold"), background="white").pack(pady=20)

        # 🎛️ **Frame voor sliders**
        self.frame = RoundedFrame(root, style="Rounded.TFrame")
        self.frame.place(relx=0.5, rely=0.35, anchor="center")  

        # **Sliders + Waarden**
        self.labels = ["Druk (atm)", "Temperatuur (°C)", "Stroomsnelheid (m³/u)", "Spui (%)", "Koeling (°C)"]
        self.limieten = [(100, 1000, 200), (200, 600, 450), (10600, 16600, 16000), (1, 20, 10), (-150, 90, 20)]
        self.sliders = []
        self.values = []

        for i, (label, (min_w, max_w, default)) in enumerate(zip(self.labels, self.limieten)):
            ttk.Label(self.frame, text=label, font=("Arial", 14)).grid(row=i, column=0, padx=20, pady=5, sticky="e")

            # Gebruik StringVar voor dynamische updates
            value_var = tk.StringVar(value=f"{default:.1f}" if label == "Spui (%)" else f"{default:.0f}")
            value_label = ttk.Label(self.frame, textvariable=value_var, font=("Arial", 14))
            value_label.grid(row=i, column=2, padx=20, pady=5, sticky="w")

            slider = ttk.Scale(
                self.frame, from_=min_w, to=max_w, orient="horizontal", 
                command=lambda val, idx=i, var=value_var: self.update_label(val, idx, var)
            )
            slider.set(default)
            slider.grid(row=i, column=1, padx=10, pady=5, sticky="ew")

            self.sliders.append(slider)
            self.values.append(value_var)

        # 🏁 **Knoppen**
        button_frame = ttk.Frame(root)
        button_frame.place(relx=0.5, rely=0.5, anchor="center")  

        bereken_button = RoundedButton(button_frame, text="Bereken", command=self.start_berekening)
        bereken_button.grid(row=0, column=0, padx=10)

        reset_button = RoundedButton(button_frame, text="Reset", command=self.reset)
        reset_button.grid(row=0, column=1, padx=10)

        # 📘 **Uitleg links in beeld**
        uitleg_tekst = """Welkom bij de Haber-Bosch simulatie! 🎉

        🔹 Gebruik de sliders in het midden om instellingen aan te passen.
        🔹 Probeer een zo hoog mogelijke winst te behalen.
        🔹 Bekijk je resultaten per dag in het groene vlak.

        📊 **Belangrijke punten**:
        - 📅 Linksboven zie je de huidige dag. Klik op 'Reset' om opnieuw te beginnen.
        - 📈 In het midden zie je de gemiddelde, minimale en maximale winst.
        - 💰 Na het klikken op 'Bereken' zie je de resultaten van de dag.

        Succes en veel plezier! 🚀"""

        self.uitleg_label = tk.Label(
            root, 
            text=uitleg_tekst, 
            font=("Arial", 12), 
            justify="left",  # Tekst perfect links uitlijnen
            anchor="w",  # Extra truc om de uitlijning strak te houden
            background="#f0f0f0",  
            relief="ridge",  
            wraplength=600,  
            padx=10,  
            pady=10
        )
        self.uitleg_label.place(x=20, y=400)

        # 📊 **Resultaten & gemiddelden naast elkaar**
        self.result_frame = RoundedFrame(root, style="Rounded.TFrame")
        self.result_frame.place(relx=0.5, rely=0.62, anchor="center")  

        self.resultaat_label = ttk.Label(self.result_frame, text="", font=("Arial", 16), justify="left", background="white")
        self.resultaat_label.grid(row=0, column=0, padx=20)

        self.stats_label = ttk.Label(self.result_frame, text="", font=("Arial", 16), justify="left", background="white")
        self.stats_label.grid(row=0, column=1, padx=20)

        # 📈 **Voortgangsbalk**
        self.progress_bar = ttk.Progressbar(root, mode='determinate', length=800)
        self.progress_bar.place(relx=0.5, rely=0.75, anchor="center")  

        # 📊 **Opslag voor winstcijfers**
        self.profits = []

    def load_gif(self, filepath):
        gif = Image.open(filepath)
        try:
            while True:
                frame = gif.copy().convert("RGBA")
                self.gif_frames.append(ImageTk.PhotoImage(frame))
                gif.seek(len(self.gif_frames))
        except EOFError:
            pass  

    def play_gif(self):
        """Speel de GIF af."""
        if self.current_frame < len(self.gif_frames):
            self.gif_label.configure(image=self.gif_frames[self.current_frame])
            self.current_frame += 1
            self.root.after(50, self.play_gif)  # Volgende frame na 50ms
        else:
            self.gif_label.lower()  # Verberg de GIF na afloop

    def update_label(self, value, index, value_var):
        """Update de waarde van de slider."""
        decimal_places = 1 if self.labels[index] == "Spui (%)" else 0
        value_var.set(f"{float(value):.{decimal_places}f}")

    def start_berekening(self):
        """Start de berekening en speel de GIF af."""
        self.progress_bar['value'] = 0  
        self.resultaat_label.config(text="🔄 Bezig met berekenen...")
        self.current_frame = 0  
        self.gif_label.lift()  
        self.play_gif()  # Start de GIF
        self.root.after(100, self.bereken)  

    def bereken(self):
        """Voer de berekening uit en update de resultaten."""
        for i in range(101):
            self.progress_bar['value'] = i
            self.root.update()
            time.sleep(0.02)

        try:
            waarden = [slider.get() for slider in self.sliders]
            simulatie = HaberBoschSimulatie(*waarden, self.sliders[3].get())
            resultaten = simulatie.bereken_resultaten()

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
            kleur = "red" if winst < 0 else "green"
            self.resultaat_label.config(text=resultaat_tekst, foreground=kleur)

            self.dag += 1
            self.dag_label.config(text=f"📅 Dag {self.dag}")

            self.profits.append(winst)
            self.update_stats()

        except ValueError as e:
            messagebox.showerror("Foutmelding", str(e))

        self.progress_bar['value'] = 0

    def update_stats(self):
        """Update de statistieken met gemiddelde, minimale en maximale winst."""
        if self.profits:
            avg_profit = sum(self.profits) / len(self.profits)
            stats_text = f"📊 Gem.: €{avg_profit:.2f}K  🔻 Min.: €{min(self.profits):.2f}K  🔺 Max.: €{max(self.profits):.2f}K"
        else:
            stats_text = "Nog geen data."
        self.stats_label.config(text=stats_text)

    def reset(self):
        """Reset de simulatie."""
        self.dag = 1
        self.dag_label.config(text=f"📅 Dag {self.dag}")
        self.profits = []
        self.update_stats()

if __name__ == "__main__":
    root = tk.Tk()
    app = HaberBoschApp(root)
    root.mainloop()
