import scrapy


class PokemonScrapper(scrapy.Spider):
  name = 'pokemon_scrapper'
  domain = "https://pokemondb.net/"
  start_urls = ["https://pokemondb.net/pokedex/all"]

  def parse(self, response):
    pokemons = response.css('#pokedex > tbody > tr')
    for pokemon in pokemons:
    #pokemon = pokemons[123]
      link = pokemon.css("td.cell-name > a::attr(href)").extract_first()
      yield response.follow(self.domain + link, self.parse_pokemon)

  def parse_pokemon(self, response):

    pokemon_id = response.css(
        '.vitals-table > tbody > tr:nth-child(1) > td > strong::text').get()
    pokemon_name = response.css('#main > h1::text').get()
    pokemon_weigth = response.css(
        '.vitals-table > tbody > tr:nth-child(5) > td::text').get()
    pokemon_heigth = response.css(
        '.vitals-table > tbody > tr:nth-child(4) > td::text').get()
    pokemon_type1 = response.css(
        '.vitals-table > tbody > tr:nth-child(2) > td > a::text').get()
    pokemon_type2 = response.css(
        '.vitals-table > tbody > tr:nth-child(2) > td > a:nth-child(2)::text'
    ).get()
    pokemon_ability1 = response.css(
        '.vitals-table > tbody > tr:nth-child(6) > td > span > a::text'
    ).get()
    pokemon_ability1_link = self.domain + response.css(
        '.vitals-table > tbody > tr:nth-child(6) > td > span > a::attr(href)'
    ).get()
    pokemon_ability2 = response.css(
        '.vitals-table > tbody > tr:nth-child(6) > td > span > a::text'
    ).get()
    pokemon_ability2_link = self.domain + response.css(
        '.vitals-table > tbody > tr:nth-child(6) > td > span:nth-child(3) > a::attr(href)'
    ).get()
    pokemon_hiddenability = response.css(
        '.vitals-table > tbody > tr:nth-child(6) > td > small > a::text'
    ).get()
    pokemon_hiddenability_link = self.domain + response.css(
        '.vitals-table > tbody > tr:nth-child(6) > td > small > a::attr(href)'
    ).get()

    evolutions = []
    evolution_cards = response.css(
        '#main > div.infocard-list-evo > div.infocard')

    for evo in evolution_cards:
      evolution_number = evo.css('.infocard-lg-data small::text').get()
      evolution_name = evo.css('.infocard-lg-data a.ent-name::text').get()
      evolution_link = evo.css(
          '.infocard-lg-data a.ent-name::attr(href)').get()

      evolutions.append({
          'evolution_number':
          evolution_number,
          'evolution_name':
          evolution_name,
          'evolution_link':
          self.domain + evolution_link if evolution_link else None
      })

    yield {
        'pokemon_id': pokemon_id,
        'pokemon_name': pokemon_name,
        'pokemon_weigth': pokemon_weigth,
        'pokemon_heigth': pokemon_heigth,
        'pokemon_type1': pokemon_type1,
        'pokemon_type2': pokemon_type2,
        'pokemon_ability1_name': pokemon_ability1,
        'pokemon_ability1_link': pokemon_ability1_link,
        'pokemon_ability1_name': pokemon_ability2,
        'pokemon_ability2_link': pokemon_ability2_link,
        'pokemon_hiddenability_name': pokemon_hiddenability,
        'pokemon_hiddenability_link': pokemon_hiddenability_link,
        'evolutions': evolutions
    }