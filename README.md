# sqlalchemy-challenge
I'd love to go on vacation in Honolulu, Hawaii, but I'm not sure if the climate there is nice! To help with my trip planning, I need to do some climate analysis on the area using Python, SQLAlchemy, Pandas, and Matplotlib. 

To begin, I use SQLAlchemy create_engine to connect to my sqlite database of Hawaiian weather station data. I use SQLAlchemy automap_base() to reflect my tables into classes and save a reference to those classes called Station and Measurement. Next, I link Python to the database by creating an SQLAlchemy session.

I analyze Hawaiian precipitation as follows:
Start by finding the most recent date in the data set.
Using this date, retrieve the last 12 months of precipitation data by querying the 12 preceding months of data.
Load the query results into a Pandas DataFrame and set the index to the date column.
Sort the DataFrame values by date.
Plot the results using the DataFrame plot method.

I'm also curious about the weather stations that gathered this data. Therefore, I also:
Design a query to calculate the total number of stations in the dataset.
Design a query to find the most active stations (i.e. which stations have the most rows?).
List the stations and observation counts in descending order.
Identify the station with the highest number of observations.
Using the most active station id, calculate the lowest, highest, and average temperature.
Design a query to retrieve the last 12 months of temperature observation data (TOBS).
Filter by the station with the highest number of observations.
Query the last 12 months of temperature observation data for this station.
Plot the results as a histogram with bins=12.

Now that I have completed your initial analysis, I design a Flask API based on the queries that I have just developed.

My home page lists all routes that are available:

/api/v1.0/precipitation -
connvert the query results to a dictionary using date as the key and prcp as the value and return the JSON representation of the dictionary.

/api/v1.0/stations - 
Return a JSON list of stations from the dataset.

/api/v1.0/tobs - 
Query the dates and temperature observations of the most active station for the last year of data. Return a JSON list of temperature observations (TOBS) for the previous year.

/api/v1.0/<start> and /api/v1.0/<start>/<end> - 
Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
