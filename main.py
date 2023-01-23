import math
import matplotlib.pyplot as plt
import numpy as np


milestone = "Milestone 4"

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
        print("[SYSTEM Src Data: ",self.srcData)
        print("[SYSTEM temp Data: ",self.tempData)
        print("[SYSTEM] Output Data: ",self.outData)


    @staticmethod
    def plotPolygon(polygon1: list[tuple],polygon2=None) -> None:
        p = []
        # print(polygon1)
        for i in polygon1:
            p.append(i['coordinates'])
        # print(polygon1)
        x,x1 = [],[]
        y,y1 = [],[]
        for j in p:
            x=[]
            y=[]
            for i in j:
                x.append(i[0])
                y.append(i[1])
            plt.plot(x,y)
        if polygon2:
            for i in polygon2:
                x1.append(i[0])
                y1.append(i[1])

            plt.plot(x1,y1)


        plt.show()
        

    @staticmethod
    def formCoord(list: list) -> list[tuple]:
        result = []
        for i in range(0,len(list),2):
            result.append((int(list[i]),int(list[i+1])))
        return result   

    @staticmethod 
    def checkPolygonDistance(srcPolygon: list[tuple],tempPolygon: list[tuple]) -> bool:
        sl = []
        kl = []
        for i in range(len(srcPolygon)-1):
            sl.append(math.sqrt((srcPolygon[i][1] - srcPolygon[i+1][1])**2 + (srcPolygon[i][0]-srcPolygon[i+1][0])**2))
            kl.append(math.sqrt((tempPolygon[i][1] - tempPolygon[i+1][1])**2 + (tempPolygon[i][0]-tempPolygon[i+1][0])**2))
            
        return sorted(sl) == sorted(kl)

    @staticmethod
    def polygon_area(vertices: list[tuple]) -> float:
        vertices = vertices[:len(vertices)-1]
        n = len(vertices)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += vertices[i][0] * vertices[j][1]
            area -= vertices[j][0] * vertices[i][1]
        area = abs(area) / 2.0
        
        return area
    @staticmethod
    def pAngles(vertices: list[tuple])-> list[float]:
        angles = []
        n = len(vertices)
        for i in range(n):

            p1 = vertices[i]
            p2 = vertices[(i+1) % n]
            p3 = vertices[(i+2) % n]
            # print(p1,p2,p3)
            a = math.sqrt((p2[1]-p1[1])**2 + (p2[0]-p1[0])**2)
            b = math.sqrt((p3[1]-p2[1])**2 + (p3[0]-p2[0])**2)
            c = math.sqrt((p3[1]-p1[1])**2 + (p3[0]-p1[0])**2)
            try:
                angle = math.degrees(math.acos((a**2 + b**2 - c**2) / (2 * a * b)))
                # print(angle)
            except:
                pass
            # angles.append(angle)
        angles.sort()
        return angles

    @staticmethod
    def pointAngle(points: list[tuple]) -> list[float]:
        # l = np.array(l[:len(l)-1])
        points = np.array(points[:len(points)-1])
        points.shape = (-1, 2)
        a = points - np.roll(points, 1, axis=0)
        b = np.roll(a, -1, axis=0)

        alengths = np.linalg.norm(a, axis=1)
        blengths = np.linalg.norm(b, axis=1)
        crossproducts = np.cross(a, b) / alengths / blengths

        angles = np.arcsin(crossproducts)
        angles_degrees = angles / np.pi * 180
        return sorted(angles_degrees)
    
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
        # checkPolygon.plotPolygon(self.tempData)
        # print(self.tempData)

    def processData(self):
        c=0
        for sidx,sploygon in enumerate(self.srcData):
            for tidx,tploygon in enumerate(self.tempData):
                if sploygon['layer'] == tploygon['layer'] and sploygon['points'] == tploygon['points'] and checkPolygon.checkPolygonDistance(sploygon["coordinates"], tploygon['coordinates']) and (checkPolygon.pointAngle(sploygon['coordinates']) == checkPolygon.pointAngle(tploygon['coordinates'])) and (checkPolygon.polygon_area(sploygon['coordinates']) == checkPolygon.polygon_area(tploygon['coordinates'])):
                    
                        # print(f"[SYSTEM]: Polygon {sidx} and {tidx} are same")
                        # checkPolygon.plotPolygon(self.tempData,sploygon['coordinates'])
                        self.outData.append(sploygon)
                        break
                    
            
                            
        print(f"[SYSTEM]: Data Processed {len(self.outData)}")


    def outputData(self):
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