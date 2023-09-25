import tkinter as tk
from Trie import Trie as ASA

class GUI(ASA):
    def __init__(self, master):
        self.master = master
        master.title("Simple Autocomplete")
        self.__startup()
        self.__setup_Arrow_Interaction()
        self.__create_widgets()

    def __startup(self):
        '''
        create the Trie structure
        '''
        # Execute startup command here
        print("Building Trie...\n")
        self.instance = ASA()
        self.Trie = self.instance.buildTrie()
        print("Done!\n")

        # create an empty array that holds the words that are referenced when the user's sentence is being created
        self.ResultWords = [""] * 10

    def __setup_Arrow_Interaction(self):
        ''' Function that handles the creation of the funciton binding that allows for the keyboard driven GUI interactions '''
        self.master.bind('<Left>', lambda event: self.__select_button(self.__get_current_button(), "left"))
        self.master.bind('<Right>', lambda event: self.__select_button(self.__get_current_button(), "right"))
        self.master.bind('<Up>', lambda event: self.__select_button(self.__get_current_button(), "up"))
        self.master.bind('<Down>', lambda event: self.__select_button(self.__get_current_button(), "down"))
        
        # bind enter key to click selected button
        self.master.bind('<Return>', lambda event: self.__click_button())

    def __buttonClick(self,letter):
        ''' Callback function for the letters of the keyboard '''
        self.text_input.insert('end',letter.lower())
        self.__execute_command()

    def __DelChars(self):
        ''' Callback function for the delete key -- removes the last character from the search box '''
        self.text_input.delete('end-2c','end-1c')
        self.__execute_command()

    def __toSentenceClick(self, wordIndex:int) -> None:
        ''' Take the word in the button selected by the user and add it to the text box that contains the sentence'''
        self.text_output.config(state="normal")
        self.text_output.insert('end',self.ResultWords[wordIndex]+" ")
        self.text_output.config(state="disabled")
        # here is where the implementation would be done to query the NN and get the predictions for the word that might come up next

    def __addUserWord(self) -> None:
        ''' 
        Enter the word a user is typing as it is written
        '''
        self.text_output.config(state="normal")
        self.text_output.insert('end',self.text_input.get("1.0","end-1c")+" ")
        self.text_output.config(state="disabled")

    def __create_widgets(self):
        '''Create the text boxes and keyboards that represent the interaction with the GUI'''
        # First text area that executes a command every time a letter is written
        self.text_input = tk.Text(self.master, height=1, width=10)
        self.text_input.grid(row = 0, column= 0, padx = 1, pady = 10)

        # Second text area that cannot be written into by the user - this will hold the sentence the user is writing using the tool
        OBW = 100
        self.text_output = tk.Text(self.master, height=20, width=OBW)
        self.text_output.grid(row = 0, column= 1, padx = 20, pady = 20, columnspan=OBW, rowspan=10)
        self.text_output.config(state="disabled")

        # 10 buttons that represent the options the user has to add to the statement
        self.ResultButtons = []
        for i in range(10):
            wordChoiceButton = tk.Button(self.master, text=self.ResultWords[i], width=6, command=lambda buttonIndex=i: self.__toSentenceClick(buttonIndex))
            # set the button's position on the grid
            wordChoiceButton.grid(row=1+i, column=12, padx=25, pady=5)
            self.ResultButtons.append(wordChoiceButton)

        clearBoxButton = tk.Button(self.master, text="Clear", padx=20, command=lambda: self.__deleteSentence())
        clearBoxButton.grid(row = 0, column=5, pady=5, columnspan=3)

        addWordButton = tk.Button(self.master, text="Add input", padx=20, command=lambda: self.__addUserWord())
        addWordButton.grid(row = 0, column=1, pady=5, columnspan=3)

        # buttons for the keyboard
        button_labels = [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["Z", "X", "C", "V", "B", "N", "Ñ", "M"],
            ["Á", "Í", "É", "Ó", "Ú", "Del"]
            ]

        # store the keyboard layout for other functions
        self.Keyboard_Layout = button_labels

        # store the list of buttons as part of the app data -- makes it easier to implement the arrow key implementation
        self.buttonList = []

        # create a list that will associate the flattened button array with the positions of the letters in the keyboard layout
        self.Flattened_Keyboard = []
        c = 0

        # create a loop to create the buttons and add them to the window
        for row in range(len(button_labels)):
            for col in range(len(button_labels[row])):
                letter = button_labels[row][col]

                self.Flattened_Keyboard.append((c,letter,(row,col)))

                if letter == "Del":
                    Del_button = tk.Button(self.master, text=button_labels[row][col], padx=15,pady=15, command= lambda : self.__DelChars())

                    # append the button references as tuples that house both the pointer to the button and the item that the button represents on the keyboard
                    self.buttonList.append((Del_button,letter))

                    # add the delete button to the grid
                    Del_button.grid(row=row+12, column=col, padx=5, pady=5)
                else:        
                    # create a button with the corresponding label
                    thisButton = tk.Button(self.master, text=button_labels[row][col], padx=15,pady=15, command=lambda letter=letter: self.__buttonClick(letter))
                    self.buttonList.append((thisButton,letter))

                    # set the button's position on the grid
                    thisButton.grid(row=row+12, column=col, padx=5, pady=5)
                
                c += 1
        
        self.buttonList[0][0].focus_set()

    def __select_button(self, current_Letter, direction):
        ''' function that moves the focus of the buttons around based off of the users input '''
        # we know that the structure of the keyboard follows a grid with the following layout:
        # ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        # ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
        # ["Z", "X", "C", "V", "B", "N", "Ñ", "M"],
        # ["Á", "Í", "É", "Ó", "Ú", "Del"]

        # i know what the current letter is because it is captures in the 1st index of the current_button input 

        for f in self.Flattened_Keyboard:
            if f[1] == current_Letter:
                focus_coordinates = f[2]
        
        # associated the directionality to the button coordinates
        if direction == "left":
            # decrease second element of coordinate by one (if possible)
            if focus_coordinates[1] > 0:
                new_y = focus_coordinates[1] - 1
                new_coordinates = (focus_coordinates[0], new_y)
            else:
                return

        elif direction == "right":
            # increase second element of coordinate by one (if possible)
            rowLim = len(self.Keyboard_Layout[focus_coordinates[0]])
            if focus_coordinates[1] < rowLim-1:
                new_y = focus_coordinates[1] + 1
                new_coordinates = (focus_coordinates[0], new_y)
            else:
                return
            
        elif direction == "up":
            # decrease first element of coordinate by one (if possible)
            if focus_coordinates[0] > 0:
                new_x = focus_coordinates[0] - 1
                new_coordinates = (new_x, focus_coordinates[1])
            else:
                return
            
        elif direction == "down":
            # increase first element of coordinate by one (if possible)
            canGoDown = focus_coordinates[0] < 3 and current_Letter != "P" and current_Letter != "L" and current_Letter != "M" and current_Letter != "Ñ" and current_Letter != "Del"
            if canGoDown: # can hardcode this because i know the number of rows in the keyboard
                new_x = focus_coordinates[0] + 1
                new_coordinates = (new_x, focus_coordinates[1])
            else:
                return
            
        for f in self.Flattened_Keyboard:
            if f[2] == new_coordinates:
                new_Linear_Index = f[0]
        
        self.buttonList[new_Linear_Index][0].focus_set()
        

    def __get_current_button(self) -> str:
        '''Get the button that is currently has the focus'''
        returnButton = self.master.focus_get()
        for button in self.buttonList:
            if button[0] == returnButton:
                return(button[1])
    
    def __click_button(self):
        '''Invokes the command associated with the specific button'''
        focused_Button = self.master.focus_get()
        focused_Button.invoke()
                

    def __execute_command(self):
        # Execute command every time a letter is written in the first text area
        text = self.text_input.get("1.0", "end-1c")
        if text != "": # I dont want this stuff to run if there are no letters in the box
            WO = self.searchTrie(self.Trie,text)
            # loop through the output words and fill the output buttons
            for i in range(10):
                self.ResultWords[i] = WO[i]
                self.ResultButtons[i].config(text = WO[i])

        else:
            # if the input is empty, clear the sentence buttons
            for B in self.ResultButtons:
                B.config(text = "")

    def __deleteSentence(self):
        ''' 
        Function that allows the user to delete words in the text box one word at at a time
        TODO: Split this into two functions, one that deletes one word at a time, and one that clears the whole box
        
        '''
        self.text_output.config(state="normal")
        self.text_output.delete("1.0", "end")
        self.text_output.config(state="disabled")


    

root = tk.Tk()
app = GUI(root)
root.mainloop()
