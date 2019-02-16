import Model
from random import randint


class AI:
    def preprocess(self, world):
        print("preprocess")
        self.set_zone(world)

    def pick(self, world):
        print("pick")
        if self.which_pick == 0:
            world.pick_hero(Model.HeroName.BLASTER)
        else:
            world.pick_hero(Model.HeroName.SENTRY)

        self.which_pick += 1

    def move(self, world):
        # print ("AP : ",world.ap)
        # self.visible_enemy

        i = 0
        for hero in world.my_heroes:
            if hero.current_cell.is_in_objective_zone is False:
                # print("move to zone")
                for j in range(6):
                    final_cell = self.zone_cell[i + j]
                    ways = world.get_path_move_directions(
                        start_cell=hero.current_cell, end_cell=final_cell
                    )
                    for way in ways:
                        world.move_hero(hero=hero, direction=way)
                i += 1
                continue
            elif hero.current_cell.is_in_objective_zone is True:
                for opp_hero in world.opp_heroes:
                    if opp_hero.current_cell.is_in_objective_zone is True:
                        # print(hero.name)
                        if hero.name == "BLASTER":
                            # print("blaster go to enemy")
                            final_row = opp_hero.current_cell.row
                            final_column = opp_hero.current_cell.column - randint(1, 4)
                            ways = world.get_path_move_directions(
                                start_cell=hero.current_cell,
                                end_row=final_row,
                                end_column=final_column,
                            )

                            for way in ways:
                                world.move_hero(hero=hero, direction=way)

                    else:
                        if hero.name == "BLASTER":
                            # print("blaster go random move")
                            final_cell = self.zone_cell[
                                int(len(world.map.objective_zone) / 2) - randint(0, 4)
                            ]
                            ways = world.get_path_move_directions(
                                start_cell=hero.current_cell, end_cell=final_cell
                            )
                            for way in ways:
                                world.move_hero(hero=hero, direction=way)

                # if hero.name == Model.HeroName.SENTRY :
                #     self.sentry_move(world, hero)
                # if hero.name == Model.HeroName.BLASTER :
                #     self.blaster_move(world, hero)

    def action(self, world):
        print(world.current_turn)
        print("action")
        for hero in world.my_heroes:

            if hero.name == "SENTRY":
                self.sentry_action(world, hero)
            # elif hero.name == "BLASTER" :
            #     self.blaster_action(world, hero)
        print("kill_Score : ",world.kill_score)
        print("zone_Score : ",world.objective_zone_score)
        # row_num = randint(0, world.map.row_num)
        # col_num = randint(0, world.map.column_num)
        # abilities = hero.abilities
        # world.cast_ability(
        #     hero=hero,
        #     ability=abilities[randint(0, len(abilities) - 1)],
        #     cell=world.map.get_cell(row_num, col_num),
        # )

    # def sentry_move(self, world, hero):

    # def blaster_move(self, world, hero):

    def sentry_action(self, world, hero):
        for opp_hero in world.opp_heroes:
            if opp_hero.current_cell.row != -1 or opp_hero.current_cell.column != -1 :
                if hero.get_ability("SENTRY_RAY").is_ready() is True:
                    targets = world.get_ability_targets(
                        ability_name="SENTRY_RAY",
                        start_cell=hero.current_cell,
                        target_cell=opp_hero.current_cell
                    )
                    for target in targets:
                        if target.current_cell.row != -1 or target.current_cell.column != -1 :
                            world.cast_ability(
                                hero=hero,
                                ability_name=Model.AbilityName.SENTRY_RAY,
                                cell=target.current_cell,
                            )
                            print("sentry doed")
            # if opp_hero == world.get_ability_targets(ability_name=Model.AbilityName.SENTRY_RAY, start_cell=hero.current_cell, target_cell=opp_hero.current_cell):

    # def blaster_action(self, world, hero):
    # for opp_hero in world.opp_heroes:
    # print(world.get_ability_targets(ability_name=Model.AbilityName.BLASTER_BOMB, start_cell=hero.current_cell, target_cell=opp_hero.current_cell))
    # if opp_hero == world.get_ability_targets(ability_name=Model.AbilityName.BLASTER_BOMB, start_cell=hero.current_cell, target_cell=opp_hero.current_cell):
    #     world.cast_ability(hero=hero, ability_name=Model.AbilityName.BLASTER_BOMB, cell=opp_hero.current_cell)
    # else :
    #     world.cast_ability(hero=hero, ability_name=Model.AbilityName.BLASTER_ATTACK, cell=opp_hero.current_cell)

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
