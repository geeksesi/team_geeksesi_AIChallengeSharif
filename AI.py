import Model
from random import randint
from heroes import sentry, healer, guardian, blaster
from sentry import sentry
from blaster import blaster
from guardian import guardian 
from healer import healer 

class AI:
    def preprocess(self, world):
        print("preprocess")
        self.sentry = sentry()
        self.blaster = blaster()
        self.healer = healer()
        self.guardian = guardian()
        self.which_pick = 0
        self.set_zone(world)
        self.set_goal_cell(world)

    def pick(self, world):
        print("pick")

        # if self.which_pick == 0:
            # world.pick_hero(Model.HeroName.GUARDIAN)
            # world.pick_hero(Model.HeroName.SENTRY)
        # elif self.which_pick == 1:
            # world.pick_hero(Model.HeroName.GUARDIAN)
            # world.pick_hero(Model.HeroName.HEALER)
        # else:
        world.pick_hero(Model.HeroName.BLASTER)

        self.which_pick += 1

    def move(self, world):
        # print ("AP : ",world.ap)
        # self.visible_enemy
        self.heros_cell = {}
        for hero in world.my_heroes:
            if hero.respawn_time != 0:
                continue
            self.heros_cell[hero.id] = hero.current_cell

        # i = 0
        for hero in world.my_heroes:
            if hero.respawn_time != 0:
                continue
            # print(hero.name)
            if hero.name == Model.HeroName.SENTRY:
                self.sentry.move(world, hero)
            elif hero.name == Model.HeroName.BLASTER:
                self.blaster.move(world, hero)
            elif hero.name == Model.HeroName.GUARDIAN:
                self.guardian.move(world, hero)
            elif hero.name == Model.HeroName.HEALER:
                self.healer.move(world, hero)

    def action(self, world):
        print(world.current_turn)
        print("action")
        for hero in world.my_heroes:
            if hero.respawn_time != 0:
                continue
            # print(hero.name)
            if hero.name == Model.HeroName.SENTRY:
                self.sentry.action(world, hero)
            elif hero.name == Model.HeroName.BLASTER:
                self.blaster.action(world, hero)
            elif hero.name == Model.HeroName.GUARDIAN:
                self.guardian.action(world, hero)
            elif hero.name == Model.HeroName.HEALER:
                self.healer.action(world, hero)


        print("my_score: ", world.my_score)


