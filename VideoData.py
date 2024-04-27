class LandMarks:
    def __init__(self, X1, Y1, X2, Y2):
        self.X1 = X1
        self.Y1 = Y1
        self.X2 = X2
        self.Y2 = Y2

    def displayInfo(self):
        print(f"""
              land Marks are :
                    X1 is  {self.X1}
                    Y1 is {self.Y1} 
                    X2 is {self.X2} 
                    Y2 is {self.Y2}""")


class VideoData:
    def __init__(self, fileName, EF_value, ED_value, ES_value, ED_frame, ES_frame, Split, ED_landMark, ES_landMark,
                 numberOfFrames,
                 ED_Frame_IMG, ES_Frame_IMG):
        self.fileName = fileName
        self.EF_value = EF_value
        self.ED_value = ED_value
        self.ES_value = ES_value
        self.ED_frame = ED_frame
        self.ES_frame = ES_frame
        self.Split = Split
        self.ED_landMark = ED_landMark
        self.ES_landMark = ES_landMark
        self.numberOfFrames = numberOfFrames
        self.ED_Frame_IMG = ED_Frame_IMG
        self.ES_Frame_IMG = ES_Frame_IMG

    def displayInfo(self):
        print(f"""
        Video Information:
              File Name is  {self.fileName}
              EF Value is {self.EF_value}
              ES Value is {self.ES_value}
              ED Value is {self.ED_value}
              ED Frame is {self.ED_frame}
              ES Frame is {self.ES_frame}
              Split is {self.Split}
              numberOfFrames is {self.numberOfFrames}""")
