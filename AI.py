import Model
from random import randint
# from heroes import blaster, sentry, healer, guardian
import heroes.sentry
from heroes.sentry import *
from heroes.blaster import *
from heroes.guardian import * 
from heroes.healer import * 
from heroes.fixed import * 

class AI:
    def preprocess(self, world):
        print("preprocess")
        self.fixed = fixed(randint, world, Model)
        self.sentry = sentry(Model, self.fixed, world)
        self.blaster = blaster(Model, self.fixed, world)
        self.healer = healer(Model, self.fixed, world)
        self.guardian = guardian(Model, self.fixed, world)
        self.which_pick = 0


    def pick(self, world):
        print("pick")

        if self.which_pick == 0:
            # world.pick_hero(Model.HeroName.GUARDIAN)
            world.pick_hero(Model.HeroName.SENTRY)
        # elif self.which_pick == 1:
            # world.pick_hero(Model.HeroName.GUARDIAN)
            # world.pick_hero(Model.HeroName.HEALER)
        else:
            world.pick_hero(Model.HeroName.BLASTER)

        self.which_pick += 1

    def move(self, world):
        # print ("AP : ",world.ap)
        # self.visible_enemy
        for hero in world.my_heroes:
            if hero.respawn_time != 0:
                continue
            self.fixed.heros_cell[hero.id] = hero.current_cell

        # i = 0
        for hero in world.my_heroes:
            if hero.respawn_time != 0:
                continue
            # print(hero.name)
            if hero.name == Model.HeroName.SENTRY:
                self.sentry.move(hero)
            elif hero.name == Model.HeroName.BLASTER:
                self.blaster.move(hero)
            elif hero.name == Model.HeroName.GUARDIAN:
                self.guardian.move(hero)
            elif hero.name == Model.HeroName.HEALER:
                self.healer.move(hero)

    def action(self, world):
        print(world.current_turn)
        print("action")
        for hero in world.my_heroes:
            if hero.respawn_time != 0:
                continue
            # print(hero.name)
            if hero.name == Model.HeroName.SENTRY:
                self.sentry.action(hero)
            elif hero.name == Model.HeroName.BLASTER:
                self.blaster.action(hero)
            elif hero.name == Model.HeroName.GUARDIAN:
                self.guardian.action(hero)
            elif hero.name == Model.HeroName.HEALER:
                self.healer.action(hero)


        print("my_score: ", world.my_score)