### *** ## ** # * MOVE * # ** ## *** ###


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
            Model.Direction.UP: [hero.current_cell.row - 1, hero.current_cell.column],
            Model.Direction.DOWN: [hero.current_cell.row + 1, hero.current_cell.column],
            Model.Direction.LEFT: [hero.current_cell.row, hero.current_cell.column - 1],
            Model.Direction.RIGHT: [hero.current_cell.row, hero.current_cell.column + 1]
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

    def guardian_move(self, world, hero):
        self.guardian_num = 0 if self.guardian_num == 1 else 1 
        if world.move_phase_num == 1 :
            if world.current_turn < 10:
                "nothing"
            # elif world.current_turn < 15:
            else:
                if hero.current_cell.is_in_objective_zone is False:
                    self.goal_cell["guardian"][self.guardian_num] = self.zone_cell[1] if (world.get_hero_by_cell(allegiance=world.my_heroes,cell=self.zone_cell[1]) is None) else self.zone_cell[9]
                else:
                    self.goal_cell["guardian"][self.guardian_num] = self.go_to_fucking_enemy(world, hero).current_cell

        self.move_my_hero(world, hero, self.goal_cell["guardian"][self.guardian_num])


    def sentry_move(self, world, hero):
        if world.move_phase_num == 1 :
            if world.current_turn < 10:
                "nothing"
            # elif world.current_turn < 15:
            else:
                if hero.current_cell.is_in_objective_zone is False:
                    self.goal_cell["sentry"] = self.zone_cell[2] if (world.get_hero_by_cell(allegiance=world.my_heroes,cell=self.zone_cell[2]) is None) else self.zone_cell[8]
                else:
                    self.goal_cell["sentry"] = self.go_to_fucking_enemy(world, hero).current_cell


        self.move_my_hero(world, hero, self.goal_cell["sentry"])

    def blaster_move(self, world, hero):
        self.blaster_num = 0 if self.blaster_num == 3 else (self.blaster_num + 1) 
        if world.move_phase_num == 1 :
            if world.current_turn < 10:
                "nothing"
            # elif world.current_turn < 15:
            else:
                if hero.current_cell.is_in_objective_zone is False:
                    self.goal_cell["blaster"][self.blaster_num] = self.zone_cell[3] if (world.get_hero_by_cell(allegiance=world.my_heroes,cell=self.zone_cell[3]) is None) else self.zone_cell[7]
                else:
                    true_cell = self.go_to_fucking_enemy(world, hero).current_cell
                    goal_cell = world.map.get_cell(true_cell.row - (randint(0, 2)), true_cell.column - (randint(0, 2)))
                    self.goal_cell["blaster"][self.blaster_num] =  goal_cell


        self.move_my_hero(world, hero, self.goal_cell["blaster"][self.blaster_num])


    def healer_move(self, world, hero):
        if world.move_phase_num == 1 :
            if world.current_turn < 8:
                # print("nothing")
                "nothing"
            # elif world.current_turn < 15:
            else:
                need_heal = None
                for team_hero in world.my_heroes:
                    if team_hero.current_hp < (team_hero.max_hp - 20):
                        if need_heal is None:
                            need_heal = team_hero
                        elif (need_heal.max_hp - need_heal.current_hp) < (team_hero.max_hp - team_hero.current_hp):
                            need_manhattan = world.manhattan_distance(hero.current_cell, need_heal.current_cell)
                            this_manhattan = world.manhattan_distance(hero.current_cell, team_hero.current_cell)
                            if need_manhattan > this_manhattan | (need_manhattan - this_manhattan) < 3:
                                need_heal = team_hero
                if hero.current_cell.is_in_objective_zone is False:
                    self.goal_cell["healer"] = self.zone_cell[0] if (world.get_hero_by_cell(allegiance=world.my_heroes,cell=self.zone_cell[0]) is None) else self.zone_cell[10]
                elif need_heal is None:
                    self.goal_cell["healer"] = hero.current_cell
                else:
                    self.goal_cell["healer"] = need_heal.current_cell
            # self.goal_cell["healer"] = 
        self.move_my_hero(world, hero, self.goal_cell["healer"])



### *** ## ** # * ACTION * # ** ## *** ###

    def enemy_cooldown(self, world):
        for casted in world.opp_cast_abilities:
            

    # like fear the walkin dead :D
    def fear_the_fucking_enemy(self, world, hero, ability):
        # fast move for hero (with action hero can recive to zone object faster)

        # dodge when enemy ability is ready and attack after dodge (it's should not do more than 2/4 hero  in 1 action )
        for opp_hero in world.opp_heroes:
            if opp_hero.current_cell.row == -1:
                continue
            if opp_hero.name == Model.HeroName.HEALER | opp_hero.respawn_time > 0:
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


    def guardian_action(self, world, hero):

        self.attak_to_fucking_enemy(world, hero, Model.AbilityName.GUARDIAN_ATTACK)
        # self.attak_to_fucking_enemy(world, hero, Model.AbilityName.SENTRY_ATTACK)

    def sentry_action(self, world, hero):

        self.attak_to_fucking_enemy(world, hero, Model.AbilityName.SENTRY_RAY)
        self.attak_to_fucking_enemy(world, hero, Model.AbilityName.SENTRY_ATTACK)


    def blaster_action(self, world, hero):

        self.attak_to_fucking_enemy(world, hero, Model.AbilityName.BLASTER_BOMB)
        self.attak_to_fucking_enemy(world, hero, Model.AbilityName.BLASTER_ATTACK)
               

    def healer_action(self, world, hero):
        for other_hero in world.my_heroes:
            if other_hero is hero:
                continue
            if other_hero.current_hp <= (other_hero.max_hp - 30):
                if hero.get_ability(Model.AbilityName.HEALER_HEAL).is_ready() is True:
                    targets = world.get_ability_targets(
                        ability_name=Model.AbilityName.HEALER_HEAL,
                        start_cell=hero.current_cell,
                        target_cell=other_hero.current_cell,
                    )
                    for target in targets:
                        if target.current_hp < target.max_hp - 30:
                            world.cast_ability(
                                hero=hero,
                                ability_name=Model.AbilityName.HEALER_HEAL,
                                cell=target.current_cell,
                            )
                            print("healer heled")

                self.attak_to_fucking_enemy(world, hero, Model.AbilityName.HEALER_ATTACK)




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


    def set_goal_cell(self, world):
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
