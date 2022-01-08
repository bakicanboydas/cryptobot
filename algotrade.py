from binance.client import Client
import talib as ta
import numpy as np
import time
import tradeTelegram
import PySimpleGUI as sg

class BinanceConnection:
    def __init__(self, file):
        self.connect(file)

    """ Creates Binance client """
    def connect(self, file):
        lines = [line.rstrip('\n') for line in open(file)]
        key = lines[0]
        secret = lines[1]
        self.client = Client(key, secret)

if __name__ == '__main__':
    filename = 'credentials.txt'
    connection = BinanceConnection(filename)
    
    layout = [[sg.Text("Lutfen para birimini giriniz... Ornek : BTTUSDT veya XRPBTC gibi.")],
    [sg.Input(key = '-BIRIM-')],
    [sg.Text("Zaman dilimini seçiniz")],
    [sg.Combo(['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w'])],
    [sg.Text("Kac adet alis-satis yapilacak yaziniz.")],
    [sg.Input(key = '-ADET-')],
    [sg.Button('Ok')]]
    
    window = sg.Window('Binance Bot Sener', layout)
    
    event, values = window.read()
    
    symbol = values['-BIRIM-']
    interval = values[0]
    limit = 500
    denetleyici = True
    sayisi = values['-ADET-']
    
    print('Bu birimden', symbol, 'bu sure icin' ,interval, 'bu kadar' ,sayisi, 'alis-satis yapiliyor.')
    window.close()
    
    alis_fiyat = 0
    satis_fiyat = 0
    kar_zarar_orani = 0
    toplam_kar_zarar = 0
    while True:
        

        try:
            klines = connection.client.get_klines(symbol=symbol, interval=interval, limit=limit)
        except Exception as exp:
            print(exp.status_code, flush=True)
            print(exp.message, flush=True)

        open = [float(entry[1]) for entry in klines]
        high = [float(entry[2]) for entry in klines]
        low = [float(entry[3]) for entry in klines]
        close = [float(entry[4]) for entry in klines]

        last_closing_price = close[-1]

        previous_closing_price = close[-2]
        print('*******************************************************************')
        print('Bu birimden', symbol, 'bu sure icin' ,interval, 'bu kadar' ,sayisi, 'alis-satis yapiliyor.')
        print('Anlik Kapanıs Fiyati', last_closing_price, ', Bir Onceki Kapanis Fiyati', previous_closing_price)

        close_array = np.asarray(close)
        close_finished = close_array[:-1]
        
        fastperiod=12
        slowperiod=26 
        signalperiod=9
            

        MMEslowa = ta.EMA(close_finished,slowperiod)
        MMEslowb = ta.EMA(MMEslowa,slowperiod)
        DEMAslow = ((2 * MMEslowa) - MMEslowb)
 
        MMEfasta = ta.EMA(close_finished,fastperiod)
        MMEfastb = ta.EMA(MMEfasta,fastperiod)
        DEMAfast = ((2 * MMEfasta) - MMEfastb)
         
        LigneMACDZeroLag = DEMAfast - DEMAslow #blue
        
        
        MMEsignala = ta.EMA(LigneMACDZeroLag,signalperiod)
        MMEsignalb = ta.EMA(MMEsignala,signalperiod)
        Lignesignal = ((2 * MMEsignala) - MMEsignalb) #red
       
        
        MACDZeroLag = LigneMACDZeroLag - Lignesignal
        
        if len(LigneMACDZeroLag) > 0:
            
            last_macd = LigneMACDZeroLag[-1]
            last_macd = round(last_macd,7)
            last_macd_signal = Lignesignal[-1]
            last_macd_signal = round(last_macd_signal,7)
            print(last_macd,last_macd_signal)
            
            previous_macd = LigneMACDZeroLag[-2]
            previous_macd = round(previous_macd,7)
            previous_macd_signal = Lignesignal[-2]
            previous_macd_signal = round(previous_macd_signal,7)
            print(previous_macd,previous_macd_signal)
            
            macd_cross_up = last_macd > last_macd_signal and previous_macd < previous_macd_signal
            macd_cross_down = last_macd < last_macd_signal and previous_macd > previous_macd_signal
            print(macd_cross_up)
            print(macd_cross_down)
            
            if macd_cross_up and denetleyici == True:
                print('Al Sinyali')
                #order = connection.client.order_market_buy(symbol=symbol,quantity=sayisi)
                alis_fiyat = last_closing_price
                tradeTelegram.alis_satis(last_closing_price,sayisi,'alis yapildi ',kar_zarar_orani,' ',toplam_kar_zarar,denetleyici,symbol)                
                denetleyici = False
            
            if macd_cross_down and denetleyici == False:
                print('Sat Sinyali')
                #order = connection.client.order_market_sell(symbol=symbol,quantity=sayisi)
                satis_fiyat = last_closing_price
                kar_zarar_orani = satis_fiyat - alis_fiyat
                toplam_kar_zarar = toplam_kar_zarar + kar_zarar_orani
                if kar_zarar_orani < 0:
                    tradeTelegram.alis_satis(last_closing_price,sayisi,'satis yapildi ',kar_zarar_orani,' zarar edildi.',toplam_kar_zarar,denetleyici,symbol)
                if kar_zarar_orani > 0:
                    tradeTelegram.alis_satis(last_closing_price,sayisi,'satis yapildi ',kar_zarar_orani,' kar edildi.',toplam_kar_zarar,denetleyici,symbol)
                denetleyici = True         
        time.sleep(5)