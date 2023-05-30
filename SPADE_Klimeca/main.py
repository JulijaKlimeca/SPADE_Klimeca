import asyncio
import random
import time

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

start_time = time.time()

print("--- %s seconds ---" % (time.time() - start_time))

#agenta parliecibas
class Belief:
    def __init__(self):
        self.chargelevel = 1.0
        self.carry_pack = None
        self.packs = []
        self.poststations = []
        self.chargers = []

#agenta velmes
class Desire:
    def __init__(self):
        self.charge_status = 0.2
        self.pack_prior = 1

#agenta nodomi
class Intention:
    def __init__(self):
        self.action = None
        self.target = None
        self.prior = 0


class Car:
    def __init__(self):
        self.location = (0, 0)
        self.chargelevel = 1.0
        self.carry_pack = None
        self.first_move = True

    def move_to(self, x, y):
        self.location = (x, y)
        if not self.first_move:
            self.chargelevel -= 0.1
        self.first_move = False

    def get_chargestate(self):
        return self.chargelevel

    def set_chargestate(self, charge):
        self.chargelevel = charge

    def get_carried_package(self):
        return self.carry_pack

    def set_carried_package(self, package):
        self.carry_pack = package


class Charger:
    def __init__(self, location):
        self.location = location

    def get_location(self):
        return self.location


class Package:
    def __init__(self, location):
        self.location = location

    def get_location(self):
        return self.location


class PostStation:
    def __init__(self, location):
        self.location = location
        self.packages = []

    def get_location(self):
        return self.location


class SensorActuator:
    def __init__(self):
        self.car = Car()
        self.chargers = [Charger((4, 4)), Charger((7, 1))]
        self.packs = [
            Package((3, 3)),
            Package((1, 5)),
            Package((6, 2)),
            Package((8, 7)),
            Package((2, 9)),
        ]
        self.poststations = [PostStation((8, 8)), PostStation((3, 7))]
        self.print_locations()
        time.sleep(3)

    def print_locations(self):
        print("Package Locations:")
        for i, package in enumerate(self.packs, start=1):
            print(f"\t{i}. Package {package.get_location()}")

        print("\nCharging Station Locations:")
        for i, charger in enumerate(self.chargers, start=1):
            print(f"\t{i}. Charger {charger.get_location()}")

        print("\nPost Station Locations:")
        for i, poststation in enumerate(self.poststations, start=1):
            print(f"\t{i}. Post Station {poststation.get_location()}")
        print("--------------------------------")

    def get_car(self):
        return self.car

    def get_charger(self):
        return self.chargers

    def get_packages(self):
        return self.packs

    def get_poststations(self):
        return self.poststations

    def move_to(self, x, y):
        prev_x, prev_y = self.car.location
        print("Agent location: ({}, {})".format(prev_x, prev_y))
        self.car.move_to(x, y)
        self.car.set_chargestate(max(0.0, self.car.get_chargestate()))
        print("Agent Battery level: {:.2%}".format(self.car.get_chargestate()))
        print("------------------------------------------------")

        # Agenta atrasanas vieta uzlades vai pasta stacija
        for i, poststation in enumerate(self.poststations):
            if (x, y) == poststation.get_location():
                print(f"POST STATION {i + 1}:")
                break

        for i, charger in enumerate(self.chargers):
            if (x, y) == charger.get_location():
                print(f"CHARGING STATION {i + 1}:")
                break

    async def run(self):
        while True:
            self.move_to(4, 4)  # braukt pie uzlades stacijas
            self.recharge(self.chargers[0], 1.0)  # uzladeties
            self.move_to(0, 0)  # braukt atpakal
            await asyncio.sleep(3)

    # agents uzladas
    def recharge(self, charger, charge_amount):
        # print("Recharge, the charger status is low!")
        print("Car Agent is charging the battery")
        current_charge = self.car.get_chargestate()
        target_charge = min(1.0, current_charge + charge_amount)

        for charge_level in range(int(current_charge * 100), int(target_charge * 100) + 1, 10):
            print("Battery charge level: {}%".format(charge_level))
            time.sleep(3)  

        self.car.set_chargestate(target_charge)
        print("Current charge level: {:.2%}".format(self.car.get_chargestate()))
        print("----------------------------------------------")

    def pick_up_package(self, package):
        print("Pickup the current package!")
        # print("----------------------------------------------")
        if package in self.packs:
            self.car.set_carried_package(package)
            self.packs.remove(package)

    def drop_package_in_poststation(self, package, poststation):
        print("Drop the current package!")
        print("----------------------------------------------")
        if self.car.get_carried_package() == package and poststation in self.poststations:
            self.car.set_carried_package(None)
            #  pievienot paku pasta stacijas sarakstam
            poststation.packages.append(package)

    # atrast tuvako uzlades staciju
    def get_nearest_charger(self):
        curr_x, curr_y = self.car.location
        min_distance = float('inf')
        nearest_charger = None
        for charger in self.chargers:
            charger_x, charger_y = charger.get_location()
            distance = abs(curr_x - charger_x) + abs(curr_y - charger_y)
            if distance < min_distance:
                min_distance = distance
                nearest_charger = charger
        return nearest_charger

    # atrast tuvako paku
    def get_nearest_package(self):
        curr_x, curr_y = self.car.location
        min_distance = float('inf')
        nearest_package = None
        for package in self.packs:
            package_x, package_y = package.get_location()
            distance = abs(curr_x - package_x) + abs(curr_y - package_y)
            if distance < min_distance:
                min_distance = distance
                nearest_package = package
        return nearest_package

    # atrast tuvako pasta staciju
    def get_nearest_poststation(self):
        curr_x, curr_y = self.car.location
        min_distance = float('inf')
        nearest_poststation = None
        for poststation in self.poststations:
            poststation_x, poststation_y = poststation.get_location()
            distance = abs(curr_x - poststation_x) + abs(curr_y - poststation_y)
            if distance < min_distance:
                min_distance = distance
                nearest_poststation = poststation
        return nearest_poststation


