
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout='wide',page_title='Startup Analysis')

df=pd.read_csv('startup_cleaned.csv')
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['month']=df['date'].dt.month
df['year'] = df['date'].dt.year


def load_overall_analysis():
    st.title("Overall Analysis")

    #Total amount
    total=round(df['amount'].sum())
    #Maximum amount infused in startup
    max=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    max=round(max)
    #Average funding to astartup
    avg_funding=round(df.groupby('startup')['amount'].sum().mean())
    #Total Funded Startups
    num_startup=df['startup'].nunique()

    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric("Total", str(total) + " " + 'Cr')
    with col2:
        st.metric("Max",str(max)+ ' ' + "Cr")
    with col3:
        st.metric("Average",str(avg_funding) +" "+"Cr")
    with col4:
        st.metric("Funded Startups", num_startup)
    col1,col2=st.columns(2)
    #MOM Plot
    with col1:
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        temp_df['x_axis'] = temp_df['year'].astype("str") + "-" + temp_df['month'].astype('str')

        st.subheader('Overall Month On month Plot')
        fig5, ax5 = plt.subplots()
        ax5.plot(temp_df['x_axis'],temp_df['amount'])
        # ax5.set_xlabel('')
        ax5.set_ylabel('Investment (in Cr)')
        # Rotate x-axis labels to vertical
        plt.xticks(rotation='vertical')
        # Display every n-th label (adjust n as needed)
        n = 3
        for i, label in enumerate(ax5.xaxis.get_ticklabels()):
            if i % n != 0:
                label.set_visible(False)
        st.pyplot(fig5)

    with col2:
        # Assuming 'top5' and 'other_city' are already defined
        top5 = df['city'].value_counts().sort_values(ascending=False).head(10)
        # other_city = df[~df['city'].isin(['Bangalore', 'Mumbai', 'New Delhi', 'Bengaluru'])]['city'].value_counts().sum()
        other_city = df[~df['city'].isin(
            ['Bangalore', 'Mumbai', 'New Delhi', 'Bengaluru', 'Pune', 'Hyderabad', 'Chennai', 'Noida', 'Gurugram'])][
            'city'].value_counts().sum()
        # Create DataFrames from the Series
        df_top5 = pd.DataFrame({'City': top5.index, 'Count': top5.values})
        df_other_city = pd.DataFrame({'City': ['Other'], 'Count': [other_city]})

        # Concatenate DataFrames vertically
        result_df = pd.concat([df_top5, df_other_city], ignore_index=True)

        st.subheader('Frequent invested city')
        fig6, ax6 = plt.subplots()
        explode = (0, 0, 0, 0, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0)
        ax6.pie(result_df['Count'],autopct='%0.1f%%', labels=result_df['City'], explode=explode)
        st.pyplot(fig6)

    col1, col2 = st.columns(2)
    # Top 10 funded startups
    with col2:
        st.subheader('Top 10 funded startups')
        top10_invested = df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10)
        fig7, ax7 = plt.subplots()
        ax7.bar(top10_invested.index, top10_invested.values)
        plt.xticks(rotation=45)
        ax7.set_xlabel('Startups')
        ax7.set_ylabel('Investment (in Cr)')
        st.pyplot(fig7)
    #Top Investors
    with col1:
        st.subheader("Top Investors")
        top_investors=df.groupby('investors')['amount'].sum().sort_values(ascending=False).head(10)
        st.dataframe(top_investors)
def load_startup_details(startup):
    st.title("Startup Analysis")
    first5_df=df[df['startup'].str.contains(startup)][
        ['investors','year','vertical', 'subvertical', 'city', 'round', 'amount']]
    st.subheader('Interested Investors')
    st.dataframe(first5_df)



    col1,col2=st.columns(2)
    #Top 10 funded startups
    with col1:
        st.subheader("Top Investors")
        temp_df = df[df['startup'].str.contains(startup)].groupby('investors')['amount'].sum().sort_values(
            ascending=False).head(10)
        st.dataframe(temp_df)

    #Frequent funded sector
    with col2:
        st.subheader('Frequent Funded sector')
        funded_sector=df[df['startup'].str.contains(startup)]['vertical'].value_counts()
        fig8, ax8 = plt.subplots()
        ax8.pie(funded_sector,labels=funded_sector.index,autopct='%0.1f%%')
        st.pyplot(fig8)

    col1,col2=st.columns(2)
    #Ffrequent funding city
    with col1:
        st.subheader('Funding city')
        df['city'] = df['city'].replace('Bangalore', 'Bengaluru')
        funded_city=df[df['startup'].str.contains(startup)]['city'].value_counts()
        fig9, ax9 = plt.subplots()
        ax9.pie(funded_city, labels=funded_city.index, autopct='%0.1f%%')
        st.pyplot(fig9)
    with col2:
        st.subheader('YOY funding')
        yoy_fund = df[df['startup'].str.contains(startup)].groupby('year')['amount'].sum()
        fig7, ax7 = plt.subplots()
        ax7.plot(yoy_fund)
        plt.xticks(rotation=45)
        ax7.set_xlabel('Year')
        ax7.set_ylabel('Funding (in Cr)')
        st.pyplot(fig7)





def load_investor_details(investor):
    st.title(investor)
    #loading the most 5 investment of the investor
    last5_df=df[df['investors'].str.contains(investor)].head()[['date','startup', 'vertical', 'subvertical', 'city', 'round', 'amount']]
    st.subheader('Most recent Investments')
    st.dataframe(last5_df)

    #Biggest Investment

    col1,col2=st.columns(2)
    with col1:
        big_series=df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader("Biggest Investment")
        fig,ax=plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_series=df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors Invested in')
        fig1,ax1=plt.subplots()
        ax1.pie(vertical_series.values,labels=vertical_series.index,autopct="%0.1f%%")
        st.pyplot(fig1)

    # Stage and Region wise Funding
    col1, col2 = st.columns(2)
    with col1:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Stages of investment')
        fig2, ax2 = plt.subplots()
        ax2.pie(vertical_series.values, labels=vertical_series.index, autopct="%0.1f%%")
        st.pyplot(fig2)

    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        vertical_series=pd.DataFrame(vertical_series)
        st.subheader('City invested  in')
        fig3 = px.pie(vertical_series, values='amount', names=vertical_series.index, hole=0.5)
        fig3.update_traces(textposition='inside', textinfo='label+percent')
        fig3.update_layout(showlegend=True, height=400, width=500)
        st.plotly_chart(fig3)

    col1, col2 = st.columns(2)
    with col1:

        year_series=df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
        st.subheader('YOY Investment')
        fig4, ax4 = plt.subplots()
        ax4.plot(year_series)
        st.pyplot(fig4)


st.sidebar.title("Startup Funding Analysis")

options=st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Inverstors'])

if options=='Overall Analysis':
    btn0=st.sidebar.button("Show Overall Analysis")
    if btn0:
        load_overall_analysis()

elif options=='StartUp':
    selected_startup=st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button("Show Startup Details")
    if btn1:
        load_startup_details(selected_startup)
else:
    selected_investor=st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    btn2=st.sidebar.button("Show Invester Details")
    if btn2:
        load_investor_details(selected_investor)
