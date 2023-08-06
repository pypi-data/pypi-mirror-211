import wx
import wx.glcanvas as glcanvas
import PyPalette
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

try:
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    from OpenGL.GLU import *
    haveOpenGL = True
except ImportError:
    haveOpenGL = False

#----------------------------------------------------------------------
cubeVertices = ((10,10,0),(200,0,0),(100,200,0),(10,300,0))
cubeVertices = ((100,100,0),(100,10,0),(100,200,0),(10,100,0))
cubeEdges = ((0,1),(0,2),(0,3),(1,2),(1,3))
width, height = 500, 400

class GeneralFrame(wx.Frame):
    """
    Class used for creating frames other than the main one
    """
    def __init__(self, title, parent):
       super(GeneralFrame, self).__init__(parent, title = title,size = (800,800),style=wx.DEFAULT_FRAME_STYLE) 

       #On a d'un côté la figure venant d'OPENGL pour permettre des interactions et de l'autre, la colorbar venant de Matplotlib

       self.Centre() 
       frame_sizer = wx.BoxSizer(wx.VERTICAL)
       
       #Partie Figure
       self.canvas2 = CubeCanvas(self)
       frame_sizer.Add(self.canvas2, 1, wx.EXPAND)
       #Partie Colorbar
       self.figure, ax = plt.subplots(figsize=(4, 0.5))
       self.figure.subplots_adjust(bottom=0.5)

       cmap = mpl.cm.RdYlGn
       norm = mpl.colors.Normalize(vmin=5, vmax=10)

       self.figure.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                     cax=ax, orientation='horizontal', label='Some Units')
       #cb = mpl.colorbar.ColorbarBase(ax, orientation='horizontal', cmap=colormap)
       self.canvas = FigureCanvas(self, -1, self.figure)
       

       frame_sizer.Add(self.canvas, 0,  wx.EXPAND)
       
       #ax1.axis('off')
       #frame_sizer.SetMinSize(frame_sizer.Size)
       self.SetSizer(frame_sizer)
       self.Fit()



class MyCanvasBase(glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1)
        self.init = False
        self.context = glcanvas.GLContext(self)

        self.lastx = self.x = 30
        self.lasty = self.y = 30
        self.size = None
        #self.SetSize(900,900)

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        self.Text = wx.StaticText( self, wx.ID_ANY, u"  Available Channels  ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Text.Wrap( -1 )

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)



    def OnSize(self, event):
        wx.CallAfter(self.DoSetViewport)
        event.Skip()


    def DoSetViewport(self):
        size = self.size = self.GetClientSize()
        self.SetCurrent(self.context)
        glViewport(0, 0, size.width, size.height)


    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()


    def OnMouseDown(self, evt):
        self.CaptureMouse()
        self.x, self.y = self.lastx, self.lasty = evt.GetPosition()


    def OnMouseUp(self, evt):
        self.ReleaseMouse()


    def OnMouseMotion(self, evt):
        self.x, self.y = evt.GetPosition()
        #Procedure de transformations des coordonnées pour obtenir celles liées au réseau de base
        self.Coordi=[self.x,self.y]
        self.Coordi=self.UpdCoordinates()
        Round_Coord=[round(self.Coordi[0], 2),round(self.Coordi[1], 2)]
        self.Text.SetLabelText("x : %s ,y: %s" % (Round_Coord[0],Round_Coord[1]))
        if evt.Dragging() and evt.LeftIsDown():
            self.lastx, self.lasty = self.x, self.y

            self.Refresh(False)
    #Fonction générique pour passer de coordonnées pixels à coordonnées réelles du réseau
    def UpdCoordinates(self):

        SizMax=[]
        SizMax.append(self.BestVirtualSize.Width)
        SizMax.append(self.BestVirtualSize.Height)
        #On inverse coordonnée Y vu qu'elle est inversée de base
        self.Coordi[1]=self.BestVirtualSize.Height-self.Coordi[1]
        #Il faut réaliser à présenter différentes étapes de transformation inverse vis-à-vis de la mise en place du réseau
        LocCoord=[0.0,0.0]
        for i in range(2):
            self.Coordi[i]=self.Coordi[i]/SizMax[i]
            LocCoord[i]=self.MinCoord[i]+(self.NewCoordMin[i]-self.Coordi[i])/(self.NewCoordMax[i]-self.NewCoordMin[i])*(self.MinCoord[i]-self.MaxCoord[i])
        test=1
        return MParam
