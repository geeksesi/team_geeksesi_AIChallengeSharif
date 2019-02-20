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

        # if self.which_pick == 0:
            # world.pick_hero(Model.HeroName.GUARDIAN)
            # world.pick_hero(Model.HeroName.SENTRY)
        # elif self.which_pick == 1:
            # world.pick_hero(Model.HeroName.GUARDIAN)
            # world.pick_hero(Model.HeroName.HEALER)
        # else:
        world.pick_hero(Model.HeroName.BLASTER)

        self.which_pick += 1

    def move(self, world):
        if world.current_turn == 4:
            self.fixed.set_enemy_ability(world)
        for hero in world.my_heroes:
            if hero.respawn_time != 0:
                continue
            self.fixed.heros_cell[hero.id] = hero.current_cell

        for hero in world.my_heroes:
            if hero.respawn_time != 0:
                continue
            if hero.name == Model.HeroName.SENTRY:
                self.sentry.move(world, hero)
            elif hero.name == Model.HeroName.BLASTER:
                self.blaster.move(world, hero)
            elif hero.name == Model.HeroName.GUARDIAN:
                self.guardian.move(world, hero)
            elif hero.name == Model.HeroName.HEALER:
                self.healer.move(world, hero)

    def action(self, world):
        self.fixed.turn_enemy_ability(world)
        self.fixed.enemy_cooldown(world)

        print("this turn ~> ",world.current_turn)
        for hero in world.my_heroes:
            if hero.respawn_time != 0:
                continue
            if hero.name == Model.HeroName.SENTRY:
                self.sentry.action(world, hero)
            elif hero.name == Model.HeroName.BLASTER:
                self.blaster.action(world, hero)
            elif hero.name == Model.HeroName.GUARDIAN:
                self.guardian.action(world, hero)
            elif hero.name == Model.HeroName.HEALER:
                self.healer.action(world, hero)


        print("My Score ~>", world.my_score)
        # print("Enemy Score ~>", world.opp_score)



