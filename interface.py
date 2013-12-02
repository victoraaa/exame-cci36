from Tkinter import Tk, Frame, BOTH


class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")   
         
        self.parent = parent
        self.initUI()
    
    def initUI(self):
      
        self.parent.title("Image Comparison")
        self.pack(fill=BOTH, expand=1)

        print self.size()
        print self.parent.size()
        
    def center_window(self):
        
        pass

def main():
  
    root = Tk()
    root.geometry("250x150+300+300")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  