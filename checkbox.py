import easygui as eg

question = "Select teams to exclude"
title = "Select teams"
listOfOptions = ['Atl','Buf','Car','Chi','Cin']

choice = eg.multchoicebox(question , title, listOfOptions)
print choice
