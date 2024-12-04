from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Abilita CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Permetti richieste da localhost (sviluppo)
        "https://pietrozoffoli-portfolio.vercel.app"  # Permetti richieste da Vercel
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Puoi aggiungere altri metodi se necessari
    allow_headers=["*"],  # Permetti tutti gli headers
)

@app.get("/dati_atleta")
def get_dati_atleta():
    url = "https://portale.fitet.org/risultati/incontri_atleta_acc.php?ATLETA=810613"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Pagina non disponibile")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []
    
    # Trova tutte le tabelle nella pagina
    tables = soup.find_all("table")
    if not tables:
        raise HTTPException(status_code=404, detail="Nessuna tabella trovata nella pagina")
    
    # Analizza ogni tabella
    for table in tables:
        rows = table.find_all("tr")
        
        # Analizza ogni riga della tabella
        for row in rows:  # Salta la riga dell'intestazione
            cells = row.find_all("td")
            if len(cells) >= 6:  # Assicura che ci siano abbastanza celle
                # Estrai il valore dell'immagine
                img_tag = cells[6].find("img")
                img_src = f"https://portale.fitet.org/{img_tag['src'].lstrip('../')}" if img_tag else "N/A"

                
                data.append({
                    "Giornata": cells[1].text.strip(),
                    "Atleta1": cells[2].text.strip(),
                    "Atleta2": cells[3].text.strip(),
                    "Risultato": f"{cells[4].text.strip()} {cells[5].text.strip()}",
                    "Immagine": img_src
                })
    
    if not data:
        raise HTTPException(status_code=404, detail="Nessun dato trovato nelle tabelle")
    
    return {"atleta_id": 810613, "incontri": data}

