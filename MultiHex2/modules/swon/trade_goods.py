from MultiHex2.modules.swon.enums import WorldCategory, TradeGood, get_entry_by_name
import json, os

# total supply mod scales base price like so when purchasing
purchase_scale = [ 
    300, 200, 175, 150,
    135, 125, 120, 115, 110,
    105, 100, 95, 90, 85, 80,
    75, 70, 65, 55, 50, 40, 25
]

for i in range(len(purchase_scale)):
    purchase_scale[i] = purchase_scale[i]/100.

# total demand mod effects sale price like so
sale_scale = [25,] + [45 + i*5 for i in range(16)]
sale_scale += [135,150,175,200,300,400]


for i in range(len(sale_scale)):
    sale_scale[i] = sale_scale[i]/100.

_data = open(os.path.join(os.path.dirname(__file__), "..", "..","resources","swon_trade_good_data.json"), 'rt')
tg_data = json.load(_data)
_data.close()

class TradeGoods:
    def __init__(
        self,
        name:str,
        json_entry:dict
    ):
        self.name = name

        self._price = float(json_entry["price"])

        self._common = False
        self._availble = []
        if len(json_entry["available"])==1:
            if json_entry["available"][0] == "all":
                self._common = True
        if not self._common:
            self._availble= [ get_entry_by_name(entry, WorldCategory) for entry in json_entry["available"] ]        
    
        self._demand_mod = { 
            get_entry_by_name(entry, WorldCategory):json_entry["demand"][entry] for entry in json_entry["demand"]
        }

        self._supply_mod = { 
            get_entry_by_name(entry, WorldCategory):json_entry["supply"][entry] for entry in json_entry["supply"]
        }


    def is_available(self, wc:WorldCategory)->bool:
        """
        Returns whether or not this Trade Good is usually available on a planet of a given World Category 
        """
        if self._common:
            return self._common
        else:
            return wc in self._availble

    def get_mod(self, wc:WorldCategory)->int:
        """
        The bigger the number, the more supply there is relative to the demand 
        """
        if wc in self._demand_mod:
            demand = self._demand_mod[wc]
        else:
            demand = 0

        if wc in self._supply_mod:
            supply = self._supply_mod[wc]
        else:
            supply = 0

        return supply - demand

    def get_purchase_price(self, wc:WorldCategory)->float:
        """
            Returns the expected price to purchase this good on a planet 

            Uses the "supply" and purchase
        """
        base = 10 + self.get_mod(wc)
        if base < 0:
            scale = 4.0
        elif base < 21:
            scale = purchase_scale[int(base)]
        else:
            scale = 0.25
        return self._price*scale


    def get_sale_price(self, wc:WorldCategory)->float:
        """
            Returns the expected amount to get by selling this good on a given planet 

            Uses the "demand" and sale
        """

        base = 10 - self.get_mod(wc)

        if base < 0:
            scale = 0.25
        elif base < 21:
            scale = sale_scale[int(base)]
        else:
            scale = 4.00
        
        return self._price*scale


ALL_GOODS = {
    get_entry_by_name(entry, TradeGood):TradeGoods(entry, tg_data[entry]) for entry in tg_data
}


