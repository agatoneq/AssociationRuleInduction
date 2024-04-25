from shiny import App, Inputs, Outputs, Session, render, ui, reactive
from shinyswatch import theme
from shiny.types import FileInfo
import os
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules    
    
#UI functions
def make_panels():
    return [
        ui.accordion_panel(
            f"Start",
            ui.card( 
                ui.card_header("Initial info"),
                ui.input_checkbox("checkbox_initial_info", "Display initial information from the author", True),
                id="card_start_initinfo",
                full_screen=True,
            ),
            ui.card( 
                ui.card_header("Choose file"),
                ui.input_checkbox("checkbox_samplefile", "Use sample file", True),
                id="card_start_cf",
                full_screen=True,
            ),
        ),        
                
        ui.accordion_panel(
            f"Frequent Itemsets",
            ui.card(
                ui.card_header("Find itemsets"),
                ui.input_slider("minsupp_slider_fi", "Minimal support:", 0.01, 100, 2, step=1, post="%"),
                full_screen=True,
            ),
            
            ui.card(   
                ui.card_header("Filter itemsets"),
                ui.input_text("containing_text_fi", "Contains: "),
                ui.input_numeric("min_values_per_itemset", "Min. number of items:", 1, min=1, max=100),
                ui.input_numeric("max_values_per_itemset", "Max. number of items:", 5, min=1, max=100),
                full_screen=True,
            ),
        ),
        
        ui.accordion_panel(
            f"Association Rules",
            ui.card(
                ui.card_header("Find association rules"),
                ui.p(ui.input_slider("minsupp_slider_ar", "Minimal support:", 0.1, 100, 2, step=5, post="%")),
                ui.p(ui.input_slider("minconf_slider_ar", "Minimal confidence:", 0.1, 100, 2, step=1, post="%")),
                full_screen=True,
            ),
            
            ui.card(   
                ui.card_header("Filter by Antecedent"),
                ui.input_text("containing_text_ant_ar", "Contains: "),
                ui.input_numeric("min_items_number_ar_ant", "Min. number of items:", 1, min=1, max=100),
                ui.input_numeric("max_items_number_ar_ant", "Max. number of items:", 5, min=1),
                full_screen=True,
            ),
            
            ui.card(   
                ui.card_header("Filter by Consequent"),
                ui.input_text("containing_text_con_ar", "Contains: "),
                ui.input_numeric("min_items_number_ar_con", "Min. number of items:", 1, min=1, max=100),
                ui.input_numeric("max_items_number_ar_con", "Max. number of items:", 5, min=1),
                full_screen=True,
            ),
        )
    ]
    
def sidebar_text():
    return (
        ui.accordion(*make_panels(), id="acc_frequent_itemsets", multiple=True),
    )
    
