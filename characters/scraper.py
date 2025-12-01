import requests
from django.conf import settings
from django.db import IntegrityError, transaction

from characters.models import Character

GRAPHQL_QUERY = """
query {
  characters(page: %s) {
    info{
      pages
    }
    results{
      api_id: id
      name
      status
      gender
      image
    }
  }
}
"""


def scrape_characters() -> list[Character]:
    url_to_scrape = settings.RICK_AND_MORTY_API_CHARACTERS_URL

    characters = []

    while url_to_scrape is not None:
        characters_response = requests.get(
            url_to_scrape, data={"query": GRAPHQL_QUERY % "1"}
        ).json()

        for character_dict in characters_response["results"]:
            characters.append(
                Character(
                    api_id=character_dict["id"],
                    name=character_dict["name"],
                    status=character_dict["status"],
                    species=character_dict["species"],
                    gender=character_dict["gender"],
                    image=character_dict["image"],
                )
            )

        url_to_scrape = characters_response["info"]["next"]

    return characters


@transaction.atomic
def save_characters(characters: list[Character]):
    to_create = []
    to_update = []

    for character in characters:
        existing = Character.objects.filter(id=character.api_id).first()
        if not existing:
            to_create.append(character)
        else:
            to_update.append(character)
            print(f"The character with ad {character.api_id} already is in DB")

    Character.objects.bulk_create(to_create, ignore_conflicts=True)

    for character_update_data in to_update:
        Character.objects.filter(api_id=character_update_data.api_id).update(
            name=character_update_data.name,
            status=character_update_data.status,
            species=character_update_data.species,
            gender=character_update_data.gender,
            image=character_update_data.image,
        )


def sync_characters_with_api() -> None:
    characters = scrape_characters()
    save_characters(characters)
