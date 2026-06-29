import pandas as pd
from pyscipopt import Model
from pyscipopt import quicksum
#you can make you own if it returns a dataframe with the expected column names
#expected columns: name(str), price(float), min(int), max(int) 
def file_reader(filepath:str):
    df = pd.read_csv(filepath)
    return df

class GroceryList:
    def __init__(self, budget, df=None):
        self.df = df
        self.budget = budget
        self.model = None
        self.vars = None#could use a numpy arrays 
        self.cons = None

    #adding from code without dataframe
    def add_item(self, data:list, colname:list):
        df1 = pd.DataFrame(data, columns=colname)
        self.df = pd.concat([self.df, df1], ignore_index=True, join='inner')
        
    def create_model(self):
        if self.df is None:
            return None
        self.model = Model("GrocerySolver")
        
        #variable creation
        n = self.df.shape[0]
        self.vars = [None for i in range(n)]

        for i in range(n):
            var_name = self.df['name'].loc[i]
            self.vars[i] = self.model.addVar(vtype='I', name=var_name)

        #objective function
        price = self.df['price']
        objective_expr = quicksum(price.loc[i]*self.vars[i] for i in range(n))
        self.model.setObjective(objective_expr)

        #constraints creation
        #assumption: you should leave min/max empty in the csv file 
        #when you don't want to set any value so pandas sets it as NaN
        self.cons = []
        for i in range(n):
            min_qty, max_qty = 0, 0
            #check empty field min/max fields
            if not pd.isna(self.df['min'].loc[i]):
                if self.df['min'].loc[i] > min_qty:
                    min_qty = self.df['min'].loc[i]
            var_name = self.df['name'].loc[i]
            self.cons.append(self.model.addCons(self.vars[i] >= min_qty, name=f"{var_name}_min"))

            if not pd.isna(self.df['max'].loc[i]):
                #
                if self.df['max'].loc[i] >= min_qty:  
                    max_qty = self.df['max'].loc[i]
                    self.cons.append(self.model.addCons(self.vars[i] <= max_qty, name=f"{var_name}_max"))
        #budget constraint
        self.cons.append(self.model.addCons(quicksum(price.loc[i]*self.vars[i] for i in range(n)) <= self.budget, name="budget_cons"))
    
    def get_price(self):
        if self.vars is None or self.cons is None:
            return None
        total_price = 0
        self.model.optimize()
        sol = self.model.getBestSol()
        n = self.df.shape[0]
        for i in range(n):
            total_price += self.df['price'].loc[i]
            print(f"{self.df['name'].loc[i]}: {sol[self.vars[i]]} (+{sol[self.vars[i]]*self.df['price'].loc[i]}€)")
        print(f"total: {total_price}€")

#testing 
if __name__ == "__main__":
    #Grocery list example (the units are specified for coherence):
    #tomato, 3.49€/kg, 1(kg), 2(kg)
    #pasta, 0.50€/pack of 500g, 2(pack of 500g), 4(pack of 500g)
    #cheese, 2.19€/bag of 100g, 1(bag of 100g), 1(bag of 100g)
    #budget: 50€
    
    df = pd.DataFrame([['tomato(kg)', 3.49, 1, 2],
                       ['pasta(500g pack)', 0.5, 2, 4],
                       ['cheese(100g bag)', 2.19, 1, 1]],
                       columns=['name', 'price', 'min', 'max'])
    df2 = file_reader("~/Documents/test.csv")
    groceries = GroceryList(50, df)
    groceries.create_model()
    groceries.get_price()



