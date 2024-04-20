import pandas as pd
import shiny.experimental as x
from shiny import Inputs, Outputs, Session, module, render, ui, reactive
from app import *


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


@module.ui 
def make_panels():
    return [
        ui.accordion_panel(
            f"Start",
            ui.card( 
                ui.card_header("Upload file"),
                ui.input_file("file1", "Choose CSV File", accept=[".csv"], multiple=False),
                
                # ui.p(
                #     f"Number of itemstes: {number_of_itemsets}", ui.br(),
                #     f"Selected itemstes: {selected_i}", ui.br(), 
                #     f"Selected examples: {selected_e}", ui.br(),
                # #     full_screen=True,),
                ui.input_action_button("confirm_button_s", "Confirm"),
                ui.output_text("confirm_button_s_onclick"), ui.br(),
            ),
    
        ),
                
                
        # ui.accordion_panel(
        #     f"Frequent Itemsets",
        #     ui.card(
        #         ui.card_header("Info"),
        #         ui.p(
        #             f"Number of itemstes: {number_of_itemsets}", ui.br(),
        #             f"Selected itemstes: {selected_i}", ui.br(), 
        #             f"Selected examples: {selected_e}", ui.br(),
        #             full_screen=True,),
        #         ui.input_action_button("expand_all_button1_fi", "Expand all"),  
        #         ui.input_action_button("collapse_all_button1_fi", "Collapse all"),
        #     ),
                        
        #     ui.card(
        #         ui.card_header("Find itemsets"),
        #         ui.p(ui.input_slider("minsupp_slider_fi", "Minimal support:", 0.1, 100, 2, step=1, post="%")),
        #         ui.p(ui.input_slider("max_itemsets_slider_fi", "Max. number of itemsets:", 10, 100000, 10000)),
        #         full_screen=True,
        #     ),
            
        #     ui.card(   
        #         ui.card_header("Filter itemsets"),
        #         ui.input_text("containing_text_fi", "Contains: "),
        #         ui.input_numeric("min_items_number_fi", "Min. number of items:", 10, min=1, max=100),
        #         ui.input_numeric("max_items_number_fi", "Max. number of items:", 10, min=1, max=100),
        #     ),
            
        #     ui.input_task_button("confirm_button_fi", "Confirm"), 
        # ),
        
        # ui.accordion_panel(
        #     f"Association Rules",
        #     ui.card(
        #         ui.card_header("Info"),
        #         ui.p(
        #             f"Number of rules: {number_of_rules}", ui.br(),
        #             f"Selected rules: {selected_r}", ui.br(), 
        #             full_screen=True,),),
                        
        #     ui.card(
        #         ui.card_header("Find association rules"),
        #         ui.p(ui.input_slider("minsupp_slider_ar", "Minimal support:", 0.1, 100, 2, step=5, post="%")),
        #         ui.p(ui.input_slider("minconf_slider_ar", "Minimal confidence:", 0.1, 100, 2, step=1, post="%")),
        #         ui.p(ui.input_slider("max_rules_slider_ar", "Max. number of rules:", 10, 100000, 10000)),
        #         full_screen=True,
        #     ),
            
        #     ui.card(   
        #         ui.card_header("Filter by Antecedent"),
        #         ui.input_text("containing_text_ar", "Contains: "),
        #         ui.input_numeric("min_items_number_ar_ant", "Min. number of items:", 10, min=1, max=100),
        #         ui.input_numeric("max_items_number_ar_ant", "Max. number of items:", 10, min=1, max=100),
        #     ),
            
        #     ui.card(   
        #         ui.card_header("Filter by Consequent"),
        #         ui.input_text("containing_text_ar", "Contains: "),
        #         ui.input_numeric("min_items_number_ar_con", "Min. number of items:", 10, min=1, max=100),
        #         ui.input_numeric("max_items_number_ar_con", "Max. number of items:", 10, min=1, max=100),
        #     ),
            
        #     ui.input_task_button("confirm_button_ar", "Confirm"), 
        # )
    ]
       
@module.ui       
def sidebar_text():
    return (
        ui.accordion(*make_panels("make_panels"), id="acc_frequent_itemsets", multiple=True),
    )
    
