import scrapy
import json


class FeatListSpider(scrapy.spiders.Spider):
    name = "skills-spider"
    base_url = "https://dungeon20.com"

    def start_requests(self):
        url = f"{self.base_url}/games/dnd-3-5/skills"
        yield scrapy.Request(url=url, callback=self.parse)

    def request_skills(self, urls):
        for relative_url in urls:
            yield scrapy.Request(
                url=f'{self.base_url}{relative_url}',
                callback=self.parse_skill
            )

    def parse(self, response):
        urls_to_follow = response.css('.skill a').xpath('@href').getall()
        for req in self.request_skills(urls_to_follow):
            yield req

    def parse_skill(self, response):
        description_list = response.css('dl')
        terms = description_list.css('dt::text').getall()
        descriptions = description_list.css('dd::text').getall()

        data = dict()
        for i, term in enumerate(terms):
            try:
                data[term[:-1]] = descriptions[i]
            except Exception:
                data[term[:-1]] = ''

        cleaned_data = {
            'ability': data['Ability'],
            'description': data['Description'],
            'requires_training': data['Requires training'] == "true",
            'armor-penalty': data["Armor penalty multiplier"].lower() or None,
            'name': data["Name"],
        }

        filename = response.url.split('/')[-1]

        cleaned_data['id'] = int(filename.split('-')[0])

        with open(f"../skills/{filename}.json", 'w') as f:
            f.write(
                json.dumps(cleaned_data, indent=2, sort_keys=True)
            )
