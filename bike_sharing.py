class Bike:
    def __init__(self, bike_id, model):
        self.__bike_id = bike_id
        self.__model = model
        self.__available = True

    def get_id(self):
        return self.__bike_id

    def get_model(self):
        return self.__model

    def is_available(self):
        return self.__available

    def take(self):
        if not self.__available:
            print("Bike", self.__bike_id, "is already taken")
            return False
        self.__available = False
        return True

    def give_back(self):
        self.__available = True

    def __str__(self):
        if self.__available:
            status = "available"
        else:
            status = "in use"
        return "Bike " + self.__bike_id + " (" + self.__model + ") - " + status


class Station:
    def __init__(self, name, capacity):
        self.__name = name
        self.__capacity = capacity
        self.__bikes = []

    def get_name(self):
        return self.__name

    def is_full(self):
        return len(self.__bikes) >= self.__capacity

    def add_bike(self, bike):
        if self.is_full():
            print("Station", self.__name, "is full")
            return False
        self.__bikes.append(bike)
        return True

    def remove_bike(self):
        for bike in self.__bikes:
            if bike.is_available():
                self.__bikes.remove(bike)
                return bike
        print("No bikes at station", self.__name)
        return None

    def show(self):
        print("Station:", self.__name, "(" + str(len(self.__bikes)) + "/" + str(self.__capacity) + ")")
        for bike in self.__bikes:
            print("   ", bike)


class User:
    def __init__(self, name, balance):
        self.__name = name
        self.__balance = balance
        self.__rental = None

    def get_name(self):
        return self.__name

    def get_balance(self):
        return self.__balance

    def get_rental(self):
        return self.__rental

    def set_rental(self, rental):
        self.__rental = rental

    def add_money(self, amount):
        if amount <= 0:
            print("Amount must be positive")
            return
        self.__balance += amount

    def pay(self, amount):
        if amount > self.__balance:
            print(self.__name, "does not have enough money")
            return False
        self.__balance -= amount
        return True

    def __str__(self):
        return self.__name + " - balance: " + str(self.__balance)


class Rental:
    PRICE_PER_MINUTE = 0.1

    def __init__(self, user, bike, station):
        self.__user = user
        self.__bike = bike
        self.__start_station = station
        self.__end_station = None
        self.__minutes = 0
        self.__price = 0

    def get_bike(self):
        return self.__bike

    def get_price(self):
        return self.__price

    def finish(self, station, minutes):
        self.__end_station = station
        self.__minutes = minutes
        self.__price = round(minutes * Rental.PRICE_PER_MINUTE, 2)

    def __str__(self):
        text = self.__user.get_name() + " rented " + self.__bike.get_id()
        text += " from " + self.__start_station.get_name()
        if self.__end_station is not None:
            text += " to " + self.__end_station.get_name()
            text += ", " + str(self.__minutes) + " min, price: " + str(self.__price)
        return text


class BikeSharingSystem:
    def __init__(self):
        self.__stations = []
        self.__users = []

    def add_station(self, station):
        self.__stations.append(station)

    def add_user(self, user):
        self.__users.append(user)

    def rent_bike(self, user, station):
        if user.get_rental() is not None:
            print(user.get_name(), "already has a bike")
            return
        if user.get_balance() <= 0:
            print(user.get_name(), "has no money")
            return

        bike = station.remove_bike()
        if bike is None:
            return

        bike.take()
        rental = Rental(user, bike, station)
        user.set_rental(rental)
        print(rental)

    def return_bike(self, user, station, minutes):
        rental = user.get_rental()
        if rental is None:
            print(user.get_name(), "has no bike to return")
            return
        if station.is_full():
            print("Station", station.get_name(), "is full")
            return

        rental.finish(station, minutes)
        user.pay(rental.get_price())
        bike = rental.get_bike()
        bike.give_back()
        station.add_bike(bike)
        user.set_rental(None)
        print(rental)

    def show(self):
        print("----------------------")
        for station in self.__stations:
            station.show()
        for user in self.__users:
            print(user)
        print("----------------------")


system = BikeSharingSystem()

station1 = Station("Central Park", 3)
station2 = Station("University", 2)
system.add_station(station1)
system.add_station(station2)

station1.add_bike(Bike("B1", "City"))
station1.add_bike(Bike("B2", "City"))
station2.add_bike(Bike("B3", "Sport"))

ali = User("Ali", 20)
madina = User("Madina", 10)
system.add_user(ali)
system.add_user(madina)

system.show()

system.rent_bike(ali, station1)
system.rent_bike(madina, station2)
system.rent_bike(ali, station1)

system.return_bike(ali, station2, 25)
system.return_bike(madina, station1, 18)
system.return_bike(madina, station1, 5)

system.show()

ali.add_money(-5)
print(ali.get_balance())
