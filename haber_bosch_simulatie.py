def bereken_opbrengst(druk, temperatuur, stroomsnelheid, spui, koeling, katalysator):
    """
    Bereken de opbrengst, omzet, kosten en winst van ammoniakproductie op basis van parameters.
    """
    # Basisparameters
    basis_opbrengst = 1400  # ton ammoniak onder ideale omstandigheden
    variabele_kosten_per_ton = 160  # € per ton
    vaste_kosten = 50000  # €
    marktprijs_per_ton = 210  # €

    # Effect van katalysator
    if katalysator == "verbeterd":
        vaste_kosten += 20000
        marktprijs_per_ton *= 1.03
    elif katalysator == "erg goed":
        vaste_kosten += 30000
        marktprijs_per_ton *= 1.06

   

   
class HaberBoschSimulatie:
    # Constante waarden voor berekeningen
    BASIS_OPBRENGST = 1400  # ton ammoniak onder ideale omstandigheden
    VARIABELE_KOSTEN_PER_TON = 160  # € per ton
    VASTE_KOSTEN = 50000  # € 
    MARKTPRIJS_PER_TON = 210  # €

    # Parametergrenzen
    PARAMETER_LIMITS = {
        "druk": (100, 1000),  # atm
        "temperatuur": (200, 600),  # °C
        "stroomsnelheid": (10600, 16600),  # m³/u
        "spui": (1, 20),  # %
        "koeling": (-150, 90),  # °C
    }

    def __init__(self, druk, temperatuur, stroomsnelheid, spui, koeling, katalysator):
        self.druk = self.valideer_parameter("druk", druk)
        self.temperatuur = self.valideer_parameter("temperatuur", temperatuur)
        self.stroomsnelheid = self.valideer_parameter("stroomsnelheid", stroomsnelheid)
        self.spui = self.valideer_parameter("spui", spui)
        self.koeling = self.valideer_parameter("koeling", koeling)
        self.katalysator = katalysator.lower() if katalysator in ["normaal", "verbeterd", "erg goed"] else "normaal"

    def valideer_parameter(self, naam, waarde):
        min_w, max_w = self.PARAMETER_LIMITS[naam]
        if not (min_w <= waarde <= max_w):
            raise ValueError(f"{naam.capitalize()} moet tussen {min_w} en {max_w} liggen.")
        return waarde

    def bereken_efficiëntie(self):
        # Factoren berekenen op basis van afwijking van optimale waarden
        factoren = {
            "druk": 1 - abs((250 - self.druk) / 250) * 0.1,
            "temperatuur": 1 - abs((425 - self.temperatuur) / 425) * 0.15,
            "stroomsnelheid": 1 - abs((15500 - self.stroomsnelheid) / 15500) * 0.15,
            "spui": 1 - (self.spui - 3) / 20 * 0.15,
            "koeling": 1 - abs((10 - self.koeling) / 100) * 0.15,
        }
        efficiëntie = max(0, factoren["druk"] * factoren["temperatuur"] * factoren["stroomsnelheid"] * factoren["spui"] * factoren["koeling"])
        
        # Effect van katalysator
        katalysator_factoren = {"normaal": 1, "verbeterd": 1.03, "erg goed": 1.06}
        efficiëntie *= katalysator_factoren[self.katalysator]
        
        return efficiëntie

    def bereken_resultaten(self):
        efficiëntie = self.bereken_efficiëntie()
        opbrengst = max(0, self.BASIS_OPBRENGST * efficiëntie)
        variabele_kosten = opbrengst * self.VARIABELE_KOSTEN_PER_TON
        totale_kosten = self.VASTE_KOSTEN + variabele_kosten
        omzet = opbrengst * self.MARKTPRIJS_PER_TON
        winst = omzet - totale_kosten

        return {
            "opbrengst_ton": opbrengst,
            "omzet_duizend": omzet / 1000,
            "totale_kosten_duizend": totale_kosten / 1000,
            "winst_duizend": winst / 1000,
        }

# Testcode voor directe uitvoering
if __name__ == "__main__":
    try:
        simulatie = HaberBoschSimulatie(250, 425, 15500, 3, 10, "verbeterd")
        resultaten = simulatie.bereken_resultaten()
        for key, value in resultaten.items():
            print(f"{key}: {value:.2f}")
    except ValueError as e:
        print(f"Fout: {e}")
