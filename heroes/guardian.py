class guardian:

    def __init__(self, Model, fixed, world):
        self.Model = Model
        self.fixed = fixed
        

    def move(self, world, hero):
        print ("write here")
        self.guardian_num = 0 if self.guardian_num == 1 else 1 
        if world.move_phase_num == 1 :
            if world.current_turn < 10:
                "nothing"
            # elif world.current_turn < 15:
            else:
                if hero.current_cell.is_in_objective_zone is False:
                    self.fixed.goal_cell["guardian"][self.fixed.guardian_num] = self.fixed.zone_cell[1] if (world.get_hero_by_cell(allegiance=world.my_heroes,cell=self.fixed.zone_cell[1]) is None) else self.fixed.zone_cell[9]
                else:
                    self.fixed.goal_cell["guardian"][self.fixed.guardian_num] = self.fixed.go_to_fucking_enemy(hero).current_cell

        self.fixed.move_my_hero(world, hero, self.fixed.goal_cell["guardian"][self.guardian_num])

    
    
    def action(self, world, hero):
        print ("write here")

    
    def move_my_hero(self, world, hero, end):
        
        not_pass = self.fixed.heros_cell
        if hero.id in not_pass:
            del not_pass[hero.id]


        ways = world.get_path_move_directions(
            start_cell=hero.current_cell,
            end_cell=end,
            not_pass=not_pass.values(),
        )
        
        if len(ways) < 1:
            # print("len is less: ", len(ways))
            return None
        check_way = {
            self.Model.Direction.UP: [hero.current_cell.row - 1, hero.current_cell.column],
            self.Model.Direction.DOWN: [hero.current_cell.row + 1, hero.current_cell.column],
            self.Model.Direction.LEFT: [hero.current_cell.row, hero.current_cell.column - 1],
            self.Model.Direction.RIGHT: [hero.current_cell.row, hero.current_cell.column + 1]
            }.get(ways[0], None)
        if check_way is None:
            print("WARN: ",ways[0])
        elif hero.current_cell.is_in_objective_zone is True and world.map.get_cell(check_way[0], check_way[1]).is_in_objective_zone is False:
            # print("hero: ",hero.current_cell.is_in_objective_zone, " | next :",world.map.get_cell(check_way[0], check_way[1]).is_in_objective_zone )
            return False

        # for way in ways:
        world.move_hero(hero=hero, direction=ways[0])
        self.fixed.heros_cell[hero.id] = hero.current_cell

    def go_to_fucking_enemy(self, world, hero):
        exist_enemy = None
        for e_hero in world.opp_heroes:
            if e_hero.current_cell.is_in_objective_zone is True:
                if exist_enemy is None:
                    exist_enemy = e_hero
                    continue
                exist_manhattan = world.manhattan_distance(hero.current_cell, exist_enemy.current_cell)
                this_manhattan = world.manhattan_distance(hero.current_cell, e_hero.current_cell)
                if exist_enemy.current_hp > e_hero.current_hp:
                    if this_manhattan <= exist_manhattan | (exist_manhattan - this_manhattan) < 5:
                        exist_enemy = e_hero
                elif this_manhattan <= exist_manhattan:
                    exist_enemy = e_hero
        if exist_enemy is None:
            return hero
        else:
            return exist_enemy

