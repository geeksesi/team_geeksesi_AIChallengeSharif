
class fixed:

    def __init__(self, randint, world, Model):
        self.zone_cell = []
        self.zone_size = {}
        self.set_zone(world)
        self.e_cooldown = {}
        self.guardian_num = 0
        self.randint = randint
        self.heros_cell = {}
        self.Model = Model
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
    def move_my_hero(self, world, hero, end):
        if world.current_turn < 7:
            ways = world.get_path_move_directions(
                start_cell=hero.current_cell,
                end_cell=end,
            )
        else:                
            not_pass = self.heros_cell
            if hero.id in not_pass:
                del not_pass[hero.id]
            ways = world.get_path_move_directions(
                start_cell=hero.current_cell,
                end_cell=end,
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
            return None
        elif hero.current_cell.is_in_objective_zone is True and world.map.get_cell(check_way[0], check_way[1]).is_in_objective_zone is False:
            # print("hero: ",hero.current_cell.is_in_objective_zone, " | next :",world.map.get_cell(check_way[0], check_way[1]).is_in_objective_zone )
            return False

        # for way in ways:
        world.move_hero(hero=hero, direction=ways[0])
        self.heros_cell[hero.id] = hero.current_cell

    def find_fucking_enemy(self, world, hero):
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

    def near_of_fucking_nemy(self, world, enemy_cell):
        row = enemy_cell.row
        column = enemy_cell.column
        # we can make 9 cell but we need 3 cell :
        one = world.map.get_cell((row - 2), (column - 2)) 
        if one.is_in_objective_zone is False:
            one = world.map.get_cell((row + 2), (column + 2)) 
            if one.is_in_objective_zone is False:
                one = world.map.get_cell((row - 1), (column - 1)) 
                if one.is_in_objective_zone is False:
                    one = world.map.get_cell((row + 1), (column + 1)) 
                            

        two = world.map.get_cell((row - 2), (column + 2)) 
        if two.is_in_objective_zone is False:
            two = world.map.get_cell((row + 2), (column - 2)) 
            if two.is_in_objective_zone is False:
                two = world.map.get_cell((row + 1), (column - 1)) 
                if two.is_in_objective_zone is False:
                    two = world.map.get_cell((row + 1), (column - 1)) 


        three = world.map.get_cell((row), (column - 4)) 
        if three.is_in_objective_zone is False:
            three = world.map.get_cell((row), (column - 3)) 
            if three.is_in_objective_zone is False:
                three = world.map.get_cell((row), (column - 2)) 
                if three.is_in_objective_zone is False:
                    three = world.map.get_cell((row), (column - 1)) 
                    if three.is_in_objective_zone is False:
                        three = world.map.get_cell((row), (column + 1)) 
                        if three.is_in_objective_zone is False:
                            three = world.map.get_cell((row), (column + 2)) 

        four = world.map.get_cell((row - 4), (column)) 
        if four.is_in_objective_zone is False:
            four = world.map.get_cell((row- 3), (column)) 
            if four.is_in_objective_zone is False:
                four = world.map.get_cell((row - 2), (column)) 
                if four.is_in_objective_zone is False:
                    four = world.map.get_cell((row - 1), (column)) 
                    if four.is_in_objective_zone is False:
                        four = world.map.get_cell((row + 1), (column)) 
                        if four.is_in_objective_zone is False:
                            four = world.map.get_cell((row + 1), (column)) 

        ret = [one, two, three, four]
        return ret


### *** ## ** # * ACTION * # ** ## *** ###

    def set_enemy_ability(self, world):
        self.e_cooldown = {}
        for opp_hero in world.opp_heroes:
            self.e_cooldown[opp_hero.id] = {}
            for e_ability in opp_hero.abilities:
                # print(self.e_cooldown[opp_hero.id])
                self.e_cooldown[opp_hero.id][str(e_ability.name)] = 0
        
    def turn_enemy_ability(self, world):
        for opp_hero in world.opp_heroes:
            for e_ability in opp_hero.abilities:
                if self.e_cooldown[opp_hero.id][str(e_ability.name)] != 0:
                    self.e_cooldown[opp_hero.id][str(e_ability.name)] -= 1
                else: 
                    continue

    def enemy_cooldown(self, world):
        for casted in world.opp_cast_abilities:
            if world.get_hero(casted.caster_id).name is None:
                continue
            self.e_cooldown[casted.caster_id][str(casted.ability_name)] +=  world.get_hero(casted.caster_id).get_ability(casted.ability_name).cooldown

    #it's fucking function and don't work :( because low AP...always... i should fix move...
    # like fear the walkin dead :D
    def fear_the_fucking_enemy(self, world, hero):
        if world.ap < 50:
            return None
        # fast move for hero (with action hero can recive to zone object faster)

        # dodge when enemy ability is ready and attack after dodge (it's should not do more than 2/4 hero  in 1 action )
        if hero.current_hp > 50:
            return None
        if hero.abilities[1].is_ready() is False:
            return None
        finish_point = [0,0]
        for opp_hero in world.opp_heroes:
            if opp_hero.current_cell.row == -1:
                continue
            if opp_hero.respawn_time > 0:
                continue
            if opp_hero.name == self.Model.HeroName.HEALER:
                continue
            if world.manhattan_distance(hero.current_cell, opp_hero.current_cell) > 5:
                if opp_hero.name != self.Model.HeroName.BLASTER:
                    continue
                else:
                    # print(self.e_cooldown[opp_hero.id])
                    if self.e_cooldown[opp_hero.id]["AbilityName.BLASTER_BOMB"] > 0:
                        continue
            if self.e_cooldown[opp_hero.id][str(opp_hero.abilities[0].name)] > 0:
                if opp_hero.name == self.Model.HeroName.guardian:
                    continue
                if self.e_cooldown[opp_hero.id][str(opp_hero.abilities[2].name)] > 0:
                    continue
            # Now this hero must jump :) 
            while True:
                if self.zone_cell[0].row - hero.current_cell.row > 0 :
                    finish_point[0] = hero.current_cell.row + self.randint(0,4)
                else:
                    finish_point[0] = hero.current_cell.row - self.randint(0,4)

                if self.zone_cell[0].column - hero.current_cell.column > 0 :
                    finish_point[1] = hero.current_cell.column + self.randint(0,4)
                else:
                    finish_point[1] = hero.current_cell.column - self.randint(0,4)

                if world.manhattan_distance(hero.current_cell, world.map.get_cell(finish_point[0], finish_point[1])) > hero.abilities[1].area_of_effect:
                    continue
                world.cast_ability(hero=hero, ability=hero.abilities[1], cell=world.map.get_cell(finish_point[0], finish_point[1]))
                print(hero.name, "dodged")
                break


    def attak_to_fucking_enemy(self, world, hero, ability):
        if hero.get_ability(ability).is_ready() is not True:
            return None
        for opp_hero in world.opp_heroes:
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
            # print("{0} doed {1}".format(hero.name, ability))
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
