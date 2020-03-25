# Important note

The CSV file has the results from 100 monte carlo simulations While the results printed at the bottom of the notebook are from a single run.

# COVID-19-Spread-Simulation
This simulation can be used to model the spread of the corona virus through any adjacent number of cities/districts/towns etc.

I have yet to make it objected oriented and I understand it's easier, but it's more important for me to create a working simulation right now.

# Goal:
If we leave the virus unchecked, which places will it hit the hardest?

# Assumptions for the example below, and in general:
- It just for Sindh's districts, no neighbouring cities on the border of sindh are involved.
- Quarantine changes the flow of traffic between districts/cities which is normally distributed (in order to remove quarantine, you can vary the parameters of the normal distribution). Quarantine also changes the parameters of the poisson distribution to reduce in-city spread of COVID-19. 
- Poisson distribution used for rate of spread.
- Weight of inflow and outflow traffic between cities is the same.
- Population remains constant (have not modeled death of people due to corona because I don't expect there to be so many deaths to have   an impact on the simulation)
- Density = population / area
- Density affects the rate of spread inside a city.
- The cases are unconfirmed+confirmed cases. There is no containment involved since the goal is to predict which places will be hit the   hardest.



# In a nutshell explanation (for Sindh)

*I used this map as a reference for Sindh https://en.wikipedia.org/wiki/Districts_of_Sindh,_Pakistan*

- Use networkx library in Python to make a graph.
- Make nodes that represent each district of Sindh, and add them to the graph.
- Add the population, area (area is used to calculate population density), and number of cases for each district.
- Loop through each district, then each case in each district, sample from a poisson distribution to see how many other people that case infects.
- Increase the number of cases in the relevant district.
- Increase the number of cases relative to the population density of the district i.e. higher population density should result in a slightly higher chance of increase of cases in that district.
- Decrease the number of cases relative to a recovery rate (which is around 30% globally (https://www.worldometers.info/coronavirus/)).
- Since people also travel between districts, we model the flow of infected people as well.
- We use data on traffic flow between districts to first estimate how many people travel on any given day (normally distributed variation).
- Once we estimate how many people flow between districts, we simulate how many of those travellers are carriers/infected.
- Increase the number of cases in the specific district since now you have travellers that are infected that have reached the district.
- Subtract the number of cases from the city where the carriers/infected travelled came from.
- Repeat this for each district

# Parameters and Parameters

For the function **simulate day**:
- **Lambda** = Parameter for the poisson distribution from which we sample how many other people an already infected person spreads the  virus to
- **recovery** = Parameter to set the recovery rate for the whole simulation
- **Effect of density** = On line 43 (below #Multiplier effect due to density of city), you can change the effect of a district's density by varying the parameters of the normal distribution



# Note
I am currently modeling the spread of the disease in the province of Sindh, Pakistan. I do not have time at the moment to update the readme file, but you can shoot me a message at abdul.qadir@minerva.kgi.edu if you need an understanding quickly.


