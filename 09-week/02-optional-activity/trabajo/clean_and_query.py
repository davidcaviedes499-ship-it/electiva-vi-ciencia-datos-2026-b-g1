"""Week 9 - Cleaning + queries for the vehicle diagnostics dataset (pandas)."""
import pandas as pd, numpy as np, re
RAW="data/diagnostics_raw.csv"
df=pd.read_csv(RAW, dtype=str)
before={"rows":len(df),"nulls":df.replace("",np.nan).isna().sum().sum(),"duplicates":df.duplicated().sum()}
null_before=df.replace("",np.nan).isna().sum()
types_before=pd.read_csv(RAW).dtypes.astype(str)

# 1. duplicates
df=df.drop_duplicates().copy()
# 2. text normalization
for c in ["brand","model","technician","fuel","symptom"]: df[c]=df[c].str.strip()
df["brand"]=df["brand"].str.title()
df["technician"]=df["technician"].str.title()
df["plate"]=df["plate"].str.upper().str.replace(r"[\s_]+","-",regex=True)
df["dtc_code"]=df["dtc_code"].str.upper().str.strip()
# 3. types
iso=df["date"].str.match(r"^\d{4}-\d{1,2}-\d{1,2}$")      # ISO yyyy-mm-dd: parse as-is
df["date"]=pd.to_datetime(df["date"].where(iso),format="%Y-%m-%d",errors="coerce").fillna(
    pd.to_datetime(df["date"].where(~iso),format="%d/%m/%Y",errors="coerce")).fillna(
    pd.to_datetime(df["date"].where(~iso),format="%d-%m-%Y",errors="coerce"))
df["mileage_km"]=pd.to_numeric(df["mileage_km"].str.replace(r"[^\d.]","",regex=True))
df["repair_cost_cop"]=pd.to_numeric(df["repair_cost_cop"].str.replace(r"[^\d.]","",regex=True))
for c in ["rpm","coolant_temp_c","battery_v","map_kpa"]: df[c]=pd.to_numeric(df[c].replace("",np.nan))
df["year"]=df["year"].astype(int)
# 4. outliers -> null (physically impossible values), then impute
valid={"rpm":(400,7000),"coolant_temp_c":(-20,130)}
out_count={}
for c,(lo,hi) in valid.items():
    m=~df[c].between(lo,hi)&df[c].notna(); out_count[c]=int(m.sum()); df.loc[m,c]=np.nan
# 5. nulls: numeric -> median by fuel type; symptom -> "Unknown"
for c in ["rpm","coolant_temp_c","battery_v","map_kpa"]:
    df[c]=df[c].fillna(df.groupby("fuel")[c].transform("median")).round(2)
df["symptom"]=df["symptom"].replace("",np.nan).fillna("Unknown")
df=df.reset_index(drop=True)
df.to_csv("data/diagnostics_clean.csv",index=False)

after={"rows":len(df),"nulls":int(df.isna().sum().sum()),"duplicates":int(df.duplicated().sum())}
report=pd.DataFrame({"nulls_before":null_before,"nulls_after":df.isna().sum(),
                     "dtype_before":types_before,"dtype_after":df.dtypes.astype(str)})
print("=== BEFORE / AFTER ===");print(before);print(after);print("outliers set to null:",out_count);print(report)
with open("data/cleaning_report.md","w") as f:
    f.write(f"| Metric | Before | After |\n|---|---|---|\n| Rows | {before['rows']} | {after['rows']} |\n| Null cells | {before['nulls']} | {after['nulls']} |\n| Duplicate rows | {before['duplicates']} | {after['duplicates']} |\n\n")
    f.write(report.to_markdown()+"\n\nOutliers converted to null before imputation: "+str(out_count)+"\n")

# ---------- Questions ----------
q1=(df.groupby("dtc_code").agg(sessions=("session_id","count"),avg_cost_cop=("repair_cost_cop","mean"))
      .sort_values("sessions",ascending=False).round(0))
print("\n=== Q1: sessions & avg repair cost per DTC ===");print(q1)
low=df[df["battery_v"]<12.4]                                  # filter
q2=low.groupby("dtc_code").size().rename("low_battery_sessions").to_frame()
q2["share_of_all_low"]=(q2["low_battery_sessions"]/len(low)*100).round(1)
q2=q2.sort_values("low_battery_sessions",ascending=False)
base=(df.groupby("dtc_code").size()/len(df)*100).round(1).rename("share_of_all_sessions")
q2=q2.join(base)
print("\n=== Q2: DTCs among low-battery (<12.4 V) sessions ===");print(f"low-battery sessions: {len(low)} of {len(df)}");print(q2)
q1.to_csv("data/q1_result.csv");q2.to_csv("data/q2_result.csv")
