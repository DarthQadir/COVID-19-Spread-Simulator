import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
from scipy.stats import poisson, norm, uniform
import csv
import numpy as np



#Function to add cities as nodes
def add_city(graph,name,area,population,cases,neighbours):


  #neighbours is a list of tuples. Each tuple contains the name of the city,
  #the area, the population, its neighbours and the strength between each of its
  #neighbours (weight). See the second cell for the format of the data

  #subtract the cases from the population to get the uninfected population
  population -= cases
  population_density = population/area

  #Add node to graph
  graph.add_node(name,population=population,
                 population_density=population_density,
                 cases=cases)
  
  #Add edges between the neighbours
  graph.add_weighted_edges_from(neighbours)

#Function that simulates a day
def simulate_day(graph,lambda_,recovery):

  #Sample 1 million numbers first instead of sampling each time the for loop
  #runs because it is much faster
  poisson_samples = poisson.rvs(lambda_,size=1000000)
  uniform_samples = uniform.rvs(size=1000000)
  #Loop through nodes
  for node in graph.nodes:

    #Loop through each case and sample from a poisson distribution to see how
    #many people the case infected

    for people in range(graph.nodes[node]['cases']):
      spread = np.random.choice(poisson_samples)
      graph.nodes[node]['cases'] += spread
      graph.nodes[node]['population'] -= spread


    #Multiplier effect due to density of city
    spread = int(round(graph.nodes[node]['population_density'] * abs(norm.rvs(0,0.0001) * graph.nodes[node]['cases'])))
    graph.nodes[node]['cases'] += spread
    graph.nodes[node]['population'] -= spread  

    #Small chance of recovery in people
    recovered = 0
    recovery_rate = round(abs(norm.rvs(recovery,0.05)))
    for people in range(graph.nodes[node]['cases']):
      if np.random.choice(uniform_samples) < recovery_rate:
        recovered +=1
    graph.nodes[node]['cases'] -= recovered
    graph.nodes[node]['population'] += recovered


    #Loop through each edge of each node to simulate flow of people
    for edges in graph.adj[node]:
      #get the weight
      weight =  list(graph[node][edges]['weight'].values())[0]

      #get expected flow of traffic from the city
      expected_flow = round((weight + abs(norm.rvs(0,0.01))) *  (graph.nodes[node]['cases']+graph.nodes[node]['population']))

      #check how many infected people travel
      samples = uniform.rvs(size=int(expected_flow))
      corona_flow = 0
      for i in samples:
        if i < graph.nodes[node]['cases']/graph.nodes[node]['population']:
          corona_flow += 1
      graph.nodes[node]['cases'] -= corona_flow
      graph.nodes[edges]['cases'] += corona_flow




