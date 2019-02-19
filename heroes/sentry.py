class sentry:


    def __init__(self, Model, fixed, world):
        self.Model = Model
        self.fixed = fixed
        # world = world

    def move(self, world, hero):
        if world.move_phase_num == 1 :
            if world.current_turn < 10:
                "nothing"
            # elif world.current_turn < 15:
            else:
                if hero.current_cell.is_in_objective_zone is False:
                    self.fixed.goal_cell["sentry"] = self.fixed.zone_cell[2] if (world.get_hero_by_cell(allegiance=world.my_heroes,cell=self.fixed.zone_cell[2]) is None) else self.fixed.zone_cell[8]
                else:
                    self.fixed.goal_cell["sentry"] = self.fixed.go_to_fucking_enemy(world, hero).current_cell


        self.fixed.move_my_hero(world, hero, self.fixed.goal_cell["sentry"])


    
    def action(self, world, hero):
        self.fixed.attak_to_fucking_enemy(world, hero, self.Model.AbilityName.SENTRY_RAY)
        self.fixed.attak_to_fucking_enemy(world, hero, self.Model.AbilityName.SENTRY_ATTACK)


    