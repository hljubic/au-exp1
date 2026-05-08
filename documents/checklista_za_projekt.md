# Analitika učenja - checklista za ispit

Ovaj dokument služi kao praktična checklista za izradu projekta.

Student treba imati projekt koji pokazuje cijeli tok rada:

1. analiza podataka u Jupyter notebooku
2. treniranje regresijskog i klasifikacijskog deep learning modela
3. spremanje modela i preprocess artefakata
4. backend API koji koristi spremljene modele
5. frontend koji prikazuje dataset, grafikone i predikcije

## Predaja projekta na GitHub

Projekt mora biti predan kroz dva odvojena GitHub repozitorija:

- backend repozitorij
- frontend repozitorij

Backend repozitorij mora sadržavati:

- Flask backend
- Jupyter notebook s eksperimentima
- spremljene modele
- spremljene encodere i scalere
- upute za pokretanje backenda

Frontend repozitorij mora sadržavati:

- Vue frontend aplikaciju
- upute za pokretanje frontenda

Prije ispitnog roka student mora poslati na mail `hrvoje.ljubic@fpmoz.sum.ba`:

- link na backend repozitorij
- link na frontend repozitorij

## 1. Minimum za prolaz

Za prolaz projekt mora imati:

- Jupyter notebook s cijelim postupkom rada
- regresijski deep learning model
- klasifikacijski deep learning model
- evaluaciju oba modela na test skupu
- spremljene modele i sve potrebne artefakte
- backend koji učitava spremljene artefakte i vraća predikcije
- frontend s minimalno tri stranice
- jasnu vezu između notebooka, backenda i frontenda

Student mora znati objasniti svaki dio projekta, ne samo pokrenuti gotov kod.

## 2. Checklista za Jupyter notebook

Notebook mora sadržavati:

- učitavanje dataseta
- kratak opis dataseta
- popis kolona i objašnjenje važnih kolona
- provjeru nedostajućih vrijednosti
- osnovno čišćenje podataka
- osnovnu eksploratornu analizu podataka
- barem nekoliko grafova za razumijevanje dataseta
- jasno definirane ulazne značajke
- jasno definiranu ciljnu varijablu za regresiju
- jasno definiranu ciljnu varijablu za klasifikaciju
- train/validation/test split
- objašnjenje zašto se koristi train, validation i test skup
- encoding kategorijskih varijabli
- scaling numeričkih varijabli ako je potreban
- fitting encodera i scalera samo na train skupu
- transformaciju validation i test skupa istim artefaktima
- regresijski deep learning model
- klasifikacijski deep learning model
- treniranje oba modela
- praćenje train i validation rezultata
- objašnjenje overfittinga ili underfittinga ako se pojave
- korištenje early stoppinga ili drugog oblika regularizacije ako ima smisla
- vrednovanje regresijskog modela na test skupu
- vrednovanje klasifikacijskog modela na test skupu
- spremanje modela
- spremanje encodera
- spremanje scalera
- kratko objašnjenje konačnih rezultata

Regresijski model mora imati metrike:

- MAE
- MSE
- RMSE
- R2

Klasifikacijski model mora imati metrike:

- accuracy
- precision
- recall
- F1
- konfuzijsku matricu

Grafički prikazi na test skupu:

- konfuzijska matrica za klasifikaciju
- linijski grafikon stvarnih i predviđenih vrijednosti za regresiju
- po mogućnosti dodatni grafovi koji objašnjavaju kvalitetu modela

## 3. Checklista za backend

Backend mora imati:

