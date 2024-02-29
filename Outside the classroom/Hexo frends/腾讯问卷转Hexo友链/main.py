import pandas as pd
import numpy as np

df = pd.read_csv("data.csv", encoding="utf-8")
df_array = np.array(df)
df_list = df_array.tolist()
for i in df_list:
    data = "\n"
    data += "    - name: " + str(i[11]) + '\n'
    data += "      link: " + str(i[12]) + '\n'
    if str(i[13]) == "nan":
        data += "      avatar: " + '\n'
    else:
        data += "      avatar: " + str(i[13]) + '\n'
    if str(i[16]) == "nan":
        data += "      descr: " + '\n'
    else:
        data += "      descr: " + str(i[16]) + '\n'
    with open('link.yml', 'a+', encoding="utf-8") as csvfile:
        csvfile.write(data)
