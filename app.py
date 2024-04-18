from shinyswatch import theme
from shiny import App, render, ui, reactive

from palmerpenguins import load_penguins

penguins = load_penguins()
ddi =3




def sidebar_text():
    return (
    "Info about your data:",
    "Number of itemstes: ",
     ui.output_text("2"),
    "selected itemstes: ", 
     ui.output_text("3"),
    "Selected examples: ",
    ui.output_text("txt"),
    
    
    "Find itemsets: ",
    ui.input_slider("minsupp_slider", "Minimal support:", 0, 100, 50),  
    ui.input_slider("max_itemsets_slider", "Max. number of itemsets:", 0, 100, 50),  
    
    
    "Filter itemsets",
    "Contains: ",
    "Min. number of items: ",
    "Max. number of items: ",
    )
    
    
app_ui = ui.page_sidebar(
    ui.sidebar(sidebar_text(), position="top"),  
    theme.darkly(),
    #ui.sidebar(),
    #ui.page_opts(title="Hello shinyswatch theme"),
    
#     "Main content",

     # ui.h2("Palmer Penguins"),
    
    ui.output_data_frame("penguins_df"),   
    title="Association Rule Induction",
)

def server(input, output, session):
    pass
    #@render.text
    
    @render.data_frame  
    def penguins_df():
        return render.DataGrid(penguins)
    
    
  #  @render.text
    def com(str):
        count = 0
        for w in str:
            if w == ",":
                count += 1
        return count
    
    @render.text
    def txt():
        text="subject,trial,condition,sample,Fp1,AF7,AF3,F1,F3,F5,F7,FT7,FC5,FC3,FC1,C1,C3,C5,T7,TP7,CP5,CP3,CP1,P1,P3,P5,P7,P9,PO7,PO3,O1,Iz,Oz,POz,Pz,CPz,Fpz,Fp2,AF8,AF4,AFz,Fz,F2,F4,F6,F8,FT8,FC6,FC4,FC2,FCz,Cz,C2,C4,C6,T8,TP8,CP6,CP4,CP2,P2,P4,P6,P8,P10,PO8,PO4,O2,VEOa,VEOb,HEOL,HEOR,Nose,TP10"
        return com(text)+1
        #return f"n*2 is {input.n() * 2}"
    
    
app = App(app_ui, server)
