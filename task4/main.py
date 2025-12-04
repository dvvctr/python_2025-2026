def shadow(limit=200):
    def decorator(func):
        def wrapper(*args, **kwargs):
            total = 0
            
            gen = func(*args, **kwargs)
            
            for item in gen:
                try:
                    amount = int(item.split()[1])
                    total += amount
                    
                    if total > limit:
                        print("Тіньовий ліміт перевищено. Активую схему.")
                except:
                    pass
                
                yield item
            
            return total
        return wrapper
    return decorator

@shadow(limit=200)
def get_transactions():
    transactions = [
        "payment 120",
        "wrong_data",
        "refund 50",
        "transfer 300",
        "tax 15"
    ]
    for t in transactions:
        yield t

stream = get_transactions()
    
for t in stream:
    print(f"Оброблено: {t}")