class CubeCanvas(MyCanvasBase):
    

    #Procédure pour créer le réseau : on doit conserver les proportions dans l'affichage final
    def wireCube(self):
        Coord=[]
        Coord.append([])
        Coord.append([])
        Coord.append([])
        self.MaxCoord=[]
        self.MinCoord=[]
        MaxLocCoord=[0.0,0.0,0.0]
        MinLocCoord=[100000.0,100000.0,100000.0]
        self.NewCoordMax=[0.0,0.0,0.0]
        self.NewCoordMin=[100000.0,100000.0,100000.0]
        DeltaPlace=[0,0,1]
        Delta=[]
        SizeMax=[]
        Bords=0.05
        Nodes_Params=[10,40,20,50]
        MParam=[0,0]
        MParam[0]=min(Nodes_Params)
        MParam[1]=max(Nodes_Params)
        Norm_Param=[]
        Param_Color=[]
        self.mypal.nb,self.mypal.values,self.mypal._segmentdata,self.mypal.colorsflt=self.mypal.export_palette_matplotlib_new('RdYlGn')
        for Param in Nodes_Params:
            Loc=(Param-MParam[0])/(MParam[1]-MParam[0])
            Norm_Param.append(Loc)
            #Loc_Color=self.mypal.lookupcolor(Loc)
            Loc_Color=self.mypal.lookupcolorflt(Loc)
            Param_Color.append(Loc_Color)
        #Première étape : évaluer la taille disponible de la fenêtre
        SizMax=[]
        SizMax.append(self.BestVirtualSize.Width)
        SizMax.append(self.BestVirtualSize.Height)
        MinSize=min(SizMax)
        MaxSize=max(SizMax)
        RapportAspect=MinSize/MaxSize
        RapportAspect=1
        LMax1=RapportAspect*(1.0-2*Bords)
        Hmax1=RapportAspect*(1.0-2*Bords)
        SizMax.append(1.0)
        glBegin(GL_LINES)
        SizeMax.append(LMax1)
        SizeMax.append(Hmax1)
        SizeMax.append(1)
        #Seconde étape : évaluer les coordonnées maximales et minimales selon chaque AXE pour obtenir le plus grand différentiel à intégrer
        for cubeEdge in cubeEdges:
            for cubeVertex in cubeEdge:
                for i in range(3):
                    Coord[i].append(cubeVertices[cubeVertex][i])     

        for Loc_Cord in Coord:
            self.MaxCoord.append(max(Loc_Cord))
            self.MinCoord.append(min(Loc_Cord))
            DeltaLoc=max(Loc_Cord)-min(Loc_Cord)
            Delta.append(DeltaLoc)
        Delta_Max=max(Delta)
        #Troisième étape : on va donc bien exprimer les deux axes pour conserver proportions
        test=1
        NewVertiList=[]
        for cubeVertex in cubeVertices:
            loc_curb=list(cubeVertex)
            for i in range(2):
                loc_curb[i]=(loc_curb[i]-self.MinCoord[i])/Delta_Max
                loc_curb[i]=loc_curb[i]*SizeMax[i]*MinSize/SizMax[i]
                if(loc_curb[i]>MaxLocCoord[i]):
                    MaxLocCoord[i]=loc_curb[i]
                if(loc_curb[i]<MinLocCoord[i]):
                    MinLocCoord[i]=loc_curb[i]
            test=1
        #On évalue la place disponible pour centrer le réseau selon le CG
        for i in range(2):
            DeltaPlace[i]=0.5-(MaxLocCoord[i]+MinLocCoord[i])/2
        #Quatrième étape, on va d'abord récupérer les coordonnées extrêmes afin de recentrer le réseau
        for cubeVertex in cubeVertices:
            loc_curb=list(cubeVertex)
            for i in range(2):
                loc_curb[i]=(loc_curb[i]-self.MinCoord[i])/Delta_Max
                loc_curb[i]=loc_curb[i]*SizeMax[i]*MinSize/SizMax[i]+DeltaPlace[i]
                if(loc_curb[i]>self.NewCoordMax[i]):
                    self.NewCoordMax[i]=loc_curb[i]
                if(loc_curb[i]<self.NewCoordMin[i]):
                    self.NewCoordMin[i]=loc_curb[i]
                test=1
            New_Tupl=tuple(loc_curb)
            NewVertiList.append(New_Tupl)
            test=1
        for cubeEdge in cubeEdges:
            for cubeVertex in cubeEdge:
                glColor3f(0.1,1.0,0.0)
                glVertex3dv(NewVertiList[cubeVertex])
            
        glEnd()

        #glBegin(GL_POINTS)
        i=0
        for cubeVertex in NewVertiList:
            #glColor3f(0.1,0.0,1.0)
            #glColor3f(Param_Color[i][0],Param_Color[i][1],Param_Color[i][2])
            glVertex3dv(cubeVertex)
            i=i+1
        glEnd()  
        temp_value=0.2
        #glBegin(GL_QUADS)
        #glVertex2f(0,0)
        #glVertex2f(temp_value, 0)
        #glVertex2f(temp_value, 0.1)
        #glVertex2f(0,0.1)
        #glEnd()
        #cmap=plt.get_cmap('RdYlGn')
        # create dummy invisible image
        # (use the colormap you want to have on the colorbar)

        test=1
        return

    def refresh2d(self,width,height):
        #glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #glOrtho(0.0, width, 0.0, height, 0.0, 6.0)
        gluOrtho2D(0.0, 1.0,0.0,1.0)
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity()

    def draw_rect(self,x, y, width, height):
        glBegin(GL_QUADS)                                  # start drawing a rectangle
        glVertex2f(x, y)                                   # bottom left point
        glVertex2f(x + width, y)                           # bottom right point
        glVertex2f(x + width, y + height)                  # top right point
        glVertex2f(x, y + height)                          # top left point
        glEnd()  
    
    def InitGL(self):
        # set viewing projection
        #glMatrixMode(GL_PROJECTION)
        #glFrustum(-1, 1, -1,1, 1.0, 3.0)
        t=1
        # position viewer
        #glMatrixMode(GL_MODELVIEW)
        #glTranslatef(0.0, 0.0, -2.0)

        # position object
        #glRotatef(self.y, 1.0, 0.0, 0.0)
        #glRotatef(self.x, 0.0, 1.0, 0.0)
        glPointSize(5)
        glEnable(GL_POINT_SMOOTH)

        self.mypal=PyPalette.wolfpalette(None,"Palette of colors")
        #self.mypal.default16()
        test=1
        """
        fig, ax = plt.subplots(figsize=(6, 1))
        fig.subplots_adjust(bottom=0.5)

        cmap = mpl.cm.cool
        norm = mpl.colors.Normalize(vmin=5, vmax=10)

        fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                     cax=ax, orientation='horizontal', label='Some Units')
        plt.show()
        """
        test=1
    def OnDraw(self):
        # clear color and depth buffers
        glClearColor(1,1,1,0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #glClearColor(0,0,1,0)
        glLoadIdentity()
        self.refresh2d(width,height) 
        glColor3f(0.0, 0.0, 0.0) 
        #self.draw_rect(10, 10, 200, 100) 
        self.MParam=self.wireCube()

        #glTranslatef(0.0, 0.0, -5)


        self.SwapBuffers()




#----------------------------------------------------------------------



app = wx.App(False)
if not haveOpenGL:
    wx.MessageBox('This sample requires the PyOpenGL package.', 'Sorry')
else:
    #frm = wx.Frame(None, title='GLCanvas Sample',size=(500,500))
    #canvas = CubeCanvas(frm)
    title='Test'
    frm=GeneralFrame(title,None)
    frm.Show()
app.MainLoop()