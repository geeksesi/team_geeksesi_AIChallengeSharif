class sentry:


    def __init__(self, Model, fixed, world):
        self.Model = Model
        self.fixed = fixed
        self.world = world

    def move(self,  hero):
        print ("write here")
        if self.world.move_phase_num == 1 :
            if self.world.current_turn < 10:
                "nothing"
            # elif self.world.current_turn < 15:
            else:
                if hero.current_cell.is_in_objective_zone is False:
                    self.fixed.goal_cell["sentry"] = self.fixed.zone_cell[2] if (self.world.get_hero_by_cell(allegiance=self.world.my_heroes,cell=self.fixed.zone_cell[2]) is None) else self.fixed.zone_cell[8]
                else:
                    self.fixed.goal_cell["sentry"] = self.fixed.go_to_fucking_enemy(self.world, hero).current_cell


        self.fixed.move_my_hero(self.world, hero, self.fixed.goal_cell["sentry"])


    
    def action(self, hero):
        print ("write here")
        self.fixed.attak_to_fucking_enemy(self.world, hero, self.Model.AbilityName.SENTRY_RAY)
        self.fixed.attak_to_fucking_enemy(self.world, hero, self.Model.AbilityName.SENTRY_ATTACK)


    