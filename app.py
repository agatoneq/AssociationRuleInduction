from shinyswatch import theme
from shiny import App, Inputs, Outputs, Session, render, ui, reactive
from palmerpenguins import load_penguins

penguins = load_penguins()
number_of_itemsets = 0
selected_i = 0
selected_e = 0



def custom_value_transform(value):
    if value <= 1:
        return value * 0.2
    else:
        return (value - 1) * 2 + 0.2

slider_value=0

def make_items():
    return [
        ui.accordion_panel(f"Section {letter}", f"Some narrative for section {letter}")
        for letter in "ABCDE"
    ]
       
        
def sidebar_text():
    return (
        ui.accordion(ui.accordion_panel(f"Section letter", 
                                        ui.card(
        ui.card_header("Info"),
        ui.p(
            f"Number of itemstes: {number_of_itemsets}", ui.br(),
            f"Selected itemstes: {selected_i}", ui.br(), 
            f"Selected examples: {selected_e}", ui.br(),
        full_screen=True,),
    ui.input_action_button("expand_all_button1", "Expand all"),  
    ui.input_action_button("collapse_all_button1", "Collapse all"),
    ),
                                        ), 
                     
                     
                     
                     id="acc_single", multiple=True),
    
    
    ui.card(
        ui.card_header("Find itemsets"),
        ui.p(ui.input_slider("minsupp_slider", "Minimal support:", 0, 100, 2, step=slider_value, post="%")),
        ui.p(ui.input_slider("max_itemsets_slider", "Max. number of itemsets:", 10, 100000, 10000)),
        full_screen=True,
    ),
    
    ui.card(   
        ui.card_header("Filter itemsets"),
        ui.input_text("containing_text", "Contains: "),
        ui.input_numeric("min_items_number", "Min. number of items:", 10, min=1, max=100),
        ui.input_numeric("max_items_number", "Max. number of items:", 10, min=1, max=100),
        ),
    
    ui.input_task_button("confirm_button", "Confirm"),
    )
    
    
app_ui = ui.page_sidebar(
    ui.sidebar(sidebar_text(), position="top", width=320),  
    theme.darkly(),
    ui.output_data_frame("penguins_df"),   
    title="Association Rule Induction",
)


def server(input, output, session):
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