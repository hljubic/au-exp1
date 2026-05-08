# Analitika učenja - pitanja i odgovori za ispit

Ovaj dokument sadrži praktična pitanja za provjeru razumijevanja projekta iz kolegija **Analitika učenja**.

Pitanja nisu zamišljena kao teorijsko nabrajanje, nego kao provjera zna li student objasniti postojeći projekt, pronaći bitne dijelove koda i prepoznati česte greške u ML/DL pipelineu.

## Dataset i cilj predikcije

| # | Pitanje                                                                                                    | Očekivani odgovor |
|---|------------------------------------------------------------------------------------------------------------|---|
| 1 | Primjer: Zašto se `gender` i `race/ethnicity` moraju kodirati, a `math score` i `reading score` ne moraju? | `gender` i `race/ethnicity` su kategorijske vrijednosti, dok su `math score` i `reading score` već numeričke vrijednosti. |
| 2 | Kako bi student provjerio ima li dataset nedostajućih vrijednosti?                                         | Može koristiti `data.isnull().sum()` i zatim objasniti hoće li redove brisati, popunjavati ili posebno obraditi. |
| 3 | Zašto se scaler ne smije fitati na cijelom datasetu prije train/test podjele? | Zato što bi informacije iz test skupa ušle u preprocessing, pa test rezultat više ne bi bio poštena procjena modela. |
| 4 | Zašto backend mora koristiti isti encoder i scaler koji su korišteni u notebooku? | Zato što model očekuje podatke obrađene na isti način kao tijekom treniranja; drugačiji preprocessing može dati pogrešne predikcije. |
| 5 | Što se može dogoditi ako frontend pošalje JSON s drugačijim nazivima polja nego što backend očekuje? | Backend neće pronaći potrebne vrijednosti i vratit će grešku ili neće moći napraviti predikciju. |
| 6 | Zašto kod regresije često trebamo `inverse_transform` nakon predikcije? | Ako je ciljna varijabla bila skalirana, model vraća skaliranu vrijednost, a `inverse_transform` vraća rezultat u originalnu skalu. |
## Train, validation i test

| # | Pitanje | Očekivani odgovor |
|---|---|---|
| 7 | Objasni ispravan redoslijed: train, validation i test skup. | Train služi za učenje modela, validation za odabir modela i hiper-parametara, a test samo za završnu procjenu. |
| 8 | Zašto model ne smijemo birati prema test rezultatu? | Ako model biramo prema test rezultatu, test skup više nije neovisna završna provjera. |
| 9 | Gdje se smiju fitati encoderi i scaleri? | Smiju se fitati samo na train skupu. |
| 10 | Koja je razlika između `fit_transform` i `transform` u ovom kontekstu? | `fit_transform` uči transformaciju i primjenjuje je, a `transform` samo primjenjuje već naučenu transformaciju. |
| 11 | Navedi primjer data leakage greške u ovom projektu. | Greška je ako se scaler ili encoder fita na cijelom datasetu prije train/validation/test splita. |
| 12 | Kako validation skup pomaže kod early stoppinga? | Early stopping prati validation rezultat i zaustavlja treniranje kad se model prestane poboljšavati. |

## Preprocessing i artefakti

| # | Pitanje | Očekivani odgovor |
|---|---|---|
| 13 | Koje artefakte backend učitava iz foldera `artifacts`? | Učitava model `.keras`, label encodere i scalere potrebne za isti preprocessing kao u treningu. |
| 14 | Zašto nije dovoljno spremiti samo model? | Model očekuje podatke obrađene na isti način kao tijekom treniranja, zato trebaju i encoderi i scaleri. |
| 15 | Što se može dogoditi ako backend koristi drugačiji encoder od onoga iz treninga? | Kategorije se mogu pretvoriti u pogrešne brojeve pa model dobiva krive ulaze. |
| 16 | Zašto je bitan redoslijed stupaca u `input_df`? | Model očekuje značajke istim redoslijedom kao u treningu. |
| 17 | Zašto se koristi `inverse_transform` nad predikcijom? | Zato što model vraća skaliranu vrijednost, a korisniku treba rezultat u originalnoj skali. |
| 18 | Što će se dogoditi ako frontend pošalje kategoriju koju encoder ne poznaje? | Backend će dobiti grešku kod transformacije i treba vratiti jasan error odgovor. |
| 19 | Što znači da backend mora reproducirati trening pipeline? | Backend mora primijeniti isti izbor značajki, isti encoding, isti scaling i isti redoslijed ulaza kao tijekom treniranja. |

