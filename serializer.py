import yaml
from tabulate import tabulate
import pandas as pd


class Serializer:
    def __init__(self, document_path: str):
        self.path = document_path
        self.planet_dict = {}
        self.min_distances = {}
        self.max_distances = {}

    def extract_solar_system(self):
        with open(self.path, 'r') as yaml_file:
            self.planet_dict = yaml.safe_load(yaml_file)
        self.convert_dict()

    def convert_dict(self):
        new_dict = {}
        for i in self.planet_dict['sun_system']['distance_to_sun']:
            planet_name = list(i.keys())[0]
            distance = i[planet_name]
            new_dict[planet_name] = distance
        self.planet_dict = new_dict

    def calc_min_distances(self):
        keys = self.planet_dict.keys()
        for i in self.planet_dict:
            self.min_distances[i] = {}
            for key in keys:
                self.min_distances[i][key] = round(abs(self.planet_dict[key] - self.planet_dict[i]), 2)

    def calc_max_distances(self):
        keys = self.planet_dict.keys()
        for i in self.planet_dict:
            self.max_distances[i] = {}
            for key in keys:
                if i == key:
                    self.max_distances[i][key] = 0
                else:
                    self.max_distances[i][key] = round(abs(self.planet_dict[key] + self.planet_dict[i]), 2)

    def generate_xlsx(self, name, data):
        df = pd.DataFrame(data)
        df.to_excel(name)

    def run(self):
        print("Processing data!")
        self.extract_solar_system()
        self.calc_min_distances()
        self.calc_max_distances()

        print("Generating tables!")
        self.generate_xlsx("max_distances.xlsx", self.max_distances)
        self.generate_xlsx("min_distances.xlsx", self.min_distances)

        print("Finished!")


if __name__ == "__main__":
    serializer = Serializer("./solar_system.yaml")
    serializer.run()

