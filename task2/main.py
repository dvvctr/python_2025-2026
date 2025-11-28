meds = [
    ("Amoxicillin", 10, "antibiotic", 8.0),
    ("Vitamin C", 25, "vitamin", 4.5),
    ("FluVac", 5, "vaccine", 26.0),
    ("BadData", "10", "vitamin", "cold")  
]

for name, qty, category, temp in meds:
    
    if not isinstance(qty, int) or not isinstance(temp, (int, float)):
        print(f"{name} – Помилка даних")
        continue

    if temp < 5:
        temp_status = "Надто холодно"
    elif temp > 25:
        temp_status = "Надто жарко"
    else:
        temp_status = "Норма"

    match category:
        case "antibiotic":
            category_status = "Рецептурний препарат"
        case "vitamin":
            category_status = "Вільний продаж"
        case "vaccine":
            category_status = "Потребує спецзберігання"
        case _:
            category_status = "Невідома категорія"


    print(f"{name} – {category_status} – {temp_status}")