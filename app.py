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

short_forms = {
    'Sunrisers Hyderabad': 'SRH',
    'Mumbai Indians': 'MI',
    'Royal Challengers Bangalore': 'RCB',
    'Kolkata Knight Riders': 'KKR',
    'Punjab Kings': 'PBKS',
    'Chennai Super Kings': 'CSK',
    'Rajasthan Royals': 'RR',
    'Delhi Capitals': 'DC',
    'Gujarat Titans': 'GT',
    'Lucknow Super Giants': 'LSG'
}

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
filtered_ball = [1,2,3,4,5]
def_ball = 0


pipe = pickle.load(open('logistic_regression.pkl', 'rb'))

st.title('IPL Win Predictor')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams), index=0)
with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted(teams), index=5)

selected_city = st.selectbox('Select host city', sorted(cities), index=14)

col1, col2 = st.columns(2)

with col1 :
    target = st.number_input('Target', value=1,min_value=1)

with col2:
    score = st.number_input('Current Score', value=0,min_value=0,max_value = target-1)

col4, col5, col6 = st.columns(3)

with col4:
    overs = st.number_input('Overs completed', value=0,max_value=19, step=1,min_value=0)


if(overs==20):

    with col5:
        balls = st.selectbox('Maximum overs are bowled',sorted(ball), disabled=True)

elif(overs==0):
    with col5:
        balls = st.selectbox('Balls bowled in current over',sorted(filtered_ball), index=ball.index(def_ball))
else:
    with col5:
        balls = st.selectbox('Balls bowled in current over',sorted(ball))
tot_balls = ((overs*6) + (balls))        
with col6:
    wickets = st.number_input('Wickets out', max_value=tot_balls, value=0,min_value=0)


    

#button = st.button('Predict Probability')



    
def ipl_win_predictor():    
        runs_left = target - score
        balls_left = 120 - tot_balls
        wickets_left = 10 - wickets
        crr = score/(overs + balls)
        rrr = (runs_left*6)/(balls_left)
        input_df = pd.DataFrame({'Batting_Team': [batting_team], 'Bowling_Team': [bowling_team], 'City': [selected_city],
                                'runs_left': [runs_left], 'balls_left': [balls_left], 'wickets_left': [wickets_left],
                                'Total_Runs_x': [target], 'crr': [crr], 'rrr': [rrr]})

        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]
        






        if(wickets >= 10 or balls_left==0 or rrr>36):
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
        fig.add_trace(go.Pie(labels=labels, values=values, hole=0.5, marker=dict(colors=colors)))

            # Update layout
        st.write("\n")
        st.write("<h3>Probability of Result</h3>", unsafe_allow_html=True)
        fig.update_layout( showlegend=True)
        fig.update_layout(width=400, height=400)
        fig.update_layout(legend=dict(x=1, y=0, orientation='h'))

        run_req = short_forms[batting_team] + " need " + str(runs_left) + " runs in " + str(balls_left ) + " balls"
        crr_text = "Current Run Rate : " + str(crr)
        rrr_text = "Required Run Rate : " + str(rrr)
        scorecard = str(score)+ "/" + str(wickets) + " in " + str(overs) + "." + str(balls) + " Overs" 

        col1, col2 = st.columns(2)
        with col2:
            st.write("\n")
            st.write("<h3>Scorecard</h3>" + "<h3>" + short_forms[batting_team] + " vs " + short_forms[bowling_team] + "</h3>", unsafe_allow_html=True)
            st.write(scorecard)
            st.write(run_req)
            st.write(crr_text)
            st.write(rrr_text)
            
            # Show the plot
        with col1:
            st.plotly_chart(fig)

# Call the function to run the Streamlit app
if __name__ == "__main__":
    ipl_win_predictor()

#if button:
    #ipl_win_predictor()
