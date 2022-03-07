import pandas as pd
pd.options.mode.chained_assignment = None
from itertools import combinations
from random import choice, choices, randint
from datetime import date, timedelta, datetime


class MyClass:
    
    def __init__(self, 
                 nor = 85000, # number of reservations to create, default is 85000
                 date1 = (date.today() + timedelta(days=-30)).strftime("%Y-%m-%d"), # start date for the period, default is 30 days ago
                 date2 = date.today().strftime("%Y-%m-%d"), # start date for the period, default is today
                 hub1 = 'aep', # the default hub1 is aep
                 hub2 = 'eze', # the default hub2 is eze
                 list_atos = ['brc', 
                              'cor', 
                              'cnq', 
                              'igr', 
                              'juj', 
                              'mdz', 
                              'nqn', 
                              'sla', 
                              'sde', 
                              'pss', 
                              'tuc', 
                              'rel', 
                              'ush', 
                              'fln', 
                              'gig', 
                              'sao', 
                              'asu', 
                              'pdp'
                             ],
                 freq_fl = True # if false, no frequent flyers are created
                ):
        
        self.nor = nor
        self.date1 = date1
        self.date2 = date2
        self.hub1 = hub1
        self.hub2 = hub2
        self.list_atos = list_atos
        self.freq_fl = freq_fl
        
    def df_generator(self):
        
        # Class variables
        nor = self.nor
        date1 = self.date1
        date2 = self.date2
        hub1 = self.hub1
        hub2 = self.hub2
        list_atos = self.list_atos
        freq_fl = self.freq_fl
        
        lista0 = [i for i in range(1, nor + 1, 1)] # Create a dummie list
        
        legs_df = pd.DataFrame(lista0) # Transform the dummie list in a pandas df

        date1 = datetime.strptime(date1, '%Y-%m-%d')
        date2 = datetime.strptime(date2, '%Y-%m-%d')
        
        """
        List of legs is created randomly, the 40% of the flights start in aep, the 20% of the flights start in eze.
        """  
        res = [(a, b) for idx, a in enumerate(list_atos) for b in list_atos[idx + 1:]]
        
        x1 = int(nor * 0.4) # aep portion
        x2 = int(nor * 0.2) # eze portion
        x3 = int(x1 + x2) # others atos portion
        x4 = int(nor - x3 - 1)
                
        list1 = [(hub1, choice(list_atos)) for i in range(x1)]
        list2 = [(hub2, choice(list_atos)) for i in range(x2)]
        list3 = [(choice(res)) for i in range(x4)]
        
        list0 = list1 + list2 + list3
        
        legs_df = pd.DataFrame(list0)
        
        legs_df['leg'] = legs_df[0] + '-' + legs_df[1]
        
        legs_df0 = legs_df.copy()
        
        """
        It is assumed that
        1. 60 percent of the people buy their ticket beetwen 90 and 180 days in advance.
        2. 10 percent of the people buy their ticket beetwen 60 and 90 days in advance.
        3. 10 percent of the people buy their ticket beetwen 30 and 60 days in advance.
        3. 10 percent of the people buy their ticket beetwen 15 and 30 days in advance.
        3. 10 percent of the people buy their ticket beetwen 0 and 15 days in advance.
        """

        # >>>> dates
        period_start_date = date1.date()
        period_end_date = date2.date()
        nr_of_rows = nor - 1 

        # initializing dates ranges 
        start_date, end_date = period_start_date, period_end_date
        # printing dates   
        res_dates = [start_date] 
        # while loop to get each date from start date till end date
        while start_date != end_date:
            start_date += timedelta(days=1)
            res_dates.append(start_date)
            
        # generate a list of random dates with choices method, k parameter set the len of the list
        res = choices(res_dates, k=nr_of_rows)

        # create a copy of legs dataframe to avoid warnings
        # legs_df_0 = legs_df.copy()
        # assign res list to fecha de reserva column
        legs_df0['fecha_de_reserva'] = res

        p10nor = nor * .1

        # create the intervals for the time beetwen purchase date and departure date
        legs_df0['fecha_partida'] = ''
        legs_df0['fecha_partida'][0:int(p10nor)] = legs_df0['fecha_de_reserva'][0:int(p10nor)] +  [timedelta(days=i) for i in [randint(1, 15) for i in range(1, int(p10nor+1), 1)]] 
        legs_df0['fecha_partida'][int(p10nor):int(2*p10nor)] = legs_df0['fecha_de_reserva'][int(p10nor):int(2*p10nor)] +  [timedelta(days=i) for i in [randint(15, 30) for i in range(1, int(p10nor+1), 1)]]
        legs_df0['fecha_partida'][int(2*p10nor):int(3*p10nor)] = legs_df0['fecha_de_reserva'][int(2*p10nor):int(3*p10nor)] +  [timedelta(days=i) for i in [randint(30, 60) for i in range(1, int(p10nor+1), 1)]]
        legs_df0['fecha_partida'][int(3*p10nor):int(4*p10nor)] = legs_df0['fecha_de_reserva'][int(3*p10nor):int(4*p10nor)] +  [timedelta(days=i) for i in [randint(60, 90) for i in range(1, int(p10nor+1), 1)]]
        legs_df0['fecha_partida'][int(4*p10nor):] = legs_df0['fecha_de_reserva'][int(4*p10nor):] +  [timedelta(days=i) for i in [randint(90, 180) for i in range(1, int(6*p10nor), 1)]]

        legs_df0['estado_reserva'] = ''
        legs_df0['fecha_ultima_modificacion'] = ''

        # initiate today as a variable
        today = date.today()
        # assume 3 days before today for the change of "estado reserva"
        today_3 = date.today() - timedelta(days=3)

        for _, row in legs_df0.iterrows():
            if row['fecha_partida'] < today_3:
                row['estado_reserva'] = 'x'
                row['fecha_ultima_modificacion'] = row['fecha_partida']
            elif (row['fecha_partida'] > today_3) and (row['fecha_partida'] < today_3):
                row['estado_reserva'] = 'y'
                row['fecha_ultima_modificacion'] = today_3
            else:
                row['estado_reserva'] = 'z'
                row['fecha_ultima_modificacion'] = row['fecha_de_reserva']

        
        
        if freq_fl == True:
            list_of_random_dnis = [randint(10000000, 40000000) for i in range(1, int(nor), 1)]

            x1 = int(nor * .01)
            x2 = int(nor * .09)

            list_ff00 = list_of_random_dnis[0:x1]
            list_ff01 = list_of_random_dnis[0:x2]

            random_list_ff00 = [choice(list_ff00) for i in range(1, int(nor*.1), 1)]
            random_list_ff01 = [choice(list_ff01) for i in range(1, int(nor*.15), 1)]

            norx = nor -(len(random_list_ff01) + len(random_list_ff00))

            list_of_random_dnis2 = [randint(10000000, 40000000) for i in range(1, int(norx), 1)]

            list_pax_res = random_list_ff00 + random_list_ff01 + list_of_random_dnis2
        
            legs_df0['dni'] = list_pax_res
        else:
            list_of_random_dnis = [randint(10000000, 40000000) for i in range(1, int(nor), 1)]
            legs_df0['dni'] = list_of_random_dnis
        
        # column for numero de reserva        
        df_00 = legs_df0.copy()
        df_00['nro'] = [i for i in range(1, len(df_00)+1, 1)]

        # initiate a list with name of the columns
        df_00.columns = ['ori',
                         'des',
                         'leg', 
                         'fec_emi',
                         'fec_vlo', 
                         'est_res', 
                         'fec_ult',
                         'dni',
                         'nro',
                        ]

        cols =['nro',
               'fec_emi',
               'ori',
               'des',
               'leg',
               'fec_vlo',
               'dni',
               'est_res',
               'fec_ult',
              ]

        df_01 = df_00[cols]
        return df_01
    
    def ages(self, df):
        

        list_ages = []
        
        for row in df.iterrows():
            # print(list(row))
            if (int(row[1][6]) <= 15000000):
                list_ages.append(randint(60, 65))
            elif (int(row[1][6]) > 15000000) and (int(row[1][6]) <= 20000000):
                list_ages.append(randint(50, 59))
            elif (int(row[1][6]) > 20000000) and (int(row[1][6]) <= 30000000):
                list_ages.append(randint(40, 49))
            elif (int(row[1][6]) > 30000000) and (int(row[1][6]) <= 35000000):
                list_ages.append(randint(30, 39))
            elif (int(row[1][6]) > 35000000) and (int(row[1][6]) <= 40000000):
                list_ages.append(randint(25, 29))
            else:
                list_ages.append(randint(18, 24))
        
        df['age'] = list_ages 