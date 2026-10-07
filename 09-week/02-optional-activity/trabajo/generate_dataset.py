"""Builds a SYNTHETIC, intentionally messy workshop dataset (seed fixed -> reproducible).
Not real vehicle data: it simulates what an OBD-II scanner + workshop log export looks like."""
import random, csv
random.seed(42)
vehicles = [("HUA-123","Chevrolet","Spark",2018,"gasoline"),("HUB-456","Renault","Logan",2016,"gasoline"),
 ("NEI-789","Mazda","CX-5",2020,"gasoline"),("TLM-321","Toyota","Hilux",2015,"diesel"),
 ("GAR-654","Kia","Picanto",2019,"gasoline"),("PIT-987","Nissan","Frontier",2017,"diesel"),
 ("ABC-111","Hyundai","Tucson",2021,"gasoline"),("XYZ-222","Ford","Ranger",2014,"diesel"),
 ("LMN-333","Suzuki","Swift",2013,"gasoline"),("QRS-444","Volkswagen","Gol",2012,"gasoline")]
dtcs = {"P0300":"Random misfire","P0299":"Turbo underboost","P0101":"MAF range/performance",
 "P0171":"System too lean","P0420":"Catalyst efficiency low","P0118":"Coolant sensor high","P0562":"System voltage low"}
symptoms = ["Pierde potencia al acelerar","Ralentí inestable","Luz MIL encendida","Consumo alto","Arranque difícil","Vibración en ralentí"]
techs = ["Carlos Ruiz","ana gomez","LUIS PEREZ","Marta Soto"]
rows=[]
for i in range(1,241):
    p,b,m,y,f = random.choice(vehicles); d = random.choice(list(dtcs))
    day = random.randint(1,28); mon = random.randint(1,9)
    date = random.choice([f"2026-{mon:02d}-{day:02d}", f"{day:02d}/{mon:02d}/2026", f"{day}-{mon}-2026"])
    rpm = random.gauss(850,60); temp = random.gauss(90,5); bat = random.gauss(12.6,0.4)
    mapk = random.gauss(42,6); km = random.randint(30000,220000); cost = random.choice([0,80000,150000,320000,450000,900000])
    r=[f"S{i:04d}",date,p,b,m,y,f,d,random.choice(symptoms),round(rpm),round(temp,1),round(bat,2),round(mapk,1),km,random.choice(techs),cost]
    rows.append(r)
cols=["session_id","date","plate","brand","model","year","fuel","dtc_code","symptom","rpm","coolant_temp_c","battery_v","map_kpa","mileage_km","technician","repair_cost_cop"]
# --- inject dirt ---
for r in random.sample(rows,25): r[9]=""                        # missing rpm
for r in random.sample(rows,20): r[10]=""                       # missing temp
for r in random.sample(rows,18): r[11]=""                       # missing battery
for r in random.sample(rows,15): r[12]=""                       # missing MAP
for r in random.sample(rows,10): r[8]=""                        # missing symptom
for r in random.sample(rows,12): r[13]=f"{r[13]:,} km"          # mileage as text "123,456 km"
for r in random.sample(rows,15): r[15]=f"${r[15]:,}"            # cost as text "$150,000"
for r in random.sample(rows,20): r[3]=random.choice([r[3].lower(), r[3].upper(), " "+r[3]+" "])
for r in random.sample(rows,15): r[2]=r[2].lower().replace("-"," ")   # plate format
for r in random.sample(rows,10): r[7]=r[7].lower()              # dtc lowercase
for r in random.sample(rows,6):  r[9]=random.choice([9999,-50])  # outliers rpm
for r in random.sample(rows,5):  r[10]=random.choice([250,-40]) # outliers temp
rows += [list(r) for r in random.sample(rows,12)]               # exact duplicates
random.shuffle(rows)
with open("data/diagnostics_raw.csv","w",newline="",encoding="utf-8") as fh:
    w=csv.writer(fh); w.writerow(cols); w.writerows(rows)
print(len(rows),"rows written")
