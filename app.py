import streamlit as st
import pickle
import pandas as pd

teams = [
    'Sunrisers Hyderabad',
    'Mumbai Indians',
    'Royal Challengers Bangalore',
    'Kolkata Knight Riders',
    'Punjab Kings',
    'Chennai Super Kings',
    'Rajasthan Royals',
    'Delhi Capitals',
    'Gujarat Titans',
    'Lucknow Super Giants'
]

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
          'Chandigarh', 'Jaipur', 'Chennai',
          'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
          'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
          'Sharjah', 'Mohali', 'Bengaluru']

method = ['KNN', 'Random Forest', 'Linear_Regression']

selected_method = st.selectbox('Select Algorithm', sorted(method))

if selected_method == 'KNN':
    pipe = pickle.load(open('knn.pkl', 'rb'))
elif selected_method == 'Random Forest':
    pipe = pickle.load(open('random_forest.pkl', 'rb'))
elif selected_method == 'Linear_Regression':
    pipe = pickle.load(open('logistic_regression.pkl', 'rb'))

st.title('IPL Win Predictor')

def generate_default_values():
    return teams[0], teams[1], cities[0], 200, 150, 15, 5

# Default values
batting_team, bowling_team, selected_city, target, score, overs, wickets = generate_default_values()

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams), index=0)
with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted(teams), index=1)

selected_city = st.selectbox('Select host city', sorted(cities), index=0)

target = st.number_input('Target', value=200)

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input('Score', value=150)
with col4:
    overs = st.number_input('Overs completed', value=15.0, step=0.1)
with col5:
    wickets = st.number_input('Wickets out', value=5)

if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (overs*6)
    wickets_left = 10 - wickets
    crr = score/overs
    rrr = (runs_left*6)/balls_left

    input_df = pd.DataFrame({'Batting_Team': [batting_team], 'Bowling_Team': [bowling_team], 'City': [selected_city],
                             'runs_left': [runs_left], 'balls_left': [balls_left], 'wickets_left': [wickets_left],
                             'Total_Runs_x': [target], 'crr': [crr], 'rrr': [rrr]})

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_team + "- " + str(round(win*100)) + "%")
    st.header(bowling_team + "- " + str(round(loss*100)) + "%")