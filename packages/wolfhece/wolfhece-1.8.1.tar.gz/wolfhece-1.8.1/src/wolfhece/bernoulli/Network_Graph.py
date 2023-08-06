from math import *
import wx
import wx.glcanvas as glcanvas
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import _load_bitmap
from matplotlib.figure import Figure

try:
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    from OpenGL.GLU import *
    haveOpenGL = True    
except ImportError:
    haveOpenGL = False

from ..PyPalette import wolfpalette

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

"""
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

"""
class CubeCanvas(MyCanvasBase):
    

    #Procédure pour créer le réseau : on doit conserver les proportions dans l'affichage final
    def DrawCircle(self,x,y,r,segments):
        Bords=0.1
        SizMax=[]
        SizMax.append(self.BestVirtualSize.Width)
        SizMax.append(self.BestVirtualSize.Height)
        MinSize=min(SizMax)
        MaxSize=max(SizMax)
        RapportAspect=1
        LMax1=RapportAspect*(1.0-2*Bords)
        Hmax1=RapportAspect*(1.0-2*Bords)
        SizMax.append(1.0)
        SizeMax=[]
        SizeMax.append(LMax1)
        SizeMax.append(Hmax1)
        SizeMax.append(1)
        angle=2.0*pi/float(segments)

        prevX=x
        prevY=y-r*SizeMax[1]*MinSize/SizMax[1]
        nb_seg=segments+1
        for i in range(nb_seg):
            newX=x+r*SizeMax[0]*MinSize/SizMax[0]*sin(angle*float(i))
            newY=y-r*SizeMax[1]*MinSize/SizMax[1]*cos(angle*float(i))
            glBegin(GL_TRIANGLES)
            glColor3f(0.0,0.5,0.0)
            glVertex3f(x,y,0.0)
            glVertex3f(prevX,prevY,0.0)
            glVertex3f(newX,newY,0.0)
            glEnd()
            prevX=newX
            prevY=newY
        return

    def refresh2d(self,width,height):
        #glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #glOrtho(0.0, width, 0.0, height, 0.0, 6.0)
        gluOrtho2D(0.0, 1.0,0.0,1.0)
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity()

    def draw_square(self,x, y, width):
        glBegin(GL_QUADS)  
        glColor3f(0.5,0.0,0.0)
        glVertex2f(x + width/2.0, y+width/2.0)                                   
        glVertex2f(x + width/2.0, y-width/2.0)                          
        glVertex2f(x - width/2.0, y-width/2.0)                 
        glVertex2f(x - width/2.0, y+width/2.0)                          
        glEnd()  
    
    def InitGL(self):

        t=1

        #glPointSize(5)
        #glEnable(GL_POINT_SMOOTH)

        self.mypal=wolfpalette(None,"Palette of colors")

        test=1

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
        x=0.5
        y=0.5
        r=0.3
        segments=300
        self.MParam=self.DrawCircle(x,y,r,segments)
        self.MParam2=self.draw_square(x,y,r)
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