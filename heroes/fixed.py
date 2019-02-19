
class fixed:

    def __init__(self, randint, world, Model):
        self.goal_cell = {
            "healer": self.zone_cell[0],
            "sentry": self.zone_cell[4],
            "blaster":[    
                self.zone_cell[(self.zone_size["row"] + 2)],
                self.zone_cell[(self.zone_size["row"] + 1)],
                self.zone_cell[0],
                self.zone_cell[3],
            ],
            "guardian": [
                self.zone_cell[0],
                self.zone_cell[4],
            ] 
        }
        self.set_zone(world)
        self.guardian_num = 0
        self.randint = randint
        self.heros_cell = {}
        self.Model = Model
    def move_my_hero(self, world, hero, end):
        
        not_pass = self.heros_cell
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
        self.heros_cell[hero.id] = hero.current_cell

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

### *** ## ** # * ACTION * # ** ## *** ###


    # def enemy_cooldown(self, world):
    #     for casted in world.opp_cast_abilities:
            

    # like fear the walkin dead :D
    def fear_the_fucking_enemy(self, world, hero, ability):
        # fast move for hero (with action hero can recive to zone object faster)

        # dodge when enemy ability is ready and attack after dodge (it's should not do more than 2/4 hero  in 1 action )
        for opp_hero in world.opp_heroes:
            if opp_hero.current_cell.row == -1:
                continue
            if opp_hero.name == self.Model.HeroName.HEALER | opp_hero.respawn_time > 0:
                continue
            

    def attak_to_fucking_enemy(self, world, hero, ability):
        for opp_hero in world.opp_heroes:
            if hero.get_ability(ability).is_ready() is not True:
                break
            if opp_hero.current_cell.row == -1 | opp_hero.current_cell.column == -1:
                continue
            targets = world.get_ability_targets(
                ability_name=ability,
                start_cell=hero.current_cell,
                target_cell=opp_hero.current_cell,
            )
            exist_target = None
            for target in targets:
                if (target.current_cell.row != -1 or target.current_cell.column != -1):
                    if exist_target is None:
                        exist_target = target
                    elif exist_target.current_hp > target.current_hp:
                        exist_target = target
            if exist_target is None:
                return None
            world.cast_ability(
                hero=hero,
                ability_name=ability,
                cell=exist_target.current_cell,
            )
            return True



### *** ## ** # * FIRST SETS * # ** ## *** ###


    def set_zone(self, world):
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
        first_cell = {"row": self.zone_cell[0].row, "column": self.zone_cell[0].column}
        last_cell = {}
        for this_size in self.zone_cell:
            if this_size.row == first_cell["row"]:
                last_cell["column"] = this_size.column
            if this_size.column == first_cell["column"]:
                last_cell["row"] = this_size.row
        self.zone_size = {
            "row": last_cell["row"] - first_cell["row"],
            "column": last_cell["column"] - first_cell["column"],
        }
