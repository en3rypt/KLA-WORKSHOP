import math


milestone = "Milestone 7"

class checkPolygon:
    def __init__(self,srcPloygonPath,tempPloygonPath=None):
        self.sourcePath = srcPloygonPath
        self.tempPolygonPath = tempPloygonPath
        self.srcData=[]
        self.tempData=[]
        self.outData = []

    def display(self):
        print("[SYSTEM] Source Path: ",self.sourcePath)
        print("[SYSTEM] Temp Path: ",self.tempPolygonPath)
        # print("[SYSTEM Src Data: ",self.srcData)
        print("[SYSTEM temp Data: ",self.tempData)
        print("[SYSTEM] Output Data: ",self.outData)

    @staticmethod
    def formCoord(list):
        result = []
        for i in range(0,len(list),2):
            result.append((int(list[i]),int(list[i+1])))
        return result

    @staticmethod 
    def checkPolygon(srcPolygon,tempPolygon):
        sl = []
        kl = []
        for i in range(len(srcPolygon)-1):
            sl.append(math.sqrt((srcPolygon[i][1] - srcPolygon[i+1][1])**2 + (srcPolygon[i][0]-srcPolygon[i+1][0])**2))
            kl.append(math.sqrt((tempPolygon[i][1] - tempPolygon[i+1][1])**2 + (tempPolygon[i][0]-tempPolygon[i+1][0])**2))
            
        return sorted(sl) == sorted(kl)
        # if len(srcPolygon)!=len(tempPolygon):
        #     print(srcPolygon,tempPolygon)
        # for i in range(len(srcPolygon)-1):
        #     sd = math.sqrt((srcPolygon[i][1] - srcPolygon[i+1][1])**2 + (srcPolygon[i][0]-srcPolygon[i+1][0])**2)
        #     td = math.sqrt((tempPolygon[i][1] - tempPolygon[i+1][1])**2 + (tempPolygon[i][0]-tempPolygon[i+1][0])**2)
            
        #     if sd != td:
        #         return False
        # return True
    def loadtempData(self):
        pass

    def loadsrcData(self):
        with open(self.sourcePath, 'r') as f:
            srcData = f.readlines()
        srcData = srcData[8:]
        d = {"layer":None,"coordinates":[]}
        i = 0
        while i<len(srcData):
            if "layer" in srcData[i]:
                d['layer'] = srcData[i].strip('\n')
            elif 'xy' in srcData[i]:
                d['points'] = srcData[i].strip('\n').split(" ")[2]
                coordList = list(filter(None, srcData[i].strip('\n').split(" ")[3:]))
                d["coordinates"] = checkPolygon.formCoord(coordList)
                self.srcData.append(d)
                d = {"layer":None,"coordinates":[]}
            i+=1
        # print(self.srcData[:5])

    def loadData(self):
        self.loadsrcData()
        print("[SYSTEM]: Source Data Loaded")
        if self.tempPolygonPath:
            self.loadtempData()
            print("[SYSTEM]: Temp Data Loaded")
    def loadtempData(self):
        with open(self.tempPolygonPath, 'r') as f:
            tempData = f.readlines()
        tempData = tempData[8:]
        d = {"layer":None,"points":None,"coordinates":[]}
        i = 0
        while i<len(tempData):
            if "layer" in tempData[i]:
                d['layer'] = tempData[i].strip('\n')
            
            elif 'xy' in tempData[i]:
                d['points'] = tempData[i].strip('\n').split(" ")[2]
                coordList = list(filter(None, tempData[i].strip('\n').split(" ")[3:]))
                d["coordinates"] = checkPolygon.formCoord(coordList)
                self.tempData.append(d)
                d = {"layer":None,"points":None,"coordinates":[]}
            i+=1
        # print(self.tempData)
        
    def processData(self):
        c=0
        for sidx,sploygon in enumerate(self.srcData):
            for tidx,tploygon in enumerate(self.tempData):
                if sploygon['layer'] == tploygon['layer'] and sploygon['points'] == tploygon['points']:
                    if checkPolygon.checkPolygon(sploygon['coordinates'],tploygon['coordinates']):
                        # print(f"[SYSTEM]: Polygon {sidx} and {tidx} are same")
                        c+=1
                        self.outData.append(sploygon)
                    
            
                            
        # print(self.outData)
        print("[SYSTEM]: Data Processed")


    def outputData(self):
        # self.outData = self.srcData[:2]
        # f"Output/{milestone}/output.txt"
        with open(f"Output/{milestone}/output.txt", 'w+') as f:
            t= True
            for line in self.outData:
                if t:
                    f.write("boundary\n")
                    t = False
                else:
                    f.write("\nboundary\n")
                f.write(line['layer']+'\n')
                f.write("datatype 0\n")
                coord = f'xy  {len(line["coordinates"])} '
                for i in line["coordinates"]:
                    coord += f' {i[0]} {i[1]} '
                coord += '\n'
                f.write(coord)
                f.write("endel")
        print("[SYSTEM]: Output Data Generated")
    

# o = ,f'Milestones/{milestone}/POI.txt'
obj = checkPolygon(f'Milestones/{milestone}/Source.txt',f'Milestones/{milestone}/POI.txt')
obj.loadData()
obj.processData()
# obj.display()
obj.outputData()