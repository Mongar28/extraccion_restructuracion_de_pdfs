import pandas as pd
import re

df = pd.read_csv('actas_concejo.csv')

actas_unicas = []
acta = []
texto_corto = ''


pattern_acta: str = r'[\s\S]{1,3}(ACTA\s\d{3})[\s\S]{1,3}'
for i, texto in enumerate(df['texto']):
    try:
        if len(texto) > 500:
            
            texto_corto = re.sub(r'\s{2,10}',' ', texto[:100])
            if re.search(pattern_acta, texto_corto).group(1) not in acta:
                actas_unicas.append(texto)
            acta.append(re.search(pattern_acta, texto_corto).group(1))
            print(i)
    except:
        print(f'error en el archvio {i}')
        
print(len(actas_unicas))

print('____________________________________________________________________________')
print(actas_unicas[0][:50])

df_actas_unicas = pd.DataFrame()
df_actas_unicas['texto'] = actas_unicas

print(df_actas_unicas['texto'][0][:100])

df_actas_unicas.to_csv('actas_procesadas.csv')

