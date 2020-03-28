# Dokumentacija

## Projektne vloge

### GET /api/project_role

Vrne vse projektne vloge.

```json
[
    {
        "id": 12,
        "title": "Project manager"
    },
    {
        "id": 13,
        "title": "Product manager"
    },
    {
        "id": 14,
        "title": "Developer"
    },
    {
        "id": 15,
        "title": "Methodology master"
    }
]
```

## Projekti

### POST /api/project

Ustvari nov projekt z določenim imenom in uporabniki.

Telo zahtevka:

```json
{
	"name": "Test project #3",
	"user_roles": [
		{
			"user_id": 1,
			"role_id": 55
		},
		{
			"user_id": 2,
			"role_id": 22
		}
	]
}
```

Napaka se vrne v naslednjih primerih:

1. Niso izpolnjena vsa polja (ime ali projektni člani).
2. Projekt s tem imenom že obstaja.
3. V seznamu uporabnikov in vlog se nek zapis podvoji.
4. V seznamu uporabnikov in vlog je podan uporabnik ali vloga, ki ne obstaja.
5. Uporabnik nima zadostnih privilegijev (mora biti administrator).

### GET /api/project

Vrne vse projekte v podatkovni bazi.

```json
[
    {
        "id": 1,
        "name": "Project 1.",
        "documentation": null,
        "users": [
            {
                "id": 1,
                "role": "Developer",
                "name": "Janez Novak",
                "username": "janeznovak",
                "email": "janez.novak@gmail.com"
            },
            {
                "id": 2,
                "role": "Developer",
                "name": "Tinkara Kovač",
                "username": "tinkarakovac",
                "email": "tinkara.kovac@gmail.com"
            },
            {
                "id": 3,
                "role": "Project manager",
                "name": "",
                "username": "admin",
                "email": "admin@gmail.com"
            }
        ],
        "created": "2020-03-22T20:47:07.036Z",
        "updated": "2020-03-23T20:04:27.204Z"
    },
    {
        "id": 3,
        "name": "Project 2",
        "documentation": null,
        "users": [
            {
                "id": 4,
                "role": "Project manager",
                "name": "",
                "username": "admin",
                "email": "admin@gmail.com"
            }
        ],
        "created": "2020-03-22T20:47:07.044Z",
        "updated": "2020-03-23T20:04:36.863Z"
    },
]
```

V primeru, da ne obstaja noben projekt, se vrne prazen seznam.

### GET /api/project/{id}

Vrne projekt z ID-jem {id}.

```json
{
    "id": 1,
    "name": "Project 1.",
    "documentation": null,
    "users": [
        {
            "id": 1,
            "role": "Developer",
            "name": "Janez Novak",
            "username": "janeznovak",
            "email": "janez.novak@gmail.com"
        },
        {
            "id": 2,
            "role": "Developer",
            "name": "Tinkara Kovač",
            "username": "tinkarakovac",
            "email": "tinkara.kovac@gmail.com"
        },
        {
            "id": 3,
            "role": "Project manager",
            "name": "",
            "username": "admin",
            "email": "admin@gmail.com"
        }
    ],
    "created": "2020-03-22T20:47:07.036Z",
    "updated": "2020-03-23T20:04:27.204Z"
}
```

V primeru, da projekt s tem ID-jem ne obstaja, se vrne napaka.

## Sprinti

### POST /api/project/{project_id}/sprint

V projekt z id-jem {project_id} se doda nov sprint.

Telo zahtevka:

```json
{
    "start_date": "2020-03-28",
    "end_date": "2020-03-29",
    "expected_speed": 1.9
}
```

Napaka se vrne v naslednjih primerih:

1. Začetni datum je v preteklosti.
2. Končni datum je pred začetnim.
3. Hitrost sprinta je manjša ali enaka 0.
4. Dodani sprint se prekriva z že obstoječimi sprinti.
5. Uporabnik nima zadostnih privilegijev (mora biti skrbnik metodologije).

### GET /api/project/{project_id}/sprint/{sprint_id}

Pridobi sprint z ID-jem {sprint_id}, ki priprada projektu z ID-jem {project_id}.

```json
{
    "id": 16,
    "start_date": "2020-03-25",
    "end_date": "2020-03-29",
    "expected_speed": 1.9,
    "project_id": 3,
    "created": "2020-03-25T18:45:14.733Z",
    "updated": "2020-03-25T19:47:26.028Z"
}
```

### GET /api/project/{project_id}/sprint

Pridobi vse sprinte, ki pripradajo projektu z ID-jem {project_id}.

```json
[
    {
        "id": 16,
        "start_date": "2020-03-25",
        "end_date": "2020-03-29",
        "expected_speed": 1.9,
        "project_id": 3,
        "created": "2020-03-25T18:45:14.733Z",
        "updated": "2020-03-25T19:47:26.028Z"
    },
    {
        "id": 20,
        "start_date": "2021-03-25",
        "end_date": "2021-03-27",
        "expected_speed": 1.9,
        "project_id": 3,
        "created": "2020-03-25T20:03:28.463Z",
        "updated": "2020-03-25T20:03:28.463Z"
    }
]
```