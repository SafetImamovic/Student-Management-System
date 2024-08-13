<a href="https://github.com/SafetImamovic/Student-Management-System/blob/main/README.md"><img src="https://img.shields.io/badge/Lang-EN-red" alt=""></a> <a href="https://github.com/SafetImamovic/Student-Management-System/blob/main/README.bs.md"><img src="https://img.shields.io/badge/Lang-BS-blue" alt="Project Documentation"></a> <a href="https://safetimamovic.github.io/Student-Management-System/starter-topic.html"><img src="https://img.shields.io/badge/Projektna%20Dokumentacija-gray" alt="Projektna Dokumentacija"></a>

# Sistem za Upravljanje Studentima

Naravno, evo prijevoda na bosanski:

## Brza Instalacija

Ovaj projekt koristi Docker za pokretanje FastAPI i PostgreSQL u odvojenim kontejnerima.

### FastAPI & PostgreSQL

Da biste pokrenuli FastAPI i PostgreSQL kontejnere, pokrenite sljedeću komandu u korijenskom direktoriju projekta:

```Bash
./scripts/start
```

Ovaj skript će kreirati zajedničku mrežu, izgraditi FastAPI sliku, pokrenuti FastAPI i PostgreSQL kontejnere i ispisati logove kontejnera.

Nakon uspješnih izgradnji, komanda `docker ps` bi trebala prikazati aktivne kontejnere.

Zatim, posjetite `http://localhost:8000/` ili `http://127.0.0.1:8000/` u pregledniku da biste vidjeli HTML sadržaj:

```Bash
{"Hello": "World"}
```

### PostgreSQL Klijent

Da biste pokrenuli PSQL klijent kao kontejner, pokrenite:

```Bash
./scripts/start-psql-client
```

Ovaj skript pokreće novi kontejner na osnovu postgres docker slike. Ovaj kontejner nije specificiran u docker compose datoteci, već se treba pokrenuti ako ne želite preuzeti i instalirati postgres drajver lokalno.

Pokreće klijent i povezuje se na mrežu na kojoj je već baza podataka. Ako kontejner baze podataka nije aktivan, klijent će prikazati greške.

### Zaustavljanje & Ciscenje

Da biste zaustavili kontejnere, pokrenite:

```Bash
docker-compose down
```

ili pokrenite:

```Bash
./scripts/clean-up
```

### Dodatne Opcije

Za dodatne opcije u vezi sa upravljanjem klijent kontejnerom i mrežom.

> Također možete pokrenuti:
> ```Bash
> ./scripts/{naziv skripta} --help
> ```
> Da vidite kako rade.

[_Više detalja o postavljanju Dockera, Dockerfile-a i Docker Compose-a možete pronaći ovdje_](https://safetimamovic.github.io/Student-Management-System/docker.html)

## Cilj

Ovaj projekt je osmišljen da pruži praktično iskustvo u izgradnji i upravljanju API-jima koristeći:
- **FastAPI**
- **PostgreSQL**
- **Alembic**
- **Pydantic**

Glavni fokus će biti na razvoju jednostavnog sistema za upravljanje studentima: kreiranje modela, rukovanje CRUD operacijama, validacija podataka i integracija relacione baze podataka sa web API-jem.

## Vremenski Okvir Projekta

Ovaj projekt traje 4 sedmice:

### Sedmica 1: Uvod i postavka

Postavljanje razvojnog okruženja i uvod u FastAPI, PostgreSQL, Alembic i Pydantic. Pregled osnovnih Python koncepta.

### Sedmica 2: Integracija baze podataka i modeli

Učenje o SQLAlchemy za ORM, kreiranje PostgreSQL baza podataka i tabela, postavljanje modela baza podataka u FastAPI i korištenje Pydantic-a za validaciju podataka.

### Sedmica 3: CRUD operacije

Implementacija CRUD operacija i razvoj API endpointa za ove operacije. Validacija podataka koristeći Pydantic modele.

### Sedmica 4: Migracije baze podataka i finalni projekt

Uvod u Alembic za migracije baza podataka, izvođenje migracija baza podataka i finalizacija projekta za prezentaciju.

> _Tabela projekta je podložna promjenama_