- Flask aplikaciju
- uključeni CORS ako frontend i backend rade odvojeno
- učitavanje dataseta za osnovne informacije i grafikone
- učitavanje spremljenog regresijskog modela
- učitavanje spremljenog klasifikacijskog modela
- učitavanje svih potrebnih encodera
- učitavanje svih potrebnih scalera
- API rutu za osnovne informacije o datasetu
- API rutu za podatke koji se prikazuju u grafikonima
- API rutu za regresijsku predikciju
- API rutu za klasifikacijsku predikciju
- primanje podataka preko JSON-a
- provjeru jesu li poslana sva obavezna polja
- vraćanje jasne greške ako podaci nisu ispravni
- isti preprocessing kao u notebooku
- isti redoslijed ulaznih značajki kao u notebooku
- `inverse_transform` kod regresije ako je ciljna varijabla skalirana
- vraćanje predikcije kao JSON odgovor
- jasne nazive polja u JSON odgovoru

Backend ne smije:

- ponovno trenirati model pri svakom API pozivu
- koristiti drugačiji preprocessing nego notebook
- vraćati lažne ili hardkodirane rezultate
- ignorirati greške u ulaznim podacima

## 4. Checklista za frontend

Frontend mora imati minimalno tri stranice:

- stranicu s osnovnim svojstvima dataseta
- stranicu s grafikonima
- stranicu za predikcije

Stranica s osnovnim svojstvima dataseta treba prikazati:

- naziv ili opis dataseta
- broj redaka
- broj stupaca
- popis važnih kolona
- osnovne statistike
- kratke uvide iz podataka

Stranica s grafikonima treba prikazati:

- barem nekoliko grafikona nad datasetom
- grafikone koji imaju smisla za odabrani problem
- podatke dohvaćene s backenda
- uredan prikaz na većim i manjim ekranima

Stranica za predikcije treba imati:

- formu za unos podataka
- padajuće izbornike za kategorijske vrijednosti
- numerička polja za numeričke vrijednosti
- slanje podataka backendu
- prikaz regresijske predikcije
- prikaz klasifikacijske predikcije
- prikaz greške ako backend vrati grešku
- loading stanje dok se čeka odgovor

Frontend ne smije:

- sam izmišljati rezultat predikcije
- raditi predikciju bez backenda
- slati JSON koji ne odgovara backendu
- prikazivati nejasne ili nečitljive rezultate

## 5. Što se očekuje za veću ocjenu

Za veću ocjenu student treba pokazati da razumije odluke u projektu i da nije samo kopirao template.

Očekuje se:

- kreativniji odabir dataseta
- smisleno odabrane ulazne značajke
- jasno obrazložen izbor ciljne varijable
- više eksperimenata u notebooku
- usporedba više arhitektura modela
- usporedba različitih hiper-parametara
- usporedba različitih preprocessing pristupa
- objašnjenje zašto je odabran konačni model
- bolja interpretacija metrika
- jasna rasprava o greškama modela
- prepoznavanje overfittinga i underfittinga
- smisleni dodatni grafovi
- uredan i razumljiv backend kod
- validacija ulaznih podataka na backendu
- bolja obrada grešaka
- bolji UX na frontendu
- responzivan frontend
- vizualno uredna i profesionalna stranica
- jasna navigacija kroz aplikaciju
- razumljiv prikaz rezultata korisniku

Za veću ocjenu ocjenjuje se i izgled stranice.

To znači:

- layout treba biti uredan
- stranice trebaju biti pregledne
- boje i razmaci trebaju biti konzistentni
- grafikoni trebaju biti čitljivi
- forme trebaju biti jednostavne za korištenje
- rezultati predikcije trebaju biti jasno istaknuti
- aplikacija treba dobro izgledati na različitim veličinama ekrana

## 6. Završna provjera prije predaje

Prije predaje student treba provjeriti:

- backend se pokreće bez greške
- frontend se pokreće bez greške
- frontend može dohvatiti podatke s backenda
- regresijska predikcija radi
- klasifikacijska predikcija radi
- grafikoni se prikazuju
- notebook se može pročitati od početka do kraja
- modeli i artefakti postoje u projektu
- README ili upute objašnjavaju kako pokrenuti projekt
- student zna objasniti cijeli tok rada od dataseta do frontenda

Ako student ne zna objasniti neki dio projekta, taj dio se ne može smatrati stvarno izrađenim.
