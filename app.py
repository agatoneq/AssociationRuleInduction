from shinyswatch import theme
from shiny import App, Inputs, Outputs, Session, render, ui, reactive, module
from shiny.types import FileInfo
from modules import *
import asyncio
import random
from datetime import date
import io
import os
from typing import Any


from palmerpenguins import load_penguins

penguins = load_penguins()
    

#UI    
app_ui = ui.page_sidebar(
    ui.sidebar(sidebar_text("sidebar")),  
    theme.darkly(),
    ui.download_button("downloadData", "Download foodmart.csv", class_="btn-primary"), ui.br(),
    title="Association Rule Induction",
)


#SERVER

def server(input: Inputs, output: Outputs, session: Session):
    @render.download()
    def downloadData():
        path = os.path.join(os.path.dirname(__file__), "foodmart.csv")
        return path

    
    # @render.text()
    # @reactive.event(input.confirm_button_s)
    # def confirm_button_s_onclick():
    #     return f"{input.confirm_button_s()}"
    

    
    # @render.text()
    # @reactive.event(input.expand_all_button)
    # def expand_button_onclick():
    #     return f"{input.expand_all_button()}"
    
    # @render.text()
    # @reactive.event(input.collapse_all_button)
    # def collapse_button_onclick():
    #     return f"{input.collapse_all_button()}"
    

    

    
    
    #@render.text
    
app = App(app_ui, server)