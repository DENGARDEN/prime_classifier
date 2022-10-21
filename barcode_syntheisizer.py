import pandas as pd

df = pd.read_csv("./Barcode.csv", sep='\t')

barcode_storage = []
for index, row in df.iterrows():
    unedited = row[1] + row[2]
    edited = row[1] + row[3]
    others = row[1]

    barcode_name = row[0]

    # barcode_storage.extend([(f"{barcode_name}_UNEDITED", unedited),
    #                         (f"{barcode_name}_EDITED", edited),
    #                         (f"{barcode_name}_OTHERS", others)])

    barcode_storage.append((f"{barcode_name}_BARCODE_ONLY", others))

pd.DataFrame(barcode_storage).to_csv("PE_LIB_BARCODE_ONLY.txt", index=False, sep=':', header=False)
