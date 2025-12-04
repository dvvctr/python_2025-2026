import threading
import random
import time

price_per_unit = 5
print_lock = threading.Lock()

class Warehouse:
    def __init__(self, name, meds): 
  
        self.name = name 
        self.meds = meds 
        self.lock = threading.Lock()

    def steal(self, amount):
        chance = random.random()

        if chance < 0.10:
            return 0, "СПІЙМАЛИ"
        
        elif chance < 0.40:
            actual_steal = amount // 2
            status = "ЧАСТКОВО"
        
        else:
            actual_steal = amount
            status = "УСПІХ"

        if actual_steal > self.meds:
            actual_steal = self.meds
            status = "ОЧИЩЕНО"

        self.meds -= actual_steal
        return actual_steal, status


class Runner(threading.Thread):
    def __init__(self, name, warehouse):
        super().__init__()
        self.name = name
        self.warehouse = warehouse
        self.earnings = 0

    def run(self):
        for i in range(10):
            amount_to_steal = random.randint(10, 30)
            
            with self.warehouse.lock:
                stolen, status = self.warehouse.steal(amount_to_steal)
                
            self.earnings += stolen * price_per_unit
            
            step = i + 1
            bar = "█" * step + "-" * (10 - step)
            
            with print_lock:
                print(f"{self.name:<10} [{bar}] Спроба {step}/10 | +{stolen*price_per_unit} грн ({status})")

            time.sleep(random.uniform(0.1, 0.5))


def run_simulation():
    print(f"===== ПОЧАТОК ОПЕРАЦІЇ =====")

    warehouses = [
        Warehouse(f"Склад-{i+1}", random.randint(100, 300)) 
        for i in range(random.randint(3, 5))
    ]

    print("Цілі (склади):")
    for w in warehouses:
        print(f" -> {w.name}: {w.meds} од.")
    print("-" * 40)

    runners = []
    names = ["Бігун-1", "Бігун-2", "Бігун-3", "Бігун-4", "Бігун-5"]
    
    for name in names:
        target = random.choice(warehouses)
        runner = Runner(name, target)
        runners.append(runner)

    for r in runners:
        r.start()

    for r in runners:
        r.join()

    print(f"\n===== ПІДСУМКОВИЙ ЗВІТ =====")
    
    total_loot = 0
    print("\n[Заробіток бігунів]:")
    for r in runners:
        total_loot += r.earnings
        print(f"{r.name}: {r.earnings} грн")

    print("\n[Залишки на складах]:")
    for w in warehouses:
        print(f"{w.name}: {w.meds} од.")

    print(f"\nЗАГАЛЬНИЙ ВИЛОВ: {total_loot} грн")

if __name__ == "__main__":
    run_simulation()