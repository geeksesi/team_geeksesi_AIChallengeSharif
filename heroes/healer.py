class healer:

    def __init__(self, Model, fixed, world):
        self.Model = Model
        self.fixed = fixed
        self.world = world


    def move(self, hero):
        print ("write here")
        if self.world.move_phase_num == 1 :
            if self.world.current_turn < 8:
                # print("nothing")
                "nothing"
            # elif self.world.current_turn < 15:
            else:
                need_heal = None
                for team_hero in self.world.my_heroes:
                    if team_hero.current_hp < (team_hero.max_hp - 20):
                        if need_heal is None:
                            need_heal = team_hero
                        elif (need_heal.max_hp - need_heal.current_hp) < (team_hero.max_hp - team_hero.current_hp):
                            need_manhattan = self.world.manhattan_distance(hero.current_cell, need_heal.current_cell)
                            this_manhattan = self.world.manhattan_distance(hero.current_cell, team_hero.current_cell)
                            if need_manhattan > this_manhattan | (need_manhattan - this_manhattan) < 3:
                                need_heal = team_hero
                if hero.current_cell.is_in_objective_zone is False:
                    self.fixed.goal_cell["healer"] = self.fixed.zone_cell[0] if (self.world.get_hero_by_cell(allegiance=self.world.my_heroes,cell=self.fixed.zone_cell[0]) is None) else self.fixed.zone_cell[10]
                elif need_heal is None:
                    self.fixed.goal_cell["healer"] = hero.current_cell
                else:
                    self.fixed.goal_cell["healer"] = need_heal.current_cell
            # self.fixed.goal_cell["healer"] = 
        self.fixed.move_my_hero(self.world, hero, self.fixed.goal_cell["healer"])




    def action(self,  hero):
        for other_hero in self.world.my_heroes:
            if other_hero is hero:
                continue
            if other_hero.current_hp <= (other_hero.max_hp - 30):
                if hero.get_ability(self.Model.AbilityName.HEALER_HEAL).is_ready() is True:
                    targets = self.world.get_ability_targets(
                        ability_name=self.Model.AbilityName.HEALER_HEAL,
                        start_cell=hero.current_cell,
                        target_cell=other_hero.current_cell,
                    )
                    for target in targets:
                        if target.current_hp < target.max_hp - 30:
                            self.world.cast_ability(
                                hero=hero,
                                ability_name=self.Model.AbilityName.HEALER_HEAL,
                                cell=target.current_cell,
                            )
                            print("healer heled")

                self.fixed.attak_to_fucking_enemy(self.world, hero, self.Model.AbilityName.HEALER_ATTACK)
