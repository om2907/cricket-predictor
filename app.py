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

team_colors = {
    'Sunrisers Hyderabad': '#FE6B18',        # Bhagwa
    'Mumbai Indians': '#004AA0',              # Blue
    'Royal Challengers Bangalore': '#BC1520',  # Red
    'Kolkata Knight Riders': '#2E0854',        # Purple
    'Punjab Kings': '#D50032',                 # Reddish-Pink
    'Chennai Super Kings': '#FFF05B',          # Yellow
    'Rajasthan Royals': '#FFC0CB',             # Hot pink
    'Delhi Capitals': '#004D80',               # Dark Blue
    'Gujarat Titans': '#1E1E28',               # Black
    'Lucknow Super Giants': '#660066'          # Dark Purple
}

ball = [0,1,2,3,4,5]


pipe = pickle.load(open('logistic_regression.pkl', 'rb'))

st.title('IPL Win Predictor')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams), index=0)
with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted(teams), index=5)

selected_city = st.selectbox('Select host city', sorted(cities), index=14)

target = st.number_input('Target', value=240)

col3, col4, col5, col6 = st.columns(4)

with col3:
    score = st.number_input('Score', value=150)
with col4:
    overs = st.number_input('Overs completed', value=15,max_value=20, step=1)


if(overs==20):

    with col5:
        balls = st.selectbox('Balls bowled',sorted(ball), disabled=True)
else:
    with  col5:
        balls = st.selectbox('Balls bowled',sorted(ball))
with col6:
    wickets = st.number_input('Wickets out', max_value=10, value=5)


    




if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 121 - ((overs*6) + (balls))
    wickets_left = 10 - wickets
    crr = score/overs
    rrr = (runs_left*6)/balls_left
    print(120 - balls_left +1)
    input_df = pd.DataFrame({'Batting_Team': [batting_team], 'Bowling_Team': [bowling_team], 'City': [selected_city],
                             'runs_left': [runs_left], 'balls_left': [balls_left], 'wickets_left': [wickets_left],
                             'Total_Runs_x': [target], 'crr': [crr], 'rrr': [rrr]})

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    






    if(wickets >= 10 or balls_left==1):
        win_chart=0
    else:
        win_chart= round(win*100)
    loss_chart= round(loss*100)
    #st.header(batting_team + "- " + str(round(win*100)) + "%")
    #st.header(bowling_team + "- " + str(round(loss*100)) + "%")


    import plotly.graph_objects as go

        # Data to plot
    labels = [batting_team, bowling_team]
    values = [win_chart, loss_chart]

    colors = [team_colors.get(batting_team, 'gray'), team_colors.get(bowling_team, 'gray')]
    

    # Set explode effect for the slices
    explode = [0, 0.1]  # Explode the first slice (Win) by 0.1


        # Create the figure
    fig = go.Figure()

        # Add trace for outer pie (green)
    fig.add_trace(go.Pie(labels=labels, values=values, hole=0.5, marker=dict(colors=colors), pull=explode))

        # Update layout
    fig.update_layout(title_text="Probability of Result", showlegend=True)

        # Show the plot
    st.plotly_chart(fig)