#UI    
app_ui = ui.page_sidebar(
    ui.sidebar(sidebar_text(), width=320),  
    theme.darkly(),
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
            
    @reactive.calc
    def get_file_size():
        file_name = get_file_name()
        if get_file_name()=="Your file is empty":
            file_size = 0
        else:
            file_size = os.path.getsize(file_name)
        return(file_size)
        
    @render.data_frame
    def data_table():
        df = parsed_file()
        if df.empty:
            return pd.DataFrame()
        return df
        
    @reactive.effect
    @reactive.event(input.checkbox_samplefile)
    def _():
        ui.remove_ui("#inserted_of")
        ui.remove_ui("#inserted_fi")  
        ui.remove_ui("#inserted_ar")   
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
        ui.remove_ui("#inserted_of")
        if input.checkbox_of():
            ui.insert_ui(
                ui.div(
                    {"id": "inserted_of"},
                    ui.card(
                        ui.h2(get_file_name()),
                        ui.output_data_frame("data_table"),
                        id="card_of",
                        full_screen=True,
                    )
                ),
                selector="#main_view",
                where="beforeEnd",
            )
            ui.update_checkbox("checkbox_fi", value=False)
            ui.update_checkbox("checkbox_ar", value=False)

    @reactive.event(input.minsupp_slider_fi)
    def change_supp_fi():
        min_supp_fi = input.minsupp_slider_fi._value/100
        return min_supp_fi   
    
    
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
        return apriori(df, min_support=change_supp_fi(), use_colnames=True)
        
    @render.data_frame
    def show_fr_itemsets():
        keyword = input.containing_text_fi().lower()
        min_values_per_itemset = input.min_values_per_itemset()
        max_values_per_itemset = input.max_values_per_itemset()
        fr_itemsets = find_fr_itemsets()
        if fr_itemsets.empty:
            return pd.DataFrame()
        else:
            fr_itemsets_filtered = fr_itemsets[fr_itemsets.apply(lambda row: min_values_per_itemset <= len(row['itemsets']) <= max_values_per_itemset, axis=1)]
            return fr_itemsets_filtered[fr_itemsets_filtered.astype(str).apply(lambda row: keyword in ''.join(row['itemsets']).lower(), axis=1)]

    @reactive.effect
    @reactive.event(input.checkbox_fi)
    def _():
        ui.remove_ui("#inserted_of")
        ui.remove_ui("#inserted_fi")  
        ui.remove_ui("#inserted_ar")    
        if input.checkbox_fi():
            ui.insert_ui(
                ui.div(
                    {"id": "inserted_fi"},
                    ui.card(
                        ui.h2(f"Frequent Itemsets in {get_file_name()}"),
                        ui.output_data_frame("show_fr_itemsets"),
                        id="card_of",
                        full_screen=True,
                    ),
                ),
                selector="#main_view",
                where="beforeEnd",
            )
            ui.update_checkbox("checkbox_of", value=False)
            ui.update_checkbox("checkbox_ar", value=False)
   
    @reactive.event(input.minsupp_slider_ar)
    def change_supp_ar():
        min_supp_fi = input.minsupp_slider_ar._value/100
        return min_supp_fi  
    
    @reactive.event(input.minconf_slider_ar)
    def change_conf_ar():
        min_supp_fi = input.minconf_slider_ar._value/100
        return min_supp_fi  
    
    @render.data_frame
    def show_assoc_rules():
        keyword_ant = input.containing_text_ant_ar().lower()
        keyword_con = input.containing_text_con_ar().lower()
        min_supp_ar = change_supp_ar()
        min_conf_ar = change_conf_ar()
        min_values_per_itemset_ant_ar = input.min_items_number_ar_ant()
        max_values_per_itemset_ant_ar = input.max_items_number_ar_ant()
        min_values_per_itemset_con_ar = input.min_items_number_ar_con()
        max_values_per_itemset_con_ar = input.max_items_number_ar_con()
        freq_itemsets = find_fr_itemsets()
        if freq_itemsets.empty:
            return pd.DataFrame()
        else:
            assoc_rules = association_rules(freq_itemsets, metric="confidence", min_threshold=min_conf_ar)
            assoc_rules_filtered = assoc_rules[assoc_rules['support'] >= min_supp_ar]
            assoc_rules_filtered_ant = assoc_rules_filtered[assoc_rules_filtered['antecedents'].apply(lambda x: min_values_per_itemset_ant_ar <= len(x) <= max_values_per_itemset_ant_ar)]
            assoc_rules_filtered_con = assoc_rules_filtered_ant[assoc_rules_filtered_ant['consequents'].apply(lambda x: min_values_per_itemset_con_ar <= len(x) <= max_values_per_itemset_con_ar)]
            assoc_rules_filtered_keywords = assoc_rules_filtered_con[
                assoc_rules_filtered_con.astype(str).apply(lambda row: keyword_ant in ''.join(row['antecedents']).lower(), axis=1)]
            assoc_rules_filtered_keywords = assoc_rules_filtered_keywords[
                assoc_rules_filtered_keywords.astype(str).apply(lambda row: keyword_con in ''.join(row['consequents']).lower(), axis=1)]
            return pd.DataFrame(assoc_rules_filtered_keywords)

    @reactive.effect
    @reactive.event(input.checkbox_ar)
    def _():
        ui.remove_ui("#inserted_of")
        ui.remove_ui("#inserted_fi")  
        ui.remove_ui("#inserted_ar")  
        if input.checkbox_ar():
            ui.insert_ui(
                ui.div(
                    {"id": "inserted_ar"},
                    ui.card(
                        ui.h2(f"Association Rules in {get_file_name()}"),
                        ui.output_data_frame("show_assoc_rules"),
                        id="card_of",
                        full_screen=True,
                    ),
                ),
                selector="#main_view",
                where="beforeEnd",
            )  
            ui.update_checkbox("checkbox_fi", value=False)
            ui.update_checkbox("checkbox_of", value=False)      
    
    @render.text
    def show_info_ar():
        txt=f"File is too large. Displaying association rules is available for files up to 7KB."
        return txt
        
    @render.text
    def show_info_fi():
        txt=f"File is too large. Displaying frequent itemsets is available for files up to 47KB."
        return txt
                  
    @reactive.effect
    def _():
        ui.remove_ui("#inserted_card")
        ui.remove_ui("#inserted_checkbox_ar")
        ui.remove_ui("#inserted_checkbox_fi")
        ui.remove_ui("#inserted_info_ar")
        ui.remove_ui("#inserted_info_fi")
        if get_file_size() != 0:
            ui.insert_ui(
                ui.div(
                    {"id": "inserted_card"}, 
                    ui.card( 
                ui.card_header("Display options"),
                ui.input_checkbox("checkbox_of", "Show original file", False),
                id="card_start_do",
                full_screen=True,)
                ),
                selector="#card_start_cf",
                where="afterEnd",
            )
            if get_file_size() <= 7000:
                ui.insert_ui(
                    ui.div(
                        {"id": "inserted_checkbox_fi", "style": "max-width: 240px; margin-left: 15px; "}, 
                        ui.input_checkbox("checkbox_fi", "Show frequent itemsets", False)
                    ),
                    selector="#card_start_do",
                    where="beforeEnd",
                )
                ui.insert_ui(
                    ui.div(
                        {"id": "inserted_checkbox_ar", "style": "max-width: 240px; margin-left: 15px; "}, 
                        ui.input_checkbox("checkbox_ar", "Show association rules", False)
                    ),
                    selector="#card_start_do",
                    where="beforeEnd",
                )
                
            elif get_file_size() <= 47000 and get_file_size() > 7000:
                ui.remove_ui("#inserted_checkbox_ar")
                ui.insert_ui(
                    ui.div(
                        {"id": "inserted_checkbox_fi", "style": "max-width: 240px; margin-left: 15px; "}, 
                        ui.input_checkbox("checkbox_fi", "Show frequent itemsets", False)
                    ),
                    selector="#card_start_do",
                    where="beforeEnd",
                )
                ui.insert_ui(
                        ui.div(
                            {"id": "inserted_info_ar", "style": "max-width: 240px; margin-left: 15px; color: rgb(171, 38, 38);"}, 
                            ui.output_text("show_info_ar"),
                        ),
                        selector="#card_start_do",
                        where="beforeEnd",
                    )
                  
    @reactive.effect
    @reactive.event(input.checkbox_initial_info)
    def _():
        if input.checkbox_initial_info():
            ui.insert_ui(
                ui.div(
                    {"id": "inserted_card_initinfo"}, 
                    ui.card( 
                    ui.card_header("Let's get started! Check how you can use this program"),
                    ui.div(
                            {"style": "max-width: 240px;"}, 
                            ui.download_button("downloadData", "Download foodmart.csv", class_="btn-primary")
                        ),
                    id="card_initial_info",
                    full_screen=True,
                    )
                ),
                selector="#main_view",
                where="afterBegin",
            )
        else:
            ui.remove_ui("#inserted_card_initinfo")                      
                           
          
                  
app = App(app_ui, server)