
class blaster:

    def __init__(self, Model, fixed, world):
        self.Model = Model
        self.fixed = fixed
        world = world
        self.blaster_num = 0

        self.respawn_goal = [
            self.fixed.zone_cell[(int(len(self.fixed.zone_cell) / 2) + 2)],
            self.fixed.zone_cell[(int(len(self.fixed.zone_cell) / 2) - 2)],
            self.fixed.zone_cell[2],
            self.fixed.zone_cell[self.fixed.zone_size["row"]]
        ]


    def move(self, world, hero):
        self.blaster_num = 0 if self.blaster_num == 3 else (self.blaster_num + 1) 
        opp_hero = self.fixed.find_fucking_enemy(world, hero)
        if opp_hero is None:
            self.fixed.move_my_hero(world, hero, self.fixed.zone_cell[5 + int(self.blaster_num * 2)])
            return True
        elif hero.current_cell.is_in_objective_zone is False:
            self.fixed.move_my_hero(world, hero, self.fixed.zone_cell[5 + int(hero.id * 2)])
            return True
        if world.manhattan_distance(hero.current_cell, opp_hero.current_cell) > 4:
            self.fixed.move_my_hero(world, hero, self.fixed.near_of_fucking_nemy(world, opp_hero.current_cell)[self.blaster_num])
            return True
        else:
            return None


    def action(self, world, hero):
        self.fixed.fear_the_fucking_enemy(world, hero)
        self.fixed.attak_to_fucking_enemy(world, hero, self.Model.AbilityName.BLASTER_BOMB)
        self.fixed.attak_to_fucking_enemy(world, hero, self.Model.AbilityName.BLASTER_ATTACK)

    # def move(self, world, hero, phase):
    #     if phase == "move":
    #         opp_hero = self.find_fucking_enemy_for_attack(world, hero)
    #         if opp_hero is None:
    #             self.fixed.move_my_hero(world, hero, self.fixed.zone_cell[15])
    #             return True
    #         if world.manhattan_distance(hero.current_cell, opp_hero.current_cell) > 4:
    #             self.fixed.move_my_hero(world, hero, opp_hero.current_cell)
    #             return True
    #         elif hero.current_cell.is_in_objective_zone is False:
    #             self.fixed.move_my_hero(world, hero, opp_hero.current_cell)
    #             return True
    #         else:
    #             return None
    #     elif phase == "action":
    #         self.fixed.fear_the_fucking_enemy(world, hero)


    def find_fucking_enemy_for_attack(self, world, hero):
        ret = None
        for opp_hero in world.opp_heroes:
            if opp_hero.current_cell.row == -1:
                continue
            if opp_hero.current_cell.is_in_objective_zone is False:
                continue
            if ret is None:
                ret = opp_hero
                continue
            if ret.current_hp < opp_hero.current_hp:
                continue
            if world.manhattan_distance(hero.current_cell, opp_hero.current_cell) > world.manhattan_distance(hero.current_cell, ret.current_cell):
                continue
            ret = opp_hero
        return ret