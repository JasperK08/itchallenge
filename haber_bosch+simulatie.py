# haber_bosch_simulatie.py

class HaberBoschSimulation:
    THEORETISCHE_HOEVEELHEID = 1500  # ton
    GEMIDDELDE_OPBRENGST = 1200  # ton
    VARIABELE_KOSTEN_PER_TON = 800  # € per ton
    VASTE_KOSTEN = 40000  # €
    
    # Min en Max waarden
    MIN_DRUK = 100  # atm
    MAX_DRUK = 1000  # atm
    MIN_TEMPERATUUR = 200  # °C
    MAX_TEMPERATUUR = 600  # °C
    MIN_stroomsnelheid = 10600  # m³/u
    MAX_stroomsnelheid = 16600  # m³/u
    MIN_ZUIVERING = 0  # %
    MAX_ZUIVERING = 100  # %
    MIN_KOELING = -150  # °C
    MAX_KOELING = 90  # °C

    def __init__(self, druk, temperatuur, stroomsnelheid, zuivering, koeling):
        # Validatie van de invoerwaarden
        if not (self.MIN_DRUK <= druk <= self.MAX_DRUK):
            raise ValueError(f"Druk moet tussen {self.MIN_DRUK} en {self.MAX_DRUK} atm liggen.")
        if not (self.MIN_TEMPERATUUR <= temperatuur <= self.MAX_TEMPERATUUR):
            raise ValueError(f"Temperatuur moet tussen {self.MIN_TEMPERATUUR} en {self.MAX_TEMPERATUUR} °C liggen.")
        if not (self.MIN_stroomsnelheid <= stroomsnelheid <= self.MAX_stroomsnelheid):
            raise ValueError(f"Stroomsnelheid moet tussen {self.MIN_stroomsnelheid} en {self.MAX_stroomsnelheid} m³/u liggen.")
        if not (self.MIN_ZUIVERING <= zuivering <= self.MAX_ZUIVERING):
            raise ValueError(f"Zuivering moet tussen {self.MIN_ZUIVERING} en {self.MAX_ZUIVERING} % liggen.")
        if not (self.MIN_KOELING <= koeling <= self.MAX_KOELING):
            raise ValueError(f"Koeling moet tussen {self.MIN_KOELING} en {self.MAX_KOELING} °C liggen.")
        
        self.druk = druk  # atm
        self.temperatuur = temperatuur  # °C
        self.stroomsnelheid = stroomsnelheid  # m³/u
        self.zuivering = zuivering  # %
        self.koeling = koeling  # °C

def bereken_opbrengst(druk, temperatuur, stroomsnelheid, zuivering, koeling, ):
    """
    Bereken de opbrengst, omzet, kosten en winst van ammoniakproductie op basis van parameters.
    """
    # Parameters    
    theoretisch = 1500  # Theoretische hoeveelheid ammoniak in ton
    variabele_kosten_per_ton = 170  # Variabele kosten per ton (€)
    vaste_kosten = 60000  # Vaste kosten (€)
    marktprijs_per_ton = 350  # Marktprijs van ammoniak per ton (€)

    # Afwijkingen berekenen
    afwijking_druk = abs((200 - druk) / 200) * 0.1
    afwijking_temp = abs((450 - temperatuur) / 450) * 0.1
    afwijking_stroomsnelheid = abs((16000 - stroomsnelheid) / 16000) * 0.1
    afwijking_zuivering = abs((25 - zuivering) / 25) * 0.1
    afwijking_koeling = abs((20 - koeling) / 20 ) * 0.06
    

    # Totale afwijking berekenen
    totale_afwijking = 1 - (afwijking_druk + afwijking_temp + afwijking_stroomsnelheid + afwijking_zuivering + afwijking_koeling)

    # Werkelijke opbrengst berekenen (met 25% reductie)
    werkelijke_opbrengst = max(0, totale_afwijking * theoretisch * 0.75)

    # Kosten berekenen
    variabele_kosten = werkelijke_opbrengst * variabele_kosten_per_ton
    totale_kosten = vaste_kosten + variabele_kosten

    # Omzet berekenen
    omzet = werkelijke_opbrengst * marktprijs_per_ton

    # Winst berekenen
    winst = omzet - totale_kosten

    # Resultaat in duizenden euro's
    return {
        "opbrengst_ton": werkelijke_opbrengst,
        "omzet": omzet / 1000,  # Omzet in duizenden euro's
        "totale_kosten": totale_kosten / 1000,  # Totale kosten in duizenden euro's
        "winst": winst / 1000  # Winst in duizenden euro's
    }



    def bereken_kwaliteit(self):
        # Basiswaarden voor ideale omstandigheden
        optimale_temperatuur = 450  # °C
        optimale_druk = 200  # atm
        optimale_stroomsnelheid = 16000  # m³/u

        # Bereken afwijkingen van optimale waarden
        temperatuur_afwijking = abs(self.temperatuur - optimale_temperatuur) / optimale_temperatuur
        druk_afwijking = abs(self.druk - optimale_druk) / optimale_druk
        stroomsnelheid_afwijking = abs(self.stroomsnelheid - optimale_stroomsnelheid) / optimale_stroomsnelheid

        # Bereken totale afwijking (in percentage)
        totale_afwijking = (temperatuur_afwijking + druk_afwijking + stroomsnelheid_afwijking) / 3
        
        return totale_afwijking

    def resultaten(self):
        # Berekeningen
        afwijking_factor = self.bereken_kwaliteit() * 0.1  # Effect van afwijking op opbrengst

        # Bereken de werkelijke opbrengst (in ton)
        werkelijke_opbrengst = self.GEMIDDELDE_OPBRENGST * (1 - afwijking_factor)
        
        # Bereken de yield als percentage van de theoretische hoeveelheid
        opbrengst_percentage = (werkelijke_opbrengst / self.THEORETISCHE_HOEVEELHEID) * 100
        
        # Variabele kosten op basis van geproduceerde ammoniak
        variabele_kosten = werkelijke_opbrengst * self.VARIABELE_KOSTEN_PER_TON
        
        # Totale kosten
        totale_kosten = variabele_kosten + self.VASTE_KOSTEN
        
        # Totale opbrengst
        marktprijs_per_ton = 300  # Voorbeeld marktprijs per ton NH3 in €
        totale_opbrengst = werkelijke_opbrengst * marktprijs_per_ton
        
        # Winst
        winst = totale_opbrengst - totale_kosten
        
        return {
            "Werkelijke opbrengst (ton NH3)": werkelijke_opbrengst,
            "Opbrengst als percentage van theoretische hoeveelheid (%)": opbrengst_percentage,
            "Variabele kosten (€)": variabele_kosten,
            "Vaste kosten (€)": self.VASTE_KOSTEN,
            "Totale kosten (€)": totale_kosten,
            "Marktprijs NH3 (€)": marktprijs_per_ton,
            "Totale opbrengst (€)": totale_opbrengst,
            "Winst (€)": winst,
        }

# Voorbeeld van het aanroepen van de simulatie
if __name__ == "__main__":
    # Voorbeeldparameters
    druk = 200  # atm
    temperatuur = 450  # °C
    stroomsnelheid = 16000  # m³/u
    zuivering = 25  # %
    koeling = 25  # °C

    try:
        simulatie = HaberBoschSimulation(druk, temperatuur, stroomsnelheid, zuivering, koeling)
        resultaten = simulatie.resultaten()

        for key, value in resultaten.items():
            print(f"{key}: {value:.2f}")
    except ValueError as e:
        print(e)
