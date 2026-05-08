# Analitika učenja - upute za ispit

Ovaj dokument je kratki vodič za ispit iz kolegija **Analitika učenja**.

Naglasak nije na tome da student samo pokrene gotov kod, nego da zna objasniti cijeli postupak:

- od dataseta
- preko preprocessinga i treniranja modela
- do exporta artefakata
- do backend API-ja
- do prikaza rezultata na frontendu

## Predaja projekta na GitHub

Projekt treba biti organiziran u dva odvojena GitHub repozitorija:

- jedan repozitorij za backend
- jedan repozitorij za frontend

Jupyter notebook s eksperimentima ide u backend repozitorij, zajedno s backend kodom, modelima i potrebnim artefaktima.

Prije ispitnog roka student mora poslati na mail:

```text
hrvoje.ljubic@fpmoz.sum.ba
```

oba linka:

- link na backend repozitorij
- link na frontend repozitorij

## 1. Što se ispituje

Na ispitu se provjerava razumijevanje cijelog toka izgradnje aplikacije koja koristi ML/DL model.

Student mora znati objasniti:

- koji se dataset koristi
- koji su ulazni podaci
- koja je ciljna varijabla
- je li zadatak regresija ili klasifikacija
- kako se radi train/validation/test split
- zašto se spremaju modeli, encodersi i scaleri
- kako backend koristi spremljene artefakte
- kako frontend šalje podatke backendu i prikazuje rezultat

## 2. Što postoji u ovom template projektu

Projekt ima:

- Flask backend u `main.py`
- Vue frontend u folderu `frontend-app`
- podatke u folderu `data`
- spremljene modele i preprocess artefakte u folderu `artifacts`

Glavni dataset u primjeru je:

```text
data/students.csv
```

Primjer predikcije u projektu je predviđanje:

```text
writing score
```

na temelju ulaza kao što su:

- `gender`
- `race/ethnicity`
- `math score`
- `reading score`

## 3. Osnovni flow projekta

Student treba razumjeti ovaj redoslijed:

1. učitati dataset
2. očistiti podatke (vrste čišćenja)
3. odabrati ulazne značajke i ciljnu varijablu
4. napraviti train/validation/test split
5. fitati encodere i scalere samo na train skupu
6. transformirati validation i test istim artefaktima
7. trenirati model
8. odabrati model prema validation rezultatu
9. završno provjeriti/vrednovati model na test skupu
10. spremiti model i sve preprocess artefakte
11. učitati artefakte u backendu
12. napraviti API rutu za predikciju
13. poslati podatke s frontenda
14. prikazati predikciju korisniku

## 4. Train, validation i test skup

Train skup služi za učenje modela.

Validation skup služi za odabir modela, arhitekture i hiper-parametara.

Test skup služi samo za završnu procjenu modela.

Važno pravilo:

```text
Model se ne bira prema test rezultatu.
```

Ako student bira model prema test rezultatu, test skup više nije poštena završna provjera.

## 5. Preprocessing i artefakti

Model ne radi direktno nad sirovim podacima.

Kategorijske vrijednosti treba kodirati, a numeričke vrijednosti često treba skalirati.

Zato se spremaju:

- model
- label encoderi
- scaleri
- drugi preprocess artefakti ako postoje

Backend mora koristiti iste artefakte kao trening dio projekta.

Ako backend drugačije obradi podatke nego trening kod, predikcija može biti pogrešna iako aplikacija formalno radi.

## 6. Backend i API

Backend u ovom projektu:

- učitava dataset
- računa osnovne statistike
- vraća podatke za grafove
- učitava model i artefakte
- prima JSON s frontenda
- radi preprocessing
- poziva model
- vraća predikciju kao JSON

Primjer API rute:

```text
POST /api/predict
```

Frontend šalje JSON, backend vraća rezultat.

## 7. Regresija i klasifikacija

Student mora znati razlikovati regresiju i klasifikaciju.

Regresija predviđa brojčanu kontinuiranu vrijednost.

Primjer:

```text
predviđanje writing score
```

Klasifikacija predviđa klasu ili kategoriju.

Primjer:

```text
predviđanje hoće li student pripadati određenoj grupi uspješnosti
```

Projekt treba imati i regresijski i klasifikacijski zadatak ako je to traženo za završni projekt.

