from shinyswatch import theme
from shiny import App, Inputs, Outputs, Session, render, ui, reactive
from palmerpenguins import load_penguins

penguins = load_penguins()
number_of_itemsets = 0
selected_i = 0
selected_e = 0

number_of_rules = 0
selected_r = 0




#UI

def custom_value_transform(value):
    if value <= 1:
        return value * 0.2
    else:
        return (value - 1) * 2 + 0.2

slider_value=0

def make_panels():
    return [
        ui.accordion_panel(
            f"Frequent Itemsets",
            ui.card(
                ui.card_header("Info"),
                ui.p(
                    f"Number of itemstes: {number_of_itemsets}", ui.br(),
                    f"Selected itemstes: {selected_i}", ui.br(), 
                    f"Selected examples: {selected_e}", ui.br(),
                    full_screen=True,),
                ui.input_action_button("expand_all_button1_fi", "Expand all"),  
                ui.input_action_button("collapse_all_button1_fi", "Collapse all"),),
                        
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
                ),
            
            ui.input_task_button("confirm_button_fi", "Confirm"), 
            ),
        
        ui.accordion_panel(
            f"Association Rules",
            ui.card(
                ui.card_header("Info"),
                ui.p(
                    f"Number of rules: {number_of_rules}", ui.br(),
                    f"Selected rules: {selected_r}", ui.br(), 
                    full_screen=True,),),
                        
            ui.card(
                ui.card_header("Find association rules"),
                ui.p(ui.input_slider("minsupp_slider_ar", "Minimal support:", 0.1, 100, 2, step=5, post="%")),
                ui.p(ui.input_slider("minconf_slider_ar", "Minimal confidence:", 0.1, 100, 2, step=1, post="%")),
                ui.p(ui.input_slider("max_rules_slider_ar", "Max. number of rules:", 10, 100000, 10000)),
                full_screen=True,
            ),
            
            ui.card(   
                ui.card_header("Filter by Antecedent"),
                ui.input_text("containing_text_ar", "Contains: "),
                ui.input_numeric("min_items_number_ar_ant", "Min. number of items:", 10, min=1, max=100),
                ui.input_numeric("max_items_number_ar_ant", "Max. number of items:", 10, min=1, max=100),
                ),
            
            ui.card(   
                ui.card_header("Filter by Consequent"),
                ui.input_text("containing_text_ar", "Contains: "),
                ui.input_numeric("min_items_number_ar_con", "Min. number of items:", 10, min=1, max=100),
                ui.input_numeric("max_items_number_ar_con", "Max. number of items:", 10, min=1, max=100),
                ),
            
            ui.input_task_button("confirm_button_ar", "Confirm"), 
            )
    ]
       
        
def sidebar_text():
    return (
        ui.accordion(*make_panels(), id="acc_frequent_itemsets", multiple=True),
    )
    


#UI    
app_ui = ui.page_sidebar(
    ui.sidebar(sidebar_text(), position="top", width=320),  
    theme.darkly(),
    ui.output_data_frame("penguins_df"),   
    title="Association Rule Induction",
)








#SERVER

def server(input, output, session):
    @render.text()
    @render.data_frame  
    def penguins_df():
        return render.DataGrid(penguins)

    def com(str):
        count = 0
        for w in str:
            if w == ",":
                count += 1
        return count
    
    @render.text()
    @reactive.event(input.expand_all_button)
    def expand_button_onclick():
        return f"{input.expand_all_button()}"
    
    @render.text()
    @reactive.event(input.collapse_all_button)
    def collapse_button_onclick():
        return f"{input.collapse_all_button()}"
    
    #@render.text
    
app = App(app_ui, server)