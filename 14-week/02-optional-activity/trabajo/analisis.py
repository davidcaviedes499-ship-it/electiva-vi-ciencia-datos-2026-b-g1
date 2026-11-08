from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
OUT = BASE / 'graficos'
OUT.mkdir(exist_ok=True)

df = pd.read_csv(BASE / 'produccion.csv', parse_dates=['fecha']).sort_values('fecha').set_index('fecha')
if df.index.has_duplicates or df['produccion_mpcd'].isna().any():
    raise ValueError('Fechas duplicadas o valores faltantes')

mensual = df['produccion_mpcd'].resample('MS').agg(['mean', 'sum'])
mensual.columns = ['promedio_diario_mpcd', 'suma_registros_diarios']
mensual.to_csv(BASE / 'resumen_mensual.csv', float_format='%.2f')
df['media_movil_7d'] = df['produccion_mpcd'].rolling(window=7, min_periods=7).mean()

fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(df.index, df['produccion_mpcd'], label='Producción diaria', alpha=0.4, linewidth=0.9)
ax.plot(df.index, df['media_movil_7d'], label='Media móvil de 7 días', linewidth=2)
ax.set(title='La producción simulada aumenta a lo largo de 2025', xlabel='Fecha', ylabel='Producción (miles de pies cúbicos/día)')
ax.set_ylim(bottom=0)
ax.legend()
ax.grid(alpha=0.2)
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig(OUT / 'evolucion.png', dpi=160)
plt.close(fig)

fig, ax = plt.subplots(figsize=(11, 5))
ax.bar(mensual.index.strftime('%b'), mensual['promedio_diario_mpcd'])
ax.set(title='El promedio diario simulado es mayor al final del año', xlabel='Mes de 2025', ylabel='Producción promedio diaria (miles de pies cúbicos/día)')
ax.set_ylim(bottom=0)
ax.grid(axis='y', alpha=0.2)
fig.tight_layout()
fig.savefig(OUT / 'comparacion.png', dpi=160)
plt.close(fig)

print('Promedio enero:', round(mensual.iloc[0, 0], 2))
print('Promedio diciembre:', round(mensual.iloc[-1, 0], 2))
print('Mes máximo:', mensual['promedio_diario_mpcd'].idxmax().strftime('%B'))
print('Mes mínimo:', mensual['promedio_diario_mpcd'].idxmin().strftime('%B'))