class color:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class PostCarAgent(Agent):
    class BeliefUpdateBehaviour(CyclicBehaviour):
        async def run(self):
            actsense = self.agent.sensor_actuator
            belief = self.agent.belief
            belief.chargelevel = actsense.get_car().get_chargestate()
            belief.carry_pack = actsense.get_car().get_carried_package()
            belief.packs = actsense.get_packages()
            belief.poststations = actsense.get_poststations()
            belief.chargers = actsense.get_charger()

            await asyncio.sleep(3)

    class PlanSelectionBehaviour(CyclicBehaviour):
        async def run(self):
            belief = self.agent.belief
            desire = self.agent.desire
            intention = self.agent.intention

            if belief.chargelevel <= desire.charge_status:
                nearest_charger = self.agent.actsense.get_nearest_charger()
                if nearest_charger:
                    intention.action = "recharge now "
                    intention.target = nearest_charger
                    intention.prior = 1
                    charger_index = belief.chargers.index(nearest_charger)
                    print(f"Charging Station {charger_index + 1} is chosen!")
                else:
                    intention.action = "explore environment now "
                    intention.target = (random.randint(0, 9), random.randint(0, 9))
                    intention.prior = 0

            elif belief.carry_pack is not None:
                poststations = belief.poststations
                if poststations:
                    nearest_poststation = self.agent.sensor_actuator.get_nearest_poststation()
                    intention.action = "drop package now "
                    intention.target = nearest_poststation
                    intention.prior = desire.pack_prior
                    print(f"Post station {poststations.index(nearest_poststation) + 1} is chosen!")
                else:
                    intention.action = "explore environment now "
                    intention.target = (random.randint(0, 9), random.randint(0, 9))
                    intention.prior = 0

            else:
                packs = belief.packs
                if packs:
                    package = packs[0]
                    intention.action = "pick up package now"
                    intention.target = package
                    intention.prior = desire.pack_prior
                else:
                    intention.action = "explore environment now "
                    intention.target = (random.randint(0, 9), random.randint(0, 9))
                    intention.prior = 0

            await asyncio.sleep(3)

    class ActionExecutionBehaviour(CyclicBehaviour):
        async def run(self):
            actsense = self.agent.sensor_actuator
            intention = self.agent.intention

            if intention.action == "recharge now ":
                charger = intention.target
                distance = abs(charger.get_location()[0] - actsense.get_car().location[0]) + abs(
                    charger.get_location()[1] - actsense.get_car().location[1])
                actsense.move_to(*charger.get_location())
                actsense.recharge(charger, 1.0)
                self.agent.belief.chargelevel = actsense.get_car().get_chargestate()

            elif intention.action == "pick up package now":
                package = intention.target
                actsense.move_to(*package.get_location())
                actsense.pick_up_package(package)


            elif intention.action == "drop package now ":
                package = actsense.get_car().get_carried_package()
                poststation = intention.target
                actsense.move_to(*poststation.get_location())
                actsense.drop_package_in_poststation(package, poststation)


            elif intention.action == "explore environment now ":
                target = intention.target
                actsense.move_to(*target)

            await asyncio.sleep(3)

    async def setup(self):
        # print("Car agent is starting the job . . .")
        print("Agent:", f"{self.jid} started the work")
        self.belief = Belief()
        self.desire = Desire()
        self.intention = Intention()
        self.sensor_actuator = SensorActuator()
        self.actsense = self.sensor_actuator

        self.add_behaviour(self.BeliefUpdateBehaviour())
        self.add_behaviour(self.PlanSelectionBehaviour())
        self.add_behaviour(self.ActionExecutionBehaviour())

# agentu skaits
if __name__ == "__main__":
    agent = PostCarAgent("julija@anonym.im", "julijaklim120202")
    '''agent2 = PostCarAgent("agent2@anonym.im", "agent2")
    agent3 = PostCarAgent("agent3@anonym.im", "agent3")
    agent4 = PostCarAgent("agent4@anonym.im", "agent4")
    agent5 = PostCarAgent("agent5@anonym.im", "agent5")
    agent6 = PostCarAgent("agent6@xmpp.xxx", "agent6")
    agent7 = PostCarAgent("agent7@xmpp.xxx", "agent7")
    agent8 = PostCarAgent("agent8@xmpp.xxx", "agent8")
    agent9 = PostCarAgent("agent9@xmpp.xxx", "agent9")
    agent10 = PostCarAgent("agent10@xmpp.xxx", "agent10")'''

    print(color.BOLD + 'To STOP the Car agent press ctrl+C' + color.END)
    print("-                                                                                 -")

    # agentu palaisana

    future = agent.start()
    future.result()

    '''future2 = agent2.start()
    future2.result()

    future3 = agent3.start()
    future3.result()

    future4 = agent4.start()
    future4.result()

    future5 = agent5.start()
    future5.result()

    future6 = agent6.start()
    future6.result()

    future7 = agent7.start()
    future7.result()

    future8 = agent8.start()
    future8.result()

    future9 = agent9.start()
    future9.result()

    future10 = agent10.start()
    future10.result()'''

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("  The agent is stopped!")

    # agentu apturesana

    agent.stop()
    '''agent2.stop()
    agent3.stop()
    agent4.stop()
    agent5.stop()
    agent6.stop()
    agent7.stop()
    agent8.stop()
    agent9.stop()
    agent10.stop()'''
