from shiny import App, Inputs, Outputs, Session, render, ui, reactive
from shinyswatch import theme
from shiny.types import FileInfo
import os
import pandas as pd
import numpy as np
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules    
    
#UI functions
def custom_value_transform(value):
    if value <= 1:
        return value * 0.2
    else:
        return (value - 1) * 2 + 0.2

slider_value=0
number_of_itemsets = 0
selected_i = 0
selected_e = 0

number_of_rules = 0
selected_r = 0
# file_name: str = "xyz"
    
def make_panels():
    return [
        ui.accordion_panel(
            f"Start",
            ui.card( 
                ui.card_header("Choose file"),
                ui.input_checkbox("checkbox_samplefile", "Use sample file", True),
                # ui.input_file("file1", "Upload CSV File", accept=[".csv"], multiple=False),
                # # ui.input_action_button("confirm_file_button_s", "Confirm your file"),
                # ui.div({"style": "text-align: center;"}, "or"),
                id="card_start_cf",
                full_screen=True,
            ),
                ui.card( 
                ui.card_header("Display option"),
                ui.input_checkbox("checkbox_of", "Show original file", False),
                ui.input_checkbox("checkbox_fi", "Show frequent itemsets", False),
                ui.input_checkbox("checkbox_ar", "Show association rules", False),
                id="card_start_do",
                full_screen=True,
            )
        ),        
                
        ui.accordion_panel(
            f"Frequent Itemsets",
            ui.card(
                ui.card_header("Info"),
                ui.p(
                    f"Number of itemstes: {number_of_itemsets}", ui.br(),
                    f"Selected itemstes: {selected_i}", ui.br(), 
                    f"Selected examples: {selected_e}", ui.br(),
                ),
                ui.input_action_button("expand_all_button1_fi", "Expand all"),  
                ui.input_action_button("collapse_all_button1_fi", "Collapse all"),
                full_screen=True,
            ),
                        
            ui.card(
                ui.card_header("Find itemsets"),
                ui.p(ui.input_slider("minsupp_slider_fi", "Minimal support:", 0.1, 100, 2, step=1, post="%")),
                ui.p(ui.input_slider("max_itemsets_slider_fi", "Max. number of itemsets:", 10, 100000, 10000)),
                full_screen=True,
            ),
            
            ui.card(   
                ui.card_header("Filter itemsets"),
                ui.input_text("containing_text_fi", "Contains: "),
                ui.input_numeric("min_items_number_fi", "Min. number of items:", 10, min=1, max=100),
                ui.input_numeric("max_items_number_fi", "Max. number of items:", 10, min=1, max=100),
                full_screen=True,
            ),
            
            ui.input_task_button("confirm_button_fi", "Confirm"), 
        ),
        
        ui.accordion_panel(
            f"Association Rules",
            ui.card(
                ui.card_header("Info"),
                ui.p(
                    f"Number of rules: {number_of_rules}", ui.br(),
                    f"Selected rules: {selected_r}", ui.br()),
                full_screen=True,
            ),
                        
            ui.card(
                ui.card_header("Find association rules"),
                ui.p(ui.input_slider("minsupp_slider_ar", "Minimal support:", 0.1, 100, 2, step=5, post="%")),
                ui.p(ui.input_slider("minconf_slider_ar", "Minimal confidence:", 0.1, 100, 2, step=1, post="%")),
                ui.p(ui.input_slider("max_rules_slider_ar", "Max. number of rules:", 10, 100000, 10000)),
                full_screen=True,
            ),
            
            ui.card(   
                ui.card_header("Filter by Antecedent"),
                ui.input_text("containing_text_ant_ar", "Contains: "),
                ui.input_numeric("min_items_number_ar_ant", "Min. number of items:", 10, min=1, max=100),
                ui.input_numeric("max_items_number_ar_ant", "Max. number of items:", 10, min=1, max=100),
                full_screen=True,
            ),
            
            ui.card(   
                ui.card_header("Filter by Consequent"),
                ui.input_text("containing_text_con_ar", "Contains: "),
                ui.input_numeric("min_items_number_ar_con", "Min. number of items:", 10, min=1, max=100),
                ui.input_numeric("max_items_number_ar_con", "Max. number of items:", 10, min=1, max=100),
                full_screen=True,
            ),
            
            ui.input_task_button("confirm_button_ar", "Confirm"), 
        )
    ]
    
