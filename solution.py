import sys
from collections import deque


def provjeriNIL(komplementCilja) :
  #Provjeravamo ako postoji u istom skupu komplementirani literal i nekomplementirani literal
  #I ako postoji ispisujemo da smo nasli NIL.
  for literal in komplementCilja:
    if komplementirajLiteral(literal) in komplementCilja :
      return True, literal
  return False, None

def procitajFile(fileDatoteka) :
    #citanje dokumenta
    file = open(fileDatoteka, "r", encoding="utf-8")
    sadrzajFile = file.read()

    splitajUlaz = sadrzajFile.strip().split("\n")
    komentari = []

    #uklanjanje komentara

    for line in splitajUlaz :
      if line[0] == "#":
        komentari.append(line)
    for line in komentari :
      splitajUlaz.remove(line)
    
    return splitajUlaz

def rijesiDisjunkciju(klauzule) :
  #uklanjamo " v " ili " V " izmedu literala i dobijamo klauzule bez njih
  ukupneKlauzule = []
  for line in klauzule :
    makniDisjunkciju = line.replace(" V ", " ").replace(" v ", " ")
    ukupneKlauzule.append(makniDisjunkciju.lower())
  return ukupneKlauzule


def identificirajCiljnuKlauzulu(klauzule) :
  
  spremiListu = []
  for klauzula in klauzule :
    podijeliKlauzule = klauzula.split()
    spremiListu.append(podijeliKlauzule)
  return spremiListu[-1]

def komplementirajLiteral(literal) :
  #radi komplement od literala
  if literal.startswith("~"):
    return literal[1:]
  else :
    return "~" + literal
  
def rezuliraj(klauzula1, klauzula2):
  
  klauzula1Set = set(klauzula1.split())
  klauzula2Set = set(klauzula2.split())
  
  novaResolventa = set()
  

  for literal in klauzula1Set :
    if komplementirajLiteral(literal) in klauzula2Set :
      novaKlauzula = klauzula1Set.copy()
      novaKlauzula.update(klauzula2Set)

      novaKlauzula.remove(literal)
      novaKlauzula.remove(komplementirajLiteral(literal))

      if novaKlauzula :
        novaResolventa.add(" ".join(novaKlauzula))
        break
      else :
        novaResolventa.add("")
        break
  return novaResolventa



def rezolucija(klauzule, ciljnaKlauzula) :
  #Pocetni ispis i priprema za rezoluciju
  for i in range(len(klauzule) -1):
    print(str(i + 1) + ". " + klauzule[i])
  
  skupPotpore = set(klauzule[:-1])
  komplement_cilja = set()
  
  for literal in ciljnaKlauzula :
    literal = literal.strip()
    
   

    if literal and not literal.isspace():
      if literal.startswith("~"):
        komplement_cilja.add(literal[1:])
      else :
        komplement_cilja.add("~" + literal)
  
  brojKoraka = len(klauzule) - 1


  for komplementCilja in komplement_cilja :
    brojKoraka += 1
    print(str(brojKoraka) + ". " + komplementCilja)
  print("===============")
  #Kraj pocetnog ispisa i kretanje u while petlju
  used_resolvents = set()  
  while True:
        found = False
        noveKlauzule = set()
        #print("Ovo je ciljno stanje: " + str(komplement_cilja))
        for klauzula1 in skupPotpore:
            for klauzula2 in komplement_cilja:
                if (klauzula1, klauzula2) not in used_resolvents and (klauzula2, klauzula1) not in used_resolvents:
                    resolvents = rezuliraj(klauzula1, klauzula2)
                    if resolvents != set() :
                      found = True
                    if "" in resolvents:
                        print("NIL" + " (" + str(klauzula1) + ", " + str(klauzula2) + ")")
                        print("[CONCLUSION]: " + " v ".join(ciljnaKlauzula) + " is true")
                        return
                    noveKlauzule.update(resolvents)
                    if resolvents != set():
                      print(" v ".join(resolvents) + " (" + str(klauzula1) + ", " + str(klauzula2) + ")")
                    used_resolvents.add((klauzula1, klauzula2))
                    if found :
                       break
            if found :
               break
            
        if not noveKlauzule:
            print("[CONCLUSION]: " + " v ".join(ciljnaKlauzula) + " is unknown")
            return

        komplement_cilja.update(noveKlauzule)
        istina, kojiJeLiteral = provjeriNIL(komplement_cilja)
        if istina:
            print("NIL" + " (" + kojiJeLiteral + ", " + str(komplementirajLiteral(kojiJeLiteral)) + ")")
            print("[CONCLUSION]: " + " v ".join(ciljnaKlauzula) + " is true")
            return

def rezulirajCooking(klauzula1, klauzula2):
  
  klauzula1Set = set(klauzula1.split())
  klauzula2Set = set(klauzula2.split())
  
  novaResolventa = set()

  for literal in klauzula1Set :
    if komplementirajLiteral(literal) in klauzula2Set :
      novaKlauzula = klauzula1Set.copy()
      novaKlauzula.update(klauzula2Set)

      novaKlauzula.remove(literal)
      novaKlauzula.remove(komplementirajLiteral(literal))

      if novaKlauzula :
        novaResolventa.add(" ".join(novaKlauzula))
      else :
        novaResolventa.add("")
  return novaResolventa



def rezolucijaCooking(klauzule, ciljnaKlauzula) :
  #Pocetni ispis i priprema za rezoluciju
  for i in range(len(klauzule) -1):
    print(str(i + 1) + ". " + klauzule[i])
  
  skupPotpore = set(klauzule[:-1])
  komplement_cilja = set()
  
  for literal in ciljnaKlauzula :
    literal = literal.strip()
    
    #https://www.geeksforgeeks.org/python-test-if-string-contains-alphabets-and-spaces/
    #Uzeo za kako provjerit je li neka varijabla ima neki znak osim razmaka

    if literal and not literal.isspace():
      if literal.startswith("~"):
        komplement_cilja.add(literal[1:])
      else :
        komplement_cilja.add("~" + literal)
  
  brojKoraka = len(klauzule) - 1


  for komplementCilja in komplement_cilja :
    brojKoraka += 1
    print(str(brojKoraka) + ". " + komplementCilja)
  print("===============")
  #Kraj pocetnog ispisa i kretanje u while petlju
  used_resolvents = set()  
  while True:
        found = False
        noveKlauzule = set()
        #print("Ovo je ciljno stanje: " + str(komplement_cilja))
        for klauzula1 in skupPotpore:
            for klauzula2 in komplement_cilja:
                if (klauzula1, klauzula2) not in used_resolvents and (klauzula2, klauzula1) not in used_resolvents:
                    resolvents = rezuliraj(klauzula1, klauzula2)
                    if resolvents != set() :
                      found = True
                    if "" in resolvents:
                        print("NIL" + " (" + str(klauzula1) + ", " + str(klauzula2) + ")")
                        print("[CONCLUSION]: " + " v ".join(ciljnaKlauzula) + " is true")
                        return
                    noveKlauzule.update(resolvents)
                    if resolvents != set():
                      print(" v ".join(resolvents) + " (" + str(klauzula1) + ", " + str(klauzula2) + ")")
                    used_resolvents.add((klauzula1, klauzula2))
                    if found :
                       break
            if found :
               break
            
        if not noveKlauzule:
            print("[CONCLUSION]: " + " v ".join(ciljnaKlauzula) + " is unknown")
            return

        komplement_cilja.update(noveKlauzule)
        istina, kojiJeLiteral = provjeriNIL(komplement_cilja)
        if istina:
            print("NIL" + " (" + kojiJeLiteral + ", " + str(komplementirajLiteral(kojiJeLiteral)) + ")")
            print("[CONCLUSION]: " + " v ".join(ciljnaKlauzula) + " is true")
            return
        
def komplementarniDaNe(literali):
   for literal in literali :
      if not literal.startswith("~") :
         komplement = "~" + literal
      else :
         komplement = literal[1:]
      if komplement in literali :
         return True
   return False

def ukloni_nepotrebne_klauzule(klauzule):
    klauzule = klauzule[:-1]  
    spojiKlauzuleiSortiraj = []
    klauzuleBezKomp = []
    for klauzula in klauzule:
        literali = set(klauzula.split())
        if not komplementarniDaNe(literali):
           klauzuleBezKomp.append(literali)

    vratiNajboljeKlauzule = klauzuleBezKomp.copy()
    for trenutna_klauzula in klauzuleBezKomp:
       
        for druga_klauzula in klauzuleBezKomp:
            if trenutna_klauzula > druga_klauzula and druga_klauzula.issubset(trenutna_klauzula):
                vratiNajboljeKlauzule.remove(trenutna_klauzula)
                break
    
    for klauzula in vratiNajboljeKlauzule :
       klauzulaSacuvaj = " ".join(sorted(klauzula))
       spojiKlauzuleiSortiraj.append(klauzulaSacuvaj)
    return spojiKlauzuleiSortiraj


