import Model
from random import randint


class AI:

    def preprocess(self, world):
        print("preprocess")
        self.set_zone(world)


    def pick(self, world):
        print("pick")
        if self.which_pick == 0:
            world.pick_hero(Model.HeroName.SENTRY)
        else:
            world.pick_hero(Model.HeroName.BLASTER)

        self.which_pick += 1


    def move(self, world):
        print("move")
        # print ("AP : ",world.ap)
        i = 0
        for hero in world.my_heroes:
            if hero.current_cell.is_in_objective_zone is False:
                final_cell = self.zone_cell[i]
                final_cell = self.zone_cell[i+1]
                final_cell = self.zone_cell[i+2]
                final_cell = self.zone_cell[i+3]
                final_cell = self.zone_cell[i+4]
                final_cell = self.zone_cell[i+5]
                final_cell = self.zone_cell[i+6]
                ways = world.get_path_move_directions(
                    start_cell=hero.current_cell, end_cell=final_cell
                )
                i += 1
                for way in ways :
                    world.move_hero(hero=hero, direction=way)
                continue
            # if hero.current_cell.is_in_objective_zone() is True:

    def action(self, world):
        print(world.current_turn)
        print("action")
        for hero in world.my_heroes:

            if hero.name == Model.HeroName.SENTRY :
                self.sentry_action
            elif hero.name == Model.HeroName.BLASTER :
                self.sentry_action

            row_num = randint(0, world.map.row_num)
            col_num = randint(0, world.map.column_num)
            abilities = hero.abilities
            world.cast_ability(
                hero=hero,
                ability=abilities[randint(0, len(abilities) - 1)],
                cell=world.map.get_cell(row_num, col_num),
            )

    def set_zone(self, world):
        self.which_pick = 0
        zone_dir = [zone for zone in world.map.objective_zone]
        alive_dir = [alive for alive in world.map.my_respawn_zone]
        first_zone = world.manhattan_distance(alive_dir[0], zone_dir[0])
        second_zone = world.manhattan_distance(
            alive_dir[0], zone_dir[len(zone_dir) - 1]
        )
        if second_zone < first_zone:
            zone = zone_dir
            zone_dir = []
            for wtf_zone in reversed(zone):
                zone_dir.append(wtf_zone)

        self.zone_cell = zone_dir