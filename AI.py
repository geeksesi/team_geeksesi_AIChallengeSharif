
import Model
from random import randint


class AI:

    def preprocess(self, world):
        print("preprocess")

    def pick(self, world):
        print("pick")
        # hero_names = [hero_name for hero_name in Model.HeroName]
        # world.pick_hero(hero_names[randint(0, len(hero_names) - 1)])
        # print(hero_names[randint(0, len(hero_names) - 1)])
        i = 0
        if i == 0:
            world.pick_hero(Model.HeroName.SENTRY) 
        else :
            world.pick_hero(Model.HeroName.BLASTER) 
            
        i +=1
        

    def move(self, world):
        print("move")

        zone_dir = [zone for zone in world.map.objective_zone]
        # for zones in zone_dir:
        # print(world.map.objective_zone)
        print ("befor : ",world.ap)
        i = 0
        for hero in world.my_heroes:
            this_cell = hero.current_cell
            final_cell = zone_dir[i]
            ways = []
            ways = world.get_path_move_directions(start_cell = this_cell, end_cell = final_cell)
            i += 1
            b = 0
            for way in ways:
                world.move_hero(hero=hero, direction=way)

                b += 1
        print ("after move : ",world.ap)

    def action(self, world):
        print("action")
        for hero in world.my_heroes:
            row_num = randint(0, world.map.row_num)
            col_num = randint(0, world.map.column_num)
            abilities = hero.abilities
            world.cast_ability(hero=hero, ability=abilities[randint(0, len(abilities) - 1)],
                               cell=world.map.get_cell(row_num, col_num))