def ukloni_nepotrebne_klauzuleCooking(klauzule):
    spojiKlauzuleiSortiraj = []
    klauzuleBezKomp = []
    for klauzula in klauzule:
        literali = set(klauzula.split())
        if not komplementarniDaNe(literali):
           klauzuleBezKomp.append(literali)

    vratiNajboljeKlauzule = klauzuleBezKomp.copy()
    for trenutna_klauzula in klauzuleBezKomp:
       
        for druga_klauzula in klauzuleBezKomp:
            if trenutna_klauzula > druga_klauzula and druga_klauzula.issubset(trenutna_klauzula):
                vratiNajboljeKlauzule.remove(trenutna_klauzula)
                break
    
    for klauzula in vratiNajboljeKlauzule :
       klauzulaSacuvaj = " ".join(sorted(klauzula))
       spojiKlauzuleiSortiraj.append(klauzulaSacuvaj)
    return spojiKlauzuleiSortiraj


argumenti = sys.argv

def ocistiTautologije(klauzule) :
  cisteKlauzule = []
  for klauzula in klauzule:
        literali = set(klauzula.split())
        imaTautologiju = False
        for literal in literali:
            if komplementirajLiteral(literal) in literali:
                imaTautologiju = True
                break
        if not imaTautologiju:
            cisteKlauzule.append(klauzula)
  return cisteKlauzule


for argument in argumenti :
  if argument == "resolution":
    sacuvajIndexRezolucije = argumenti.index("resolution")
    sljedeciIndexDatoteke = argumenti[sacuvajIndexRezolucije + 1]

    klauzule = procitajFile(sljedeciIndexDatoteke)
    
    klauzule = rijesiDisjunkciju(klauzule)
    
    ciljnaKlauzula = identificirajCiljnuKlauzulu(klauzule)
    
    klauzule = ukloni_nepotrebne_klauzule(klauzule)
    klauzule = ocistiTautologije(klauzule)
    klauzule.append(ciljnaKlauzula) 
    

    rezultat = rezolucija(klauzule,ciljnaKlauzula)
  if argument == "cooking" :
     sacuvajIndexCookinga = argumenti.index("cooking")
     sljedeciIndexDatoteke = argumenti[sacuvajIndexCookinga + 1]

     klauzule = procitajFile(sljedeciIndexDatoteke)
     
     klauzule = rijesiDisjunkciju(klauzule)
     
     klauzule = ukloni_nepotrebne_klauzuleCooking(klauzule)
  
     klauzule = ocistiTautologije(klauzule)

     sljedeciIndexUputaDatoteke = argumenti[sacuvajIndexCookinga + 2]

     naredbe = procitajFile(sljedeciIndexUputaDatoteke)
     proba = klauzule
     i = 0
     for naredba in naredbe :
        i += 1
        prviZnak = None
        #uzeo za splitanje po zadnjem element tj razmaku u ovom slucaju s ove stranice :
        #https://www.geeksforgeeks.org/python-split-on-last-occurrence-of-delimiter/
        prviZnak, naredbaZnak = naredba.rsplit(" ", 1)
        prviZnak = prviZnak.lower().replace(" v ", " ").replace(" V ", " ")
        print(prviZnak)
        print("Users's command " + naredba)
        if naredbaZnak == "?":
          
          klauzule.append(prviZnak)
          rezolucijaCooking(klauzule, [prviZnak])
          klauzule.remove(prviZnak)
        if naredbaZnak == "+":
          klauzule.append(prviZnak)
          print("Added " + prviZnak)
          
        if naredbaZnak == "-":
          print(prviZnak)
          
          for klauzula in klauzule :
             i = 0
             splitanaKlauzula = klauzula.split()
             for splitana in splitanaKlauzula :
                if splitana not in prviZnak :
                   i = 1
             if i == 0 :
                klauzule.remove(klauzula)
          
          print("removed " + prviZnak)
        
        