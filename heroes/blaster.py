
class blaster:

    def __init__(self, Model, fixed, world):
        self.Model = Model
        self.fixed = fixed
        self.world = world

    def move(self, hero):
        print ("write here")
        self.blaster_num = 0 if self.blaster_num == 3 else (self.blaster_num + 1) 
        if self.world.move_phase_num == 1 :
            if self.world.current_turn < 10:
                "nothing"
            # elif self.world.current_turn < 15:
            else:
                if hero.current_cell.is_in_objective_zone is False:
                    self.fixed.goal_cell["blaster"][self.blaster_num] = self.fixed.zone_cell[3] if (self.world.get_hero_by_cell(allegiance=self.world.my_heroes,cell=self.fixed.zone_cell[3]) is None) else self.fixed.zone_cell[7]
                else:
                    true_cell = self.fixed.go_to_fucking_enemy(self.world, hero).current_cell
                    self.fixed.goal_cell = self.world.map.get_cell(true_cell.row - (self.fixed.randint(0, 2)), true_cell.column - (self.fixed.randint(0, 2)))
                    self.fixed.goal_cell["blaster"][self.blaster_num] =  self.fixed.goal_cell


        self.fixed.move_my_hero(self.world, hero, self.fixed.goal_cell["blaster"][self.blaster_num])


    def action(self, hero):
        self.fixed.attak_to_fucking_enemy(self.world, hero, self.Model.AbilityName.BLASTER_BOMB)
        self.fixed.attak_to_fucking_enemy(self.world, hero, self.Model.AbilityName.BLASTER_ATTACK)
        print ("write here")

    