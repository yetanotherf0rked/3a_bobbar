import pygame

import ressources.config
class Weather:

    def __init__(self):
        self.config = ressources.config.para


    def update(self, weather):
        if weather == "Sandstorm":
            self.config.WEATHER_ENERGY_COEFF = self.ENERGY_MAX * 1/(16 * self.config.TICK_DAY)
            self.config.WEATHER_PERCEPTION_COEFF = 1
            self.config.WEATHER_VELOCITY_COEFF = 1
            self.config.weather = weather
        if weather == "Hail":
            self.config.WEATHER_ENERGY_COEFF = self.ENERGY_MAX * 1/(16 * self.config.TICK_DAY)
            self.config.WEATHER_PERCEPTION_COEFF = 1
            self.config.WEATHER_VELOCITY_COEFF = 1
            self.config.weather = weather
        if weather == "Fogue":
            self.config.WEATHER_ENERGY_COEFF = 1
            self.config.WEATHER_PERCEPTION_COEFF = 1/2
            self.config.WEATHER_VELOCITY_COEFF = 1
            self.config.weather = weather
        if weather == "Rain":
            self.config.WEATHER_ENERGY_COEFF = 1
            self.config.WEATHER_PERCEPTION_COEFF = 1
            self.config.WEATHER_VELOCITY_COEFF = 2
            self.config.weather = weather
        if weather == "Sun":
            self.config.WEATHER_ENERGY_COEFF = 1
            self.config.WEATHER_PERCEPTION_COEFF = 1
            self.config.WEATHER_VELOCITY_COEFF = 1
            self.config.weather = weather