## Model, metrika i evaluacija

| # | Pitanje | Očekivani odgovor |
|---|---|---|
| 20 | Koja izlazna aktivacija ima smisla za predviđanje `writing score` i zašto? | Ima smisla linearni izlaz jer se predviđa kontinuirana brojčana vrijednost. |
| 21 | Koji izlazni sloj i loss funkcija imaju smisla za binarnu klasifikaciju? | Najčešće se koristi sigmoid izlaz i `binary_crossentropy`. |
| 22 | Koji izlazni sloj i loss funkcija imaju smisla za višeklasnu klasifikaciju? | Najčešće se koristi softmax izlaz i `categorical_crossentropy` ili `sparse_categorical_crossentropy`. |
| 23 | Koje metrike imaju smisla za regresiju? | Imaju smisla MAE, MSE, RMSE i R2. |
| 24 | Koje metrike imaju smisla za klasifikaciju? | Imaju smisla accuracy, precision, recall, F1 i konfuzijska matrica. |
| 25 | Kako bi student prepoznao overfitting? | Trening rezultat se poboljšava, a validation rezultat stagnira ili se pogoršava. |
| 26 | Kako se može smanjiti overfitting? | Može se koristiti early stopping, weight decay, dropout, jednostavniji model ili više podataka. |
| 27 | Kako bi student prepoznao underfitting? | Model ima loš rezultat i na train skupu i na validation skupu. |
| 28 | Što bi student mogao promijeniti ako model underfitta? | Može povećati kapacitet modela, dodati bolje značajke, trenirati dulje ili prilagoditi learning rate. |

## Backend i API

| # | Pitanje | Očekivani odgovor |
|---|---|---|
| 29 | Objasni što radi funkcija `make_prediction`. | Prima JSON podatke, gradi DataFrame, kodira kategorije, skalira ulaz, poziva model i vraća predikciju u originalnoj skali. |
| 30 | Koja se ruta koristi za predikciju i kojom HTTP metodom? | Koristi se `POST /api/predict`, a u projektu postoji i alias `POST /predict_writing_score`. |
| 31 | Koja polja backend očekuje u JSON zahtjevu za predikciju? | Očekuje `gender`, `race/ethnicity`, `math score` i `reading score`. |
| 32 | Što backend vraća ako nedostaje obavezno polje? | Vraća HTTP 400 i popis polja koja nedostaju. |
| 33 | Zašto je dobro da backend hvata `ValueError`? | Zato da korisnik dobije razumljivu grešku za neispravne ulazne vrijednosti umjesto rušenja aplikacije. |
| 34 | Što vraća ruta `/api/overview` i zašto je korisna? | Vraća osnovne informacije o datasetu, missing values, statistike i insightse za dashboard. |
| 35 | Što vraća ruta `/api/charts` i zašto se vraća JSON? | Vraća podatke za grafikone, a JSON omogućuje frontendu da sam nacrta i prilagodi prikaz. |

## Frontend i komunikacija s backendom

| # | Pitanje | Očekivani odgovor |
|---|---|---|
| 36 | U kojem frontend fileu se šalje zahtjev za predikciju? | Zahtjev se šalje u `frontend-app/src/views/Predict.vue`. |
| 37 | Što radi `@submit.prevent="submitForm"` u formi? | Sprječava klasično slanje forme i refresh stranice te pokreće Vue funkciju za API poziv. |
| 38 | Zašto se koristi `v-model.number` za score polja? | Zato da Vue vrijednost iz inputa pretvori u broj umjesto da ostane string. |
| 39 | Što bi puklo ako backend vrati ključ `prediction`, a frontend očekuje `predicted_writing_score`? | Frontend ne bi prikazao rezultat jer čita krivi naziv polja iz JSON odgovora. |
| 40 | Kako bi student u browseru provjerio šalje li frontend ispravan zahtjev? | Treba otvoriti Network tab, poslati formu i provjeriti URL, metodu, payload i response. |
| 41 | Zašto frontend ne bi trebao sam raditi encoding, scaling i predikciju? | Zato što ta logika pripada backendu koji ima spremljene modele i artefakte iz treninga. |
| 42 | Kako bi student dodao prikaz još jedne predikcije na frontend? | Treba dodati API poziv ili proširiti odgovor backenda, spremiti rezultat u `ref` i prikazati ga u templateu. |

## Praktične izmjene projekta

| # | Pitanje | Očekivani odgovor |
|---|---|---|
| 43 | Ako student želi dodati `lunch` kao ulaznu značajku, što sve mora promijeniti? | Mora promijeniti trening kod, spremiti novi encoder/scaler/model, proširiti backend payload i dodati polje na frontend formu. |
| 44 | Ako student želi promijeniti target s `writing score` na `math score`, što sve mora promijeniti? | Mora promijeniti ciljnu varijablu u treniranju, spremiti novi model i scaler za target te prilagoditi backend i tekstove na frontendu. |
| 45 | Kako bi student dodao novi klasifikacijski endpoint? | Treba definirati klasifikacijski target, istrenirati klasifikacijski model, spremiti artefakte, dodati backend rutu i povezati frontend formu. |
| 46 | Kada bi `OneHotEncoder` bio bolji izbor od `LabelEncoder`? | Bio bi bolji kada kategorije nemaju prirodan redoslijed jer ne nameće lažni poredak kategorija. |
| 47 | Kada bi `RobustScaler` mogao biti bolji od `StandardScaler`? | Mogao bi biti bolji ako numeričke značajke imaju puno outliera. |
| 48 | Kako bi student testirao backend bez frontenda? | Može koristiti Postman, curl ili sličan alat i poslati JSON na `POST /api/predict`. |
| 49 | Koji je minimalni dokaz da student razumije cijeli flow predikcije? | Treba objasniti put od forme, preko JSON zahtjeva i backend preprocessinga, do modela i prikaza rezultata. |
| 50 | Koja je najvažnija razlika između projekta koji samo radi i projekta koji je metodološki ispravan? | Metodološki ispravan projekt ima korektan split, preprocessing bez curenja podataka, spremljene artefakte i poštenu evaluaciju. |

## Organizacija i predaja projekta

| # | Pitanje | Očekivani odgovor |
|---|---|---|
| 51 | Kako trebaju biti organizirani GitHub repozitoriji? | Frontend i backend trebaju biti u dva odvojena GitHub repozitorija. |
| 52 | U koji repozitorij ide Jupyter notebook? | Notebook s eksperimentima ide u backend repozitorij. |
| 53 | Što student mora poslati prije ispitnog roka? | Mora poslati link na backend repozitorij i link na frontend repozitorij na `hrvoje.ljubic@fpmoz.sum.ba`. |

## Minimalno znanje za prolaz

Student za prolaz mora znati:

- pokrenuti backend i frontend
- objasniti dataset, ulazne značajke i ciljnu varijablu
- objasniti train/validation/test podjelu
- objasniti zašto se spremaju model, encoderi i scaleri
- pokazati gdje backend radi predikciju
- pokazati gdje frontend šalje API zahtjev
- prepoznati najčešće greške u preprocessingu i evaluaciji
