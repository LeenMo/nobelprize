import pandas as pd
import seaborn as sns
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.ticker import PercentFormatter
import plotly.express as px

nobel = pd.read_csv('nobel.csv')
st.title("Nobel Prize Analytics")


nobel['decade'] = (np.floor(nobel['year']/10)*10).astype(int)

#calculate birthdate and age of NP winners
nobel['birth_date'] = pd.to_datetime(nobel['birth_date'])
nobel['age'] = nobel['year'] - (pd.DatetimeIndex(nobel['birth_date']).year)



# Add a selectbox to the sidebar:
navigate = st.sidebar.selectbox(
    "Navigate to",
    ("Home Page", "About", "Analysis"))

if navigate == "Home Page":
	st.balloons()
	st.subheader("Check the sidebar for navigation options!")
	st.subheader("")
	IMAGE_URL = "https://www.nobelprize.org/images/52993-landscape-full-width-2x.jpg"
	st.image(IMAGE_URL, use_column_width=True)



#if chose ABOUT
if navigate == "About":
	st.write("The Nobel prize is one of the most famous and prestigious\
	 intellectual awards. It is awarded annually for 6 different categories. \
	 From Stockholm, the Royal Swedish Academy of Sciences confers the prizes \
	 for physics, chemistry, and economics, the Karolinska Institute confers \
	 the prize for physiology or medicine, and the Swedish Academy confers the \
	 prize for literature. The Norwegian Nobel Committee based in Oslo confers \
	 the prize for peace.")
	st.write('A person or organization awarded the Nobel Prize \
	 is called a Nobel Laureate. The word "laureate" refers to the laurel wreath \
	 that was considered as "a trophy" in ancient greek, given to victors of \
	 competitions (image to the right).')
	st.write("This dataset lists all prize winners from the start of the prize in 1901 till 2016.")

	view_nobel=st.checkbox("View a snippet of the dataset")
	if view_nobel:
		st.write(nobel.head(10))


if navigate == "Analysis":
	view_analysis = st.sidebar.selectbox(
    "View",
    ("Countries with most laureates", "Laureates by country and decade",
     "Laureates by category and decade", "Female Nobel Prize winners", 
     "Winners with more than one Nobel Prize",
     "Nobel Prize winners' ages", "Prize categories by age", 
    "Interesting stats"))

	if view_analysis == "Countries with most laureates" :
		st.subheader("Countries with the most laureates")
		val = st.slider(
	    "How many countries would you like to view?", 1, 20,50)
		st.write("The " , val, " countries with most laureats are")
		top_countries = nobel['birth_country'].value_counts() #create new series to save the output in
		st.write(top_countries.head(val))


	if view_analysis == "Laureates by country and decade" :
		st.subheader("The proportions of Nobel Prize winners per country and decade")
		unique_countries = nobel['birth_country'].unique() #create new series with the unique countries only
		country = st.selectbox("Choose a country", unique_countries)
		
		#Add country column to nobel, where the value is True when birth_country is whatever country the user chose.
		nobel[country] =  np.where( nobel['birth_country'] == country, True, False)
		#Add a decade column to nobel for the decade each prize was awarded. Here, np.floor() will come in handy. Ensure the decade column is of type int64.
		prop_winners = nobel.groupby(['decade'], as_index = False)[country].mean()
		
		#add a checkbox to ask the user if she'd like to see the table
		view_prop_t=st.checkbox("View the list of proportions")
		if view_prop_t:
			st.write(prop_winners)
		#add a checkbox to ask the user if she'd like to see a graph
		view_prop_g=st.checkbox("View a graph of the proportions")
		if view_prop_g:
			fig_prop = px.line(prop_winners, x='decade', y=country)
			st.write(fig_prop)

	if view_analysis == "Laureates by category and decade" :
			st.subheader("The proportions of Nobel Prize winners per category and decade")
			unique_categories = nobel['category'].unique() #create new series with the unique countries only
			catg = st.selectbox("Choose a category", unique_categories)
			
			#Add country column to nobel, where the value is True when birth_country is whatever country the user chose.
			nobel[catg] =  np.where( nobel['category'] == catg, True, False)
			#Add a decade column to nobel for the decade each prize was awarded. Here, np.floor() will come in handy. Ensure the decade column is of type int64.
			prop_catg = nobel.groupby(['decade'], as_index = False)[catg].mean()
			
			#add a checkbox to ask the user if she'd like to see the table
			view_prop_t=st.checkbox("View the list of proportions")
			if view_prop_t:
				st.write(prop_catg)
			#add a checkbox to ask the user if she'd like to see a graph
			view_prop_g=st.checkbox("View a graph of the proportions")
			if view_prop_g:
				fig_prop = px.line(prop_catg, x='decade', y=catg)
				st.write(fig_prop)


	if view_analysis == "Female Nobel Prize winners" :
		st.subheader("Gender of typical Nobel Prize winners")
		#add column for gender analysis
		nobel['female_winner'] = np.where(nobel['sex'] == 'Female', True, False)
		prop_female_winners = nobel.groupby(['decade', 'category'], as_index = False)['female_winner'].mean() 

		view_female_t=st.checkbox("View the list of female winners by decade and category")
		if view_female_t:
			st.write(prop_female_winners)

		view_female_g=st.checkbox("View a graph of female winners by decade and category") 
		if view_female_g:
			fig_female = px.line(prop_female_winners, x='decade', y='female_winner', color='category')
			st.write(fig_female)

	
	if view_analysis == "Winners with more than one Nobel Prize" :
		st.subheader("Who are the few winners that got more than one Nobel Prize?")
		mult_w = nobel.groupby('full_name').filter(lambda group: len(group) >= 2)
		st.write(mult_w)


	if view_analysis == "Nobel Prize winners' ages" :
		st.subheader("How old were the winners at the time they got the Nobel Prize?")
		mean_age = np.floor(nobel['age'].mean())
		st.write("The average age of winners was ", mean_age, ".")
		st.write("Check out the graph below for a clear view of Nobel Prize winners' ages.")
		fig_age = px.scatter(nobel, x="year", y="age", trendline="lowess")
		st.write(fig_age)

	if view_analysis == "Prize categories by age" :
		st.subheader("Age differences between prize categories")
		fig_age_cat = px.scatter(nobel, x="year", y='age', facet_row='category', 
			color='category' ,facet_row_spacing=0.05 ,trendline="lowess", width=900, height=1000)
		st.write(fig_age_cat)

	if view_analysis == "Interesting stats" :
		st.subheader("Want to know some interesting facts?")
		view_oldest=st.checkbox("Who was the oldest winner?!")
		if view_oldest:
			oldest= nobel.nlargest(1, 'age')[['full_name','age', 'year', 'birth_country','category']]
			st.write(oldest)
		view_youngest=st.checkbox("Who was the youngest winner")
		if view_youngest:
			st.write(nobel.nsmallest(1, 'age')[['full_name','age', 'year', 'birth_country','category']])

		view_female1 =st.checkbox("Who was the first female to win a Nobel prize?")
		if view_female1 :
			females_only = nobel.loc[nobel['sex'] == 'Female']    #is creating a new df a bad practice?
			st.write(females_only.nsmallest(1, 'year')[['full_name','year','category']])
