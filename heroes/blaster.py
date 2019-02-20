
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
        if world.move_phase_num == 1 :
            # print("move phase number ~>",world.move_phase_num)
            if world.current_turn < 10:
                "nothing"
            # elif world.current_turn < 15:
            else:
                if hero.current_cell.is_in_objective_zone is False:
                    # self.fixed.goal_cell["blaster"][self.blaster_num] = self.fixed.zone_cell[3] if (world.get_hero_by_cell(allegiance=world.my_heroes,cell=self.fixed.zone_cell[3]) is None) else self.fixed.zone_cell[7]
                    self.fixed.goal_cell["blaster"][self.blaster_num] = self.respawn_goal[self.blaster_num]
                else:
                    true_cell = self.fixed.go_to_fucking_enemy(world, hero).current_cell
                    goal_cell = world.map.get_cell(true_cell.row - (self.fixed.randint(0, 2)), true_cell.column - (self.fixed.randint(0, 2)))
                    self.fixed.goal_cell["blaster"][self.blaster_num] =  goal_cell


        self.fixed.move_my_hero(world, hero, self.fixed.goal_cell["blaster"][self.blaster_num])


    def action(self, world, hero):
        self.fixed.fear_the_fucking_enemy(world, hero)
        self.fixed.attak_to_fucking_enemy(world, hero, self.Model.AbilityName.BLASTER_BOMB)
        self.fixed.attak_to_fucking_enemy(world, hero, self.Model.AbilityName.BLASTER_ATTACK)

