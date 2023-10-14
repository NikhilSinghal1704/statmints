import pandas as pd
import re
import plotly.graph_objs as go


class BankStatementProcessor:
    def __init__(self, xlsx_file):
        self.df = pd.read_excel(xlsx_file)
        self.dataframes_by_type = {}
        self.dataframes_by_method = {}
        self.process_data()

    def extract_for_upi(self, entry):
        entry = entry.split("/")
        reference_id, to, upi_id, name = entry[1:]
        return reference_id, to, upi_id, name

    def extract_for_neft(self, entry):
        entry = entry.split("/")
        name = entry[-1]
        return name

    def extract_method_of_payment(self, entry):
        upi_pattern = r'UPI/\d+'
        neft_pattern = r'NEFT_IN:\S+'
        atm_pattern = r'ATM WDR \d+'
        imp_pattern = r'IMPS-IN/\d+'

        if re.search(upi_pattern, entry):
            return "UPI Payment"
        elif re.search(neft_pattern, entry):
            return "NEFT Payment"
        elif re.search(atm_pattern, entry):
            return "ATM Withdrawal"
        elif re.search(imp_pattern, entry):
            return "IMPS Payment"
        else:
            return "Other"

    def process_data(self):
        self.df['Method of Payment'] = self.df['Remarks'].apply(
            self.extract_method_of_payment)

        for type_value in self.df['Type'].unique():
            type_df = self.df[self.df['Type'] == type_value]
            self.dataframes_by_type[type_value] = type_df

        for method_of_payment in self.df['Method of Payment'].unique():
            method_df = self.df[self.df['Method of Payment']
                                == method_of_payment]
            self.dataframes_by_method[method_of_payment] = method_df

        upi_df = self.dataframes_by_method["UPI Payment"]
        upi_df[['Reference_ID', 'To', 'UPI_ID', 'Name']] = upi_df['Remarks'].apply(
            self.extract_for_upi).apply(pd.Series)
        self.dataframes_by_method['UPI Payment'] = upi_df

        IMPS_df = self.dataframes_by_method['IMPS Payment']
        IMPS_df['Name'] = IMPS_df['Remarks'].apply(self.extract_for_neft)

        NEFT_df = self.dataframes_by_method['NEFT Payment']
        NEFT_df['Name'] = NEFT_df['Remarks'].apply(self.extract_for_neft)

    def create_pie_chart(self):
        method_counts = self.df['Method of Payment'].value_counts()
    
        # Create a pie chart using Plotly
        pie_chart = go.Figure(data=[go.Pie(
            labels=method_counts.index,
            values=method_counts,
            hole=0.7,
            marker_colors=['#ff9999', '#66b3ff', '#99ff99', '#c2c2f0'],
            textinfo='percent+label'
        )])
    
        # Convert the chart to JSON
        pie_chart_data = pie_chart.to_json()
    
        return pie_chart_data

    def create_monthly_graph(self):
        # Convert 'Date' column to datetime
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d-%m-%Y')
    
        # Extract the year and month from the 'Date' column
        self.df['YearMonth'] = self.df['Date'].dt.to_period('M')
    
        # Group the data by YearMonth and calculate the sum of credits (CR) and debits (DR)
        monthly_data = self.df.groupby(['YearMonth', 'Type'])['Amount'].sum().unstack(fill_value=0)
    
        # Create a bar graph using Plotly
        bar_graph = go.Figure()
    
        # Specify the width of the bars (you can adjust this value as needed)
        bar_width = 0.4
    
        # Create CR bars
        bar_graph.add_trace(go.Bar(
            x=monthly_data.index.strftime('%m/%y'),
            y=monthly_data['CR'],
            name='CR',
            marker_color='lightgreen',
            width=bar_width,
        ))
    
        # Create DR bars
        bar_graph.add_trace(go.Bar(
            x=monthly_data.index.strftime('%m/%y'),
            y=monthly_data['DR'],
            name='DR',
            marker_color='lightblue',
            width=bar_width,
        ))
    
        # Customize the appearance of the bar graph
        bar_graph.update_layout(
            barmode='group',  # Use 'group' to group CR and DR bars for each month
            xaxis_tickangle=-45,
            xaxis_title='Month (MM/YY)',
            yaxis_title='Amount',
            title='Monthly Credits (CR) and Debits (DR)',
        )
    
        return bar_graph.to_json()

    def get_dataframes_by_type(self):
        return self.dataframes_by_type

    def get_dataframes_by_method(self):
        return self.dataframes_by_method
