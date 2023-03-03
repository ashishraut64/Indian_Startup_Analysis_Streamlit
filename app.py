import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(layout='wide',page_title='Startup Analysis')
df = pd.read_csv('startup_cleaned.csv')
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['month']=df['date'].dt.month
df['year']=df['date'].dt.year



def overall_analysis():
    st.title('Overall Analysis')
    col1,col2,col3,col4 = st.columns(4)
    #Total
    with col1:
        total = round(df['amount'].sum())
        st.metric('Total Investment',str(total) + ' Cr')
    #Maximum
    with col2:
        max=round(df.groupby('startup')['amount'].sum().max(),2)
        st.metric('Maximum Investment',str(max) + ' Cr')
    with col3:
        avg=round(df.groupby('startup')['amount'].sum().mean(),2)
        st.metric('Average Investment',str(avg) + " Cr")
    with col4:
        num=df['startup'].nunique()
        st.metric('Total Funded Startups',str(num) + ' Cr')
    #MOM Chart
    if 'key' not in st.session_state:
        st.session_state['key'] = 'value'
    st.subheader('Month-on-Month Chart')
    selected_option = st.selectbox('MOM', ['Startups Funded', 'Amount Funded'])
    btn4= st.button('Analyse MOM')
    if btn4:
        if selected_option=='Amount Funded':
            temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
            temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)
            fig2 =px.line(temp_df,x=temp_df['x_axis'],y=temp_df['amount'],markers=True,labels={'x_axis':'Month & Year','amount':'Amount in Cr'})
            st.plotly_chart(fig2)
        else:
            temp_df = df.groupby(['year', 'month'])['startup'].count().reset_index()
            temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)
            fig3 = px.line(temp_df, x=temp_df['x_axis'], y=temp_df['startup'],markers=True,labels={'x_axis':'Month & Year','startup':'No. of Startups'})
            st.plotly_chart(fig3)
    #Sector Analysis Pie
    st.subheader('Sector-Wise Analysis')
    selected_option=st.selectbox('Sector-Wise',['Sector Invested','Amount Invested'])
    btn3= st.button('Analyse Sectors')
    if btn3:
        if selected_option=='Sector Invested':
            data = df['vertical'].value_counts()
            temp = data[data.values > 10]
            fig1 = px.pie(values=temp, names=temp.index)
            st.plotly_chart(fig1)
        else:
            data = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(20)
            fig = px.pie(values=data, names=data.index)
            st.plotly_chart(fig)
    #Type of Funding
    st.subheader('Type of Funding')
    data = df['rounds'].value_counts()
    temp = data[data.values > 10]
    fig=px.pie(values=temp, names=temp.index)
    st.plotly_chart(fig)
    #City
    st.subheader('City-Wise Investment')
    temp = df.groupby('city')['amount'].sum().sort_values(ascending=False).head(25)
    fig4=px.bar(temp, x=temp.index, y=temp.values, text_auto=True)
    st.plotly_chart(fig4)
    #Top-Investors
    temp = df.groupby('investors')['amount'].sum().sort_values(ascending=False).head(10)
    fig5=px.bar(temp,x=temp.index,y=temp.values,color=temp.index,text_auto=True,labels={'y':'Amount in Cr','investors':'Investors'})
    st.plotly_chart(fig5)



def investor_details(investor):
    st.title(investor)
    #Most recent investment
    last5_invest=df[df['investors'].str.contains(investor)][
        ['date', 'startup', 'vertical', 'city', 'rounds', 'amount']].head()
    st.subheader('Most Recent Investments')
    st.dataframe(last5_invest)
    #Biggest Investment
    st.subheader('Biggest Investments')
    col1,col2,col3= st.columns(3)
    with col1:
        big_invest = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(
            ascending=False).head()
        st.dataframe(big_invest)
    with col2:
        fig=px.bar(big_invest,x=big_invest.index,y=big_invest.values,color=big_invest.index,labels={'y':'Amount in Cr','startup':'Startup'})
        st.plotly_chart(fig)
    #Sectors Invested In
    st.subheader('Sectors Invested In')
    col1,col2,col3=st.columns(3)
    with col1:
        vertical_sector = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().sort_values(ascending=False).head()
        st.dataframe(vertical_sector)
    with col2:
        vertical_sector = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().sort_values(ascending=False).head(10)
        fig1=px.pie(values=vertical_sector,names=vertical_sector.index)
        st.plotly_chart(fig1)
    #Rounds
    st.subheader('Stage')
    col1, col2,col3= st.columns(3)
    with col1:
        round_in = df[df['investors'].str.contains(investor)].groupby('rounds')['amount'].sum().sort_values(ascending=False).head()
        st.dataframe(round_in)
    with col2:
        round_in = df[df['investors'].str.contains(investor)].groupby('rounds')['amount'].sum().sort_values(ascending=False)
        fig2=px.pie(values=round_in,names=round_in.index)
        st.plotly_chart(fig2)
    #City
    st.subheader('Investment in City')
    col1, col2,col3 = st.columns(3)
    with col1:
        city_in = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum().sort_values(ascending=False).head()
        st.dataframe(city_in)
    with col2:
        city_in = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum().sort_values(ascending=False).head(10)
        fig3=px.pie(values=city_in,names=city_in.index)
        st.plotly_chart(fig3)
    #YOY Investment
    st.subheader('YOY Investment')
    df['year']=df['date'].dt.year
    col1, col2,col3 = st.columns(3)
    with col1:
        YOY = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
        st.dataframe(YOY)
    with col2:
        YOY = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
        fig4= px.bar(YOY,x=YOY.index,y=YOY.values,color=YOY.index,labels={'y':'Amount in Cr'})
        st.plotly_chart(fig4)



def startup_details(startup):
    #Company Name
    st.header(startup)
    #Vertical
    st.subheader('Verticals and Investment')
    temp = df[df['startup'] == startup].groupby('vertical')['amount'].sum()
    fig=px.pie(values=temp, names=temp.index)
    st.plotly_chart(fig)
    #City
    st.subheader('City and Investment')
    col1,col2,col3=st.columns(3)
    with col1:
        temp=df[df['startup'] == startup].groupby('city')['amount'].sum()
        st.dataframe(temp)
    with col2:
        fig1=px.bar(temp, x=temp.index, y=temp.values, color=temp.index)
        st.plotly_chart(fig1)
    #Investors
    st.subheader('Investors and Investment')
    col1,col2=st.columns(2)
    with col1:
        temp = df[df['startup'] == startup].groupby('investors')['amount'].sum().reset_index()
        temp.rename(columns={'investors': 'Investors', 'amount': 'Amount'}, inplace=True)
        st.dataframe(temp)
    with col2:
        fig2=px.bar(temp, x=temp['Investors'], y=temp['Amount'],color=temp['Investors'])
        st.plotly_chart(fig2)
    #Funding Rounds
    st.subheader('Funding Round Details')
    temp=df[df['startup'] == startup][['rounds', 'date', 'investors']].set_index('rounds')
    st.dataframe(temp)






st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])
if option=='Overall Analysis':
    overall_analysis()
elif option=='Startup':
    #st.title('Startup Analysis')
    selected_startup=st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    if btn1:
        startup_details(selected_startup)
elif option=='Investor':
    #st.title('Investor Analysis')
    selected_investor=st.sidebar.selectbox('Select Startup',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        investor_details(selected_investor)