def sidebar_text():
    return (
        ui.accordion(*make_panels(), id="acc_frequent_itemsets", multiple=True),
    )
 
#  sf = False
    
#UI    
app_ui = ui.page_sidebar(
    ui.sidebar(sidebar_text(), width=320),  
    theme.darkly(),
    ui.download_button("downloadData", "Download foodmart.csv", class_="btn-primary"), ui.br(),
    ui.output_table("summary"),
    ui.output_text("find_frequent_itemsets"),
    title="Association Rule Induction",
    id = "main_view",
)


#SERVER
def server(input: Inputs, output: Outputs, session: Session):
    @render.download()
    def downloadData():
        path = os.path.join(os.path.dirname(__file__), "foodmart.csv")
        return path
    
    @reactive.calc
    def parsed_file():
        global file_name
        if input.checkbox_samplefile():
            file_name = "foodmart.csv"
            return pd.read_csv("foodmart.csv")
        else:    
            file: list[FileInfo] | None = input.file1()
            if file is None:
                return pd.DataFrame()
            file_name = pd.read_csv(file[0]["name"])
            return pd.read_csv(file[0]["datapath"])
        
    @reactive.calc
    def get_file_name():
        if input.checkbox_samplefile():
            return "foodmart.csv"
        else:    
            file: list[FileInfo] | None = input.file1()
            if file is None:
                return "Your file is empty"
            else:
                return file[0]["name"]
        
    @render.data_frame
    def data_table():
        df = parsed_file()
        if df.empty:
            return pd.DataFrame()
        return df
        
    @reactive.effect
    @reactive.event(input.checkbox_samplefile)
    def _():
        if not input.checkbox_samplefile():
            ui.insert_ui(
                ui.div(
                    {"id": "inserted_file_selector", "style": "max-width: 240px; text-align: center; margin-left: 15px; "}, 
                    ui.input_file("file1", "Upload CSV File", accept=[".csv"], multiple=False)
                ),
                selector="#card_start_cf",
                where="beforeEnd",
            )
        else:
            ui.remove_ui("#inserted_file_selector")
                    
    @reactive.effect
    @reactive.event(input.checkbox_of)
    def _():
        if input.checkbox_of():
            ui.insert_ui(
                ui.div(
                    {"id": "inserted_df"},
                    ui.h2(get_file_name()),
                    ui.output_data_frame("data_table"),
                ),
                selector="#main_view",
                where="beforeEnd",
            )
        else:
            ui.remove_ui("#inserted_df")        

    def find_fr_itemsets():
        pf = parsed_file()
        if pf.empty:
            return pd.DataFrame()
        if 'ID' in pf.columns:
            pf.drop(columns=['ID'], inplace=True)
        dataset = pf.values.tolist()
        dataset = [[item for item in row if isinstance(item, str)] for row in dataset]
        te = TransactionEncoder()
        te_ary = te.fit(dataset).transform(dataset)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        return apriori(df, min_support=0.0001, use_colnames=True)

    @render.data_frame
    def show_fr_itemsets():
        return pd.DataFrame(find_fr_itemsets())
    
    @reactive.effect
    @reactive.event(input.checkbox_fi)
    def _():
        if input.checkbox_fi():
            ui.insert_ui(
                ui.div(
                    {"id": "inserted_df_fi"},
                    ui.h2(f"Frequent Itemsets in {get_file_name()}"),
                    ui.output_data_frame("show_fr_itemsets"),
                ),
                selector="#main_view",
                where="beforeEnd",
            )
        else:
            ui.remove_ui("#inserted_df_fi")    
       
    @render.data_frame
    def show_assoc_rules():
        freq_itemsets = find_fr_itemsets()
        return pd.DataFrame(association_rules(freq_itemsets, metric="confidence", min_threshold=0.7))

    @reactive.effect
    @reactive.event(input.checkbox_ar)
    def _():
        if input.checkbox_ar():
            ui.insert_ui(
                ui.div(
                    {"id": "inserted_df_ar"},
                    ui.h2(f"Association Rules in {get_file_name()}"),
                    ui.output_data_frame("show_assoc_rules"),
                ),
                selector="#main_view",
                where="beforeEnd",
            )
        else:
            ui.remove_ui("#inserted_df_ar")           
        

    
app = App(app_ui, server)