def make_sindh():
#Make sindh graph
  sindh = nx.Graph()

  #Add cities/districts

  #data was taken from https://en.wikipedia.org/wiki/Districts_of_Sindh,_Pakistan

  add_city(sindh, 'Badin',6470,1804516,0, [("Badin",'Thatta',{'weight':abs(norm.rvs(0.001,0.0005))}),("Badin",'Tando Muhammad Khan',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                            ("Badin",'Hyderabad',{'weight':abs(norm.rvs(0.001,0.0005))}), ("Badin",'Tando Allahyar',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                            ("Badin",'Mirpur Khas',{'weight':abs(norm.rvs(0.001,0.0005))}), ("Badin",'Tharparker',{'weight':abs(norm.rvs(0.001,0.0005))})] )
  add_city(sindh, 'Dadu',8034,1550266,0, [("Dadu",'Qambar Shahdadkot',{'weight':abs(norm.rvs(0.001,0.0005))}),("Dadu",'Larkana',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                          ("Dadu",'Larkana',{'weight':abs(norm.rvs(0.001,0.0005))}),("Dadu",'Naushahro Firoz',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                          ("Dadu",'Jamshoro',{'weight':abs(norm.rvs(0.001,0.0005))})])
  add_city(sindh, 'Ghotki',6506,1647239,8, [("Ghotki",'Kashmore',{'weight':abs(norm.rvs(0.001,0.0005))}), ("Ghotki",'Sukkur',{'weight':abs(norm.rvs(0.001,0.0005))})] )
  add_city(sindh, 'Hyderabad',1022,2201079,3, [("Hyderabad",'Jamshoro',{'weight':abs(norm.rvs(0.0025,0.0005))}), ("Hyderabad",'Matiari',{'weight':abs(norm.rvs(0.0025,0.0005))}),
                                                ("Hyderabad",'Sanghar',{'weight':abs(norm.rvs(0.0025,0.0005))}), ("Hyderabad",'Tando Allahyar',{'weight':abs(norm.rvs(0.0025,0.0005))}),
                                                ("Hyderabad",'Badin',{'weight':abs(norm.rvs(0.0025,0.0005))}),("Hyderabad",'Tando Muhammad Khan',{'weight':abs(norm.rvs(0.0025,0.0005))}),
                                                ("Hyderabad",'Thatta',{'weight':abs(norm.rvs(0.0025,0.0005))})] )
  add_city(sindh, 'Jacobabad',2771,1006297,3, [("Jacobabad",'Kashmore',{'weight':abs(norm.rvs(0.001,0.0005))}),("Jacobabad",'Shikarpur',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                                ("Jacobabad",'Larkana',{'weight':abs(norm.rvs(0.001,0.0005))}),("Jacobabad",'Qambar Shahdadkot',{'weight':abs(norm.rvs(0.001,0.0005))})] )
  add_city(sindh, 'Jamshoro',11250,993142,12, [ ("Jamshoro",'Dadu',{'weight':abs(norm.rvs(0.001,0.0005))}),  ("Jamshoro",'Naushahro Firoz',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                                ("Jamshoro",'Nawabshah',{'weight':abs(norm.rvs(0.001,0.0005))}), ("Jamshoro",'Matiari',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                                ("Jamshoro",'Hyderabad',{'weight':abs(norm.rvs(0.001,0.0005))}), ("Jamshoro",'Thatta',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                                ("Jamshoro",'Karachi',{'weight':abs(norm.rvs(0.001,0.0005))})] )
  add_city(sindh, 'Karachi',3672,17144157,10, [ ("Karachi",'Jamshoro',{'weight':abs(norm.rvs(0.003,0.001))}),  ("Karachi",'Thatta',{'weight':abs(norm.rvs(0.003,0.001))})] )
  add_city(sindh, 'Kashmore',2551,1089169,8, [ ("Kashmore",'Ghotki',{'weight':abs(norm.rvs(0.0007,0.0003))}),("Kashmore",'Sukkur',{'weight':abs(norm.rvs(0.0007,0.0003))}),
                                              ("Kashmore",'Shikarpur',{'weight':abs(norm.rvs(0.0007,0.0003))}),("Kashmore",'Jacobabad',{'weight':abs(norm.rvs(0.0007,0.0003))})] )
  add_city(sindh, 'Khairpur',15925,2405523,13, [("Khairpur",'Larkana',{'weight':abs(norm.rvs(0.001,0.0005))}),("Khairpur",'Sukkur',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                                ("Khairpur",'Shikarpur',{'weight':abs(norm.rvs(0.001,0.0005))}), ("Khairpur",'Nawabshah',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                                ("Khairpur",'Sanghar',{'weight':abs(norm.rvs(0.001,0.0005))}), ("Khairpur",'Naushahro Firoz',{'weight':abs(norm.rvs(0.001,0.0005))})] )
  add_city(sindh, 'Larkana',1906,1524391,0, [("Larkana",'Shikarpur',{'weight':abs(norm.rvs(0.001,0.0005))}),("Larkana",'Jacobabad',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                              ("Larkana",'Qambar Shahdadkot',{'weight':abs(norm.rvs(0.001,0.0005))}),("Larkana",'Dadu',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                              ("Larkana",'Naushahro Firoz',{'weight':abs(norm.rvs(0.001,0.0005))}),("Larkana",'Khairpur',{'weight':abs(norm.rvs(0.001,0.0005))})] )
  add_city(sindh, 'Matiari',1459,769349,0, [("Matiari",'Nawabshah',{'weight':abs(norm.rvs(0.001,0.0005))}),("Matiari",'Sanghar',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                            ("Matiari",'Hyderabad',{'weight':abs(norm.rvs(0.001,0.0005))}), ("Matiari",'Jamshoro',{'weight':abs(norm.rvs(0.001,0.0005))})] )
  add_city(sindh, 'Mirpur Khas',3319,1505876,0, [("Mirpur Khas",'Sanghar',{'weight':abs(norm.rvs(0.001,0.0005))}), ("Mirpur Khas",'Umerkot',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                                  ("Mirpur Khas",'Tharparker',{'weight':abs(norm.rvs(0.001,0.0005))}), ("Mirpur Khas",'Tando Allahyar',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                                  ("Mirpur Khas",'Badin',{'weight':abs(norm.rvs(0.001,0.0005))})] )
  add_city(sindh, 'Naushahro Firoz',2027,1612373,6, [("Naushahro Firoz",'Dadu',{'weight':abs(norm.rvs(0.001,0.0005))}),("Naushahro Firoz",'Larkana',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                                      ("Naushahro Firoz",'Khairpur',{'weight':abs(norm.rvs(0.001,0.0005))}),("Naushahro Firoz",'Nawabshah',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                                      ("Naushahro Firoz",'Jamshoro',{'weight':abs(norm.rvs(0.001,0.0005))})])
  add_city(sindh, 'Nawabshah',4618,2012847,8, [("Nawabshah",'Khairpur',{'weight':abs(norm.rvs(0.001,0.0005))}),("Nawabshah",'Sanghar',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                                ("Nawabshah",'Naushahro Firoz',{'weight':abs(norm.rvs(0.001,0.0005))}),("Nawabshah",'Matiari',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                                ("Nawabshah",'Jamshoro',{'weight':abs(norm.rvs(0.001,0.0005))})] )
  add_city(sindh, 'Qambar Shahdadkot',5599,1341042,3, [("Qambar Shahdadkot",'Larkana',{'weight':abs(norm.rvs(0.0007,0.0003))}),("Qambar Shahdadkot",'Dadu',{'weight':abs(norm.rvs(0.0007,0.0003))}),
                                                        ("Qambar Shahdadkot",'Jacobabad',{'weight':abs(norm.rvs(0.0007,0.0003))})] )
  add_city(sindh, 'Sanghar',10259,2057057	,5, [("Sanghar",'Khairpur',{'weight':abs(norm.rvs(0.001,0.0005))}),("Sanghar",'Matiari',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                                ("Sanghar",'Nawabshah',{'weight':abs(norm.rvs(0.001,0.0005))}),("Sanghar",'Hyderabad',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                                ("Sanghar",'Mirpur Khas',{'weight':abs(norm.rvs(0.001,0.0005))}),("Sanghar",'Tando Muhammad Khan',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                                ("Sanghar",'Umerkot',{'weight':abs(norm.rvs(0.001,0.0005))})] )
  add_city(sindh, 'Shikarpur',2577,1231481,8, [("Shikarpur",'Jacobabad',{'weight':abs(norm.rvs(0.001,0.0005))}),("Shikarpur",'Kashmore',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                                ("Shikarpur",'Ghotki',{'weight':abs(norm.rvs(0.001,0.0005))}),("Shikarpur",'Larkana',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                                ("Shikarpur",'Sukkur',{'weight':abs(norm.rvs(0.001,0.0005))}),("Shikarpur",'Khairpur',{'weight':abs(norm.rvs(0.001,0.0005))})] )
  add_city(sindh, 'Sukkur',5216,1487903,160, [("Sukkur",'Ghotki',{'weight':abs(norm.rvs(0.0025,0.0005))}),("Sukkur",'Kashmore',{'weight':abs(norm.rvs(0.0025,0.0005))}),
                                            ("Sukkur",'Shikarpur',{'weight':abs(norm.rvs(0.0025,0.0005))}),("Sukkur",'Khairpur',{'weight':abs(norm.rvs(0.0025,0.0005))})] )
  add_city(sindh, 'Tando Allahyar',1573,836887,3, [("Tando Allahyar",'Sanghar',{'weight':abs(norm.rvs(0.001,0.0005))}),("Tando Allahyar",'Mirpur Khas',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                                    ("Tando Allahyar",'Badin',{'weight':abs(norm.rvs(0.001,0.0005))}),("Tando Allahyar",'Hyderabad',{'weight':abs(norm.rvs(0.001,0.0005))})] )
  add_city(sindh, 'Tando Muhammad Khan',1814,677228,0, [("Tando Muhammad Khan",'Hyderabad',{'weight':abs(norm.rvs(0.001,0.0005))}),("Tando Muhammad Khan",'Thatta',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                                          ("Tando Muhammad Khan",'Badin',{'weight':abs(norm.rvs(0.001,0.0005))})] )
  add_city(sindh, 'Tharparker',19808,1649661,0, [("Tharparker",'Umerkot',{'weight':abs(norm.rvs(0.0007,0.0003))}),("Tharparker",'Badin',{'weight':abs(norm.rvs(0.0007,0.0003))}),
                                                  ("Tharparker",'Mirpur Khas',{'weight':abs(norm.rvs(0.0007,0.0003))})] )
  add_city(sindh, 'Thatta',16404,1761784,2, [("Thatta",'Hyderabad',{'weight':abs(norm.rvs(0.001,0.0005))}),("Thatta",'Jamshoro',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                              ("Thatta",'Karachi',{'weight':abs(norm.rvs(0.001,0.0005))}),("Thatta",'Tando Muhammad Khan',{'weight':abs(norm.rvs(0.001,0.0005))}),
                                              ("Thatta",'Badin',{'weight':abs(norm.rvs(0.001,0.0005))})] )
  add_city(sindh, 'Umerkot',5503,1073146,2, [("Umerkot",'Sanghar',{'weight':abs(norm.rvs(0.0007,0.0003))}),("Umerkot",'Mirpur Khas',{'weight':abs(norm.rvs(0.0007,0.0003))}),
                                              ("Umerkot",'Tharparker',{'weight':abs(norm.rvs(0.0007,0.0003))})] )
  
  return sindh




#List to store results to calculate a confidence interval. 
district_cases = np.array([[[None for k in range(100)] for x in range(23)] for j in range(14)])


#Run the simulation for an X number of days. X is determined by how many times
#you run the loop
for i in range(100):
  print('run ', i)
  sindh = make_sindh()
  for day in range(1,15):
    simulate_day(sindh,0.5,0.3)
    print('day ', day)
    for k, district in zip(range(23), sindh.nodes):
      district_cases[day-1][k][i] = sindh.nodes[district]['cases']



#Save the results in a csv file

with open('corona_sindh.csv','w',newline='') as file:
  writer = csv.writer(file)
  writer.writerow(['Day','District','Total Population', 'Lower End of 95% CI of Predicted Cases', 'Upper End of 95% CI of Predicted Cases'])
  for day in range(1,15):
    for k,district in zip(range(23), sindh.nodes):
      low_end = np.percentile(district_cases[day-1][k],2.5)
      high_end = np.percentile(district_cases[day-1][k],97.5)
      writer.writerow([day,district,sindh.nodes[district]['population'],low_end,high_end])
    
