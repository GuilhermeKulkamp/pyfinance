import ofxparse
import pandas as pd
import os
from datetime import datetime

df = pd.DataFrame()

for extrato in os.listdir("extratos"):
    with open(f"extratos/'{extrato}'", encoding='USASCII') as ofx_file:
        ofx = ofxparse.OfxParser.parse(ofx_file)
