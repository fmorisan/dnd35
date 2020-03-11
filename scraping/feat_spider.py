import scrapy
import re
import json

header_data_re = re.compile(r".+>(.+)<.+:\s+(.+)$")
content_data_re = re.compile(r".+>(.+):<.+>\s+(.+)$")

MODE_CHOICES = {
    "Normal": 'normal',
    "Repeatable": 'repeatable',
    "Stackable": 'stackable',
    None: None
}

CATEGORY_CHOICES = {
    "General": 'general',
    "Metam\u00e1gica": 'metamagic',
    "Especial": 'special',
    "Creaci\u00f3n de objetos": 'object-creation',
    None: None
}


class FeatListSpider(scrapy.spiders.Spider):
    name = "feats-spider"
    base_url = "https://dungeon20.com"

    def start_requests(self):
        urls = [
            f"{self.base_url}/games/dnd-3-5/feats?page={page}"
            for page in [1, 2, 3, 4, 5]
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def request_feats(self, urls):
        for relative_url in urls:
            yield scrapy.Request(
                url=f'{self.base_url}{relative_url}',
                callback=self.parse_feat
            )

    def parse(self, response):
        urls_to_follow = response.css('a.row-link').xpath('@href').getall()
        for req in self.request_feats(urls_to_follow):
            self.logger.info(
                f"Requesting {req.url}"
            )
            yield req

    def interpret_feat(self, feat) -> dict:
        prerequisites = feat['header_data'].get('Prerequisitos', '')
        if not prerequisites:
            prerequisites = feat['header_data'].get('Prerrequisitos', '')
        prerequisites_parsed = []
        if prerequisites:
            prerequisites_parsed = [
                pre.strip() for pre in prerequisites.split(',')
            ]

        category = CATEGORY_CHOICES[
            feat['header_data'].get('Categor\u00eda')
        ]
        mode = MODE_CHOICES[feat['header_data'].get('Modo')]
        father = feat['header_data'].get('Padre', '')
        benefit = feat['description_data'].get('Beneficio', '')

        return {
            "category": category,
            "mode": mode,
            "father": father,
            "benefit": benefit,
            "prerequisites": prerequisites_parsed,
            "id": feat['id'],
            "name": feat['name'],
        }

    def parse_feat(self, response):
        header = response.css(
            '.card-block p:nth_child(1)'
        ).get().split('<br>')[1:-1]
        content = response.css('.card-block p').getall()[1:]
        # All card_data wrapped in <p>content</p>
        # inspect_response(response, self)
        header_data = dict()
        for point in header:
            match = header_data_re.match(point)
            if match:
                header_data[match.group(1)] = match.group(2)

        extra_data = list()
        description_data = dict()
        for data in content:
            data = data[3:-4]
            match = content_data_re.match(data)
            if match:
                description_data[match.group(1)] = match.group(2)
            if not match:
                if "<strong>" in data:
                    match = content_data_re.match(data.replace("\n", " "))
                    if match:
                        description_data[match.group(1)] = match.group(2)
                    else:
                        self.logger.error("No match for %s", data)
                else:
                    extra_data.append(data)

        filename = response.url.split('/')[-1]
        feat_data = {
            "id": int(filename.split('-')[0]),
            "name": response.css('.card-title span::text').get(),
            "header_data": header_data,
            "description_data": description_data,
            "extra_data": extra_data[:-2]
        }

        with open(f"../feats/{filename}.json", 'w') as f:
            f.write(
                json.dumps(
                    self.interpret_feat(feat_data),
                    indent=2,
                    sort_keys=True
                )
            )