## 8. Izlazne aktivacije

Za regresiju se najčešće koristi linearni izlaz.

Za binarnu klasifikaciju koristi se sigmoid.

Za višeklasnu klasifikaciju koristi se softmax.

Student mora povezati tip problema s izlaznim slojem, loss funkcijom i metrikama.

## 9. Early stopping i weight decay

Early stopping zaustavlja treniranje kada se model prestane poboljšavati na validation skupu.

Weight decay je oblik regularizacije koji penalizira/kažnjava prevelike težine modela.

Oboje pomaže smanjiti overfitting i poboljšati generalizaciju modela.

## 10. Inverse transform

Ako je ciljna varijabla skalirana, model vraća predikciju u skaliranom prostoru.

`inverse_transform` vraća rezultat u originalnu skalu.

Bez toga rezultat može biti tehnički ispravan, ali korisniku nerazumljiv.

## 11. Tipične greške

Student treba znati prepoznati ove greške:

- `fit_transform` na validation ili test skupu
- scaler fitan prije train/test splita (na cijelom datasetu)
- model odabran prema test rezultatu (biramo na validation skupu)
- nespremljen encoder ili scaler (neće biti ispravni rezultati u produkciji)
- drugačiji redoslijed stupaca u backendu
- zaboravljen `inverse_transform` (podaci će u produkciji biti skalirani, a ne stvari)
- kriva aktivacija na izlazu modela

## 12. Minimalno znanje za prolaz

Student za prolaz mora znati:

- pokrenuti backend
- pokrenuti frontend
- objasniti što radi `main.py`
- objasniti odabrani dataset i kako je pre-processed
- objasniti što je model
- objasniti što su artefakti i zašto ih spremamo/koristimo
- objasniti zašto se koristi train/validation/test, a ne samo train/test
- pokazati gdje frontend šalje zahtjev backendu (korištenje network tools)


## 13. Potrebno znanje za veću ocjenu

Za veću ocjenu student ne treba samo znati pokrenuti projekt, nego mora znati objasniti odluke koje su donesene u projektu i predložiti bolje alternative.

Student treba znati objasniti:

- zašto su odabrane baš te ulazne značajke i ciljna varijabla
- kako bi se projekt mogao proširiti s dodatnim značajkama (za ovo je se potrebno "unijeti" u podatke)
- koje metrike imaju smisla za regresiju, a koje za klasifikaciju
- zašto se modeli uspoređuju na validation skupu
- kako bi prepoznao overfitting ili underfitting (i kako ih spriječiti)
- kako bi promijenio arhitekturu modela ako rezultati nisu dobri
- koje alternative postoje za encoding kategorijskih varijabli (umjesto LabelEncodera)
- zašto je važno da backend koristi isti preprocessing kao trening kod
- kako bi dodao još jedan prediktivni endpoint u backend
- kako bi frontend prikazao više modelskih rezultata ili usporedbu predikcija

Za veću ocjenu student bi trebao znati raspraviti i konkretne alternative:

- `LabelEncoder` u odnosu na `OneHotEncoder` - način funkcioniranja
- `StandardScaler` u odnosu na `MinMaxScaler` ili `RobustScaler` - kako rade
- accuracy, precision, recall i F1 kod klasifikacije (konfuzijska matrica)
- MAE, MSE, RMSE i R2 kod regresije

Student također treba znati prepoznati da dobar projekt nije samo model s dobrim rezultatom, nego cijeli pipeline:

1. ispravan dataset
2. ispravan split
3. ispravan preprocessing
4. ispravno treniranje
5. korektna evaluacija
6. spremljeni artefakti
7. backend koji reproducira isti pipeline
8. frontend koji jasno prikazuje rezultat

## 14. Kratka checklist

Prije ispita student treba moći odgovoriti:

- Znam li objasniti dataset?
- Znam li objasniti ulaze i izlaz modela?
- Znam li objasniti train/validation/test?
- Znam li objasniti zašto spremamo scalere i encodere?
- Znam li objasniti što backend radi prije predikcije?
- Znam li objasniti kako frontend dobije rezultat?
- Znam li prepoznati pogrešan redoslijed preprocessinga?

Ako student zna objasniti ove točke, razumije osnovu projekta.
