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