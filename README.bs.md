<a href="https://github.com/SafetImamovic/Student-Management-System/blob/main/README.md"><img src="https://img.shields.io/badge/Lang-EN-red" alt=""></a> <a href="https://github.com/SafetImamovic/Student-Management-System/blob/main/README.bs.md"><img src="https://img.shields.io/badge/Lang-BS-blue" alt="Project Documentation"></a> <a href="https://safetimamovic.github.io/Student-Management-System/starter-topic.html"><img src="https://img.shields.io/badge/Projektna%20Dokumentacija-gray" alt="Projektna Dokumentacija"></a>

# Sistem za Upravljanje Studentima

## Brza Postavka

Ovaj projekat koristi Docker za pokretanje FastAPI i PostgreSQL-a u zasebnim kontejnerima.

Da biste pokrenuli FastAPI i PostgreSQL kontejnere, pokrenite sljedeću komandu u korijenu projekta:

```Bash
./start
```

Ovaj skript će kreirati zajedničku mrežu, izgraditi sliku za FastAPI, pokrenuti FastAPI i PostgreSQL kontejnere, i prikazati logove kontejnera.

Nakon uspješne izgradnje, pokretanje `docker ps` bi trebalo prikazati aktivne kontejnere.

Da biste zaustavili kontejnere, pokrenite:

```Bash
docker-compose down
```

> Također možete pokrenuti:
> ```Bash
> ./start --help
> ```

Nakon toga, posjećivanje `http://localhost:8000/` ili `http://127.0.0.1:8000/` u pretraživaču će rezultirati HTML tijelom:

```Bash
{"Hello": "World"}
```

[_Više detalja o postavljanju Dockera, Dockerfile-a i Docker Compose-a možete pronaći ovdje_](https://safetimamovic.github.io/Student-Management-System/docker.html)

> Volumes još nisu integrisani, tako da live ažuriranja ne rade

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