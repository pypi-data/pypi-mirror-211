# Code utilisé pour l'importation/lecture d'un fichier .vecz ou au contraire, l'écriture et/ou exportation de ce même fichier au format texte
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time
import array as arr
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import wx
import wx.grid as grid
import wx.glcanvas as glcanvas
import os.path
from itertools import count

from ..PyTranslate import _

try:
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    from OpenGL.GLU import *
except:
    msg=_('Error importing OpenGL library')
    msg+=_('   Python version : ' + sys.version)
    msg+=_('   Please check your version of opengl32.dll -- conflict may exist between different fils present on your desktop')
    raise Exception(msg)


cubeVertices = ((100,100,0),(100,10,0),(100,200,0),(10,100,0))
cubeEdges = ((0,1),(0,2),(0,3),(1,2),(1,3))
width, height = 500, 400
#Partie dédiée à la création d'une interface spatiale utilisable
class Window_Test(wx.Frame):
    #Partie Menu


    def __init__(self, *args, **kwargs):
        super(Window_Test, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):

        #Partie Menu

        menubar = wx.MenuBar()

        #Premier menu
        fileMenu = wx.Menu()
        NewNet=fileMenu.Append(wx.ID_NEW, '&New')
        menuOpen=fileMenu.Append(wx.ID_OPEN, '&Open','Open a file to edit')
        fileMenu.Append(wx.ID_SAVE, '&Save')
        fileMenu.AppendSeparator()
       
        imp = wx.Menu()
        self.Network0D=False
        NWoD=imp.Append(wx.ID_ANY, 'Import Network0D')
        #imp.Append(wx.ID_ANY, 'Import bookmarks...')
        #imp.Append(wx.ID_ANY, 'Import mail...')

        fileMenu.Append(wx.ID_ANY, 'I&mport', imp)

        #On associe les différents évènements liés à ces menus
        #Fermeture de l'application
        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+W')
        fileMenu.Append(qmi)

        self.Bind(wx.EVT_MENU, self.OnQuit, qmi)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        #Ouvrir réellement nouveau fichier

        menubar.Append(fileMenu, '&File')
        self.menubar=menubar
        self.SetMenuBar(self.menubar)
        #Ouvrir box pour ajouter nouveau jeu ou nouveau lien
        #On associe les différents évènements 

        #Partie Toolbar
        self.count = 5
        self.LocalNode =(0,0)
        self.toolbar = self.CreateToolBar()
        #tundo = self.toolbar.AddTool(wx.ID_UNDO, '',wx.Bitmap('D:\PIRARD_Thomas\exit8.png'))
        tundo = self.toolbar.AddTool(wx.ID_UNDO, '',wx.Bitmap('exit8.png'))
        tredo = self.toolbar.AddTool(wx.ID_REDO, '',wx.Bitmap('exit7.png'))
        self.toolbar.EnableTool(wx.ID_REDO, False)
        self.toolbar.AddSeparator()
        texit = self.toolbar.AddTool(wx.ID_EXIT, '', wx.Bitmap('exit3.png'))
        self.toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.OnQuit, texit)
        self.Bind(wx.EVT_TOOL, self.OnUndo, tundo)
        self.Bind(wx.EVT_TOOL, self.OnRedo, tredo)
        
        self.SetSize((600, 600))
        self.SetTitle('Network 0D')
        self.Centre()
        Click_Info=[]
        #Evènements pour la création et importation d'un réseau depuis un dossier fourni par l'utilisateur
        self.Bind(wx.EVT_TOOL, self.ImportNetwork, NWoD)

        #Evènements pour la création d'un nouveau réseau
        self.Bind(wx.EVT_TOOL, self.on_new_frame, NewNet)


    def OnUndo(self, e):
        if self.count > 1 and self.count <= 5:
            self.count = self.count - 1

        if self.count == 1:
            self.toolbar.EnableTool(wx.ID_UNDO, False)

        if self.count == 4:
            self.toolbar.EnableTool(wx.ID_REDO, True)

    def OnRedo(self, e):
        if self.count < 5 and self.count >= 1:
            self.count = self.count + 1

        if self.count == 5:
            self.toolbar.EnableTool(wx.ID_REDO, False)

        if self.count == 2:
            self.toolbar.EnableTool(wx.ID_UNDO, True)


    def OnQuit(self, e):
        self.Close()

    #Importation d'un réseau 0D sur base d'un fichier .vecz
    def ImportNetwork(self, e):
        #Recherche du fichier .vecz(structure géométrique) dans les dossiers de l'utilisateur

        dlg = wx.FileDialog(self, "Choose the .vecz file",
                           defaultDir = "",
                           defaultFile = "",
                           wildcard = "*")

        if dlg.ShowModal() == wx.ID_OK:

            #Ajout d'éléments supplémentaires de menu liés à la mise en place d'un réseau 0D
            #Menu d'ajout d'éléments
            if(not(self.Network0D)):
                AddMenu = wx.Menu()
                self.Network0D=True
                NewNode=AddMenu.Append(wx.ID_ANY, '&New Node')
                NewEdge=AddMenu.Append(wx.ID_ANY, '&New Edge')
                AddMenu.AppendSeparator()
                Edition=AddMenu.Append(30, '&Activate Edit Network')
                self.menubar.Append(AddMenu, '&New Element')
                self.SetMenuBar(self.menubar)
                self.Bind(wx.EVT_MENU, self.Node_To_add, NewNode)
                self.Bind(wx.EVT_MENU, self.Edge_To_add, NewEdge)
                self.Bind(wx.EVT_MENU, self.Edition_Evaluation, Edition)
            Test=1
            if Test==1:
                #Obtention du chemin d'accès
                namepath=dlg.GetPath()
            
                #namepath='D:\\ProgThomas\\wolf_oo\\Sources-Thomas3\\Solutions\\Unit_Tests\\to_debug\\Jock_Basic\\Network_Vectors.vecz'
                #namepath='D:\\ProgThomas\\wolf_oo\\Sources-Thomas3\\Solutions\\Unit_Tests\\to_debug\\Jock_Compl_Network_New_3Groups\\Network_Vectors.vecz'
                #namepath='D:\\ProgThomas\\wolf_oo\\Sources-Thomas3\\Solutions\\Unit_Tests\\to_debug\\Network_Valve\\Network_Vectors.vecz'
                #Lecture du fichier en vue d'obtenir une structure d'objet (via dictionnaires + listes) de type "Zones"
                self.Zones=Import_vecz(namepath)
   
                if(self.Zones!=False):

                    #Sous-routine pour extraire l'ensemble des numéros de vecteur et de noeuds 
                    #Création du réseau afin de l'afficher en rendant comme résultat une structure Matplotlib.pyplot()
                    Network,self.Graph,self.List_Nodes,self.Discr_Nodes,self.Draw_Options,self.Edition_Mode,self.List_Nodes_OGL,self.Edg_OGL=Create_Network(self.Zones)
                    self.canvas = CubeCanvas(self)
                    self.Build_Network()
                    self.Param=self.Import_General_Parameters(namepath)
                    self.Nodes,self.Graph,self.Draw_Options=Import_Nodes_Attributes(namepath,self.Graph,self.List_Nodes,self.Draw_Options,self.Param)
                    self.Zones=Import_Vector_Attributes(namepath,self.Zones,self.Param)
                    self.Zones=Add_Main_Attributes(self.Zones)
                    #Network.show() #Ligne de code permettant l'affichage de la structure mais dans une fenêtre Matplotlib propre qui n'est donc pas intégrée à WX
            
                    #Méthode classique utilisée pour faire le lien WX/matplotlib
                    self.figure = Network
                    #ax = plt.gca()
                    self.canvas = FigureCanvas(self, -1, self.figure)

                    #Evènements pour l'affichage de la position courante du curseur
                    #Create 'Position Display'
                    self.Text = wx.StaticText( self, wx.ID_ANY, u"  Available Channels  ", wx.DefaultPosition, wx.DefaultSize, 0 )
                    self.Text.Wrap( -1 )
                    mouseMoveID = self.canvas.mpl_connect('motion_notify_event',self.onMotion)

                    #Remise à la taille correcte de la Figure suivant un agrandissement (à revoir pour la partie réduction)
                
                    self.sizer = wx.BoxSizer(wx.VERTICAL)
                    self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.EXPAND)
                    self.sizer.Add(self.Text,0, wx.LEFT | wx.EXPAND)
                    self.SetSizer(self.sizer)
                    self.Fit()
                
                #Evènements liés à l'obtention d'informations sur le noeud ou lignée identifiée via un clic
                self=self.canvas.mpl_connect('button_press_event', self.OnClick)
                #On peut désormais accéder aux informations du click
                t=1
            dlg.Destroy()

    #Ouverture de fichier ".vecz"
    def OnOpen(self, e):
        dlg = wx.FileDialog(self, "Choose the .vecz file",
                           defaultDir = "",
                           defaultFile = "",
                           wildcard = "*")
        if dlg.ShowModal() == wx.ID_OK:
            namepath=dlg.GetPath()
            t=1
        dlg.Destroy()
    #Ouverture d'une fenêtre supplémentaire
    def on_new_frame(self, event):
        title = 'New Network'
        frame = Mywin(None,title=title)
        #self.frame_number += 1
    
    #Procédure utilisée pour identifier le noeud ou vecteur le plus proche d'un clic effectué par l'utilisateur
    def Assoc_element(self):
        Index,dist=closest_node(self.LocNode,  self.List_Nodes['Coord'][:])
        #On va recherche alors les informations auprès de l'élément : noeud ou vecteur
        self.LocalNode=[]
        Type_Node=self.List_Nodes['TypeEl'][Index]
        Num_El=self.List_Nodes['NbrEl'][Index]
        self.LocalNode.append(Index)
        Test=1
        if(Type_Node=='Vector'):
            self.Print_VectorData()
        else:
            if(Type_Node=='Node'):
                Test=12

        return Test

    #Procédure d'ajout d'un noeud au sein du réseau
    def Node_To_add(self,e):
        Test=1
        #Nouvelle fenêtre s'ouvrant permettant ainsi d'ajouter les coordonnées du noeud
        New_frame=NewNodeFrame('New node in the network',self)
        # 
    #Procédure d'ajout d'un Edge au sein du réseau
    def Edge_To_add(self,e):
        Test=1  
        #Parcours du Graph à faire afin de s'assurer qu'au minimum deux noeuds sont bien présents au sein du réseau
        New_frame=NewEdgeFrame('New edge in the network',self)
    #Mise à jour des variables d'édition notamment pour arrêter ou commencer la phase d'édition du réseau
    def Edition_Evaluation(self,e):
        self.First_Node=[]
        self.Last_Node=[]
        if(self.Edition_Mode):
            self.Edition_Mode=False
            Test=1
            self.menubar.SetLabel(30,'&Activate Edit Network')
            self.menubar.Refresh()
            #La fin de la partie d'édition devrait s'accompagner d'une recharge effective du réseau afin de l'afficher également
            #Une recharge du réseau devrait d'ailleurs se faire après l'ajout de tout noeud/liaison
            Test=1
        else:
            self.Edition_Mode=True
            Test=1
            self.menubar.SetLabel(30,'&DEactivate Edit Network')
            self.menubar.Refresh()
            Test=1
       
            
    #Fonction destinée à la fois à récupérer les informations puis à afficher les données utiles
    def OnClick(self, e):
        type_event=e.button
        xdata=e.xdata
        ydata=e.ydata
        self.LocNode=(e.xdata,e.ydata)
        self.type_click=e.button
        self.new_edge='X'
        if(hasattr(self,'loc_new_edge')):
            if(self.loc_new_edge!='X'):
                self.new_edge=self.loc_new_edge
        if(hasattr(self,'Edition_Mode_Local')):
            self.Edition_Mode=self.Edition_Mode_Local
        #On va avoir deux types d'analyse selon le type de clic effectué : clic gauche renvoie des informations minimes sur le noeud ou tronçon le plus proche tandis que le clic droit ouvre
        #sur une fenêtre ouvrant sur la plupart des attributs de l'élément afin de les modifier (écriture souple ou lourde)
        if(type_event==1):
            #Clic Gauche
            if(self.Edition_Mode):
                Test=1
                #Clic gauche utilisé directement pour faire les liaisons entre les noeuds en venant soit sélectionner le premier noeud ou le second noeud pour faire la liaison
                Test=self.Select_Node(self.LocNode,self.Discr_Nodes,self.List_Nodes)
            else:
                lol=1
                LeTest=self.Assoc_element()
        elif(type_event==3):
            if(self.Edition_Mode):
                #Le clic droit amène directement dans la sous-routine d'ajout de noeud 
                New_frame=NewNodeFrame('New node in the network',self)
            else:
                #Clic Droit
                #Première étape est de savoir quel type de résultat veut afficher l'utilisateur : fenêtre intermédiaire proposant les différents choix disponibles
                #Déterminer le type de paramétrage à considérer ainsi qu'éventuellement, le pas de temps à évaluer : sous-routine à implémenter
                title='Data to draw'
                self.child_frame=Draw_Options(self,title,self)
                self.child_frame.Bind(wx.EVT_CLOSE, self.OnChildFrameClose)
                #self.Show_Results=False
                #Test temporaire afin de réaliser cette fois une surimpression du réseau en affichant des résultats
        #Phase de reconnaissance des coordonnées afin d'y associer l'élément le plus proche
        test=1
        return self

    def onMotion(self, evt):
        """This is a bind event for the mouse moving on the MatPlotLib graph
            screen. It will give the x,y coordinates of the mouse pointer.
        """
        xdata = evt.xdata
        ydata = evt.ydata
        try:
            x = round(xdata,4)
            y = round(ydata,4)
        except:
            x = ""
            y = ""

        self.Text.SetLabelText("x : %s ,y: %s" % (x,y))
    #Sous-routine utilisée pour ouvrir une nouvelle fenêtre locale via un clic droit afin d'afficher les informations du vecteur sélectionné
    def Print_VectorData(self):
        #Ouverture d'une nouvelle fenêtre
        #On va rechercher les informations sur le vecteur ainsi identifié
        Index=int(self.LocalNode[0])
        NumZone=int(self.List_Nodes['IdZone'][Index])
        NumVec=self.List_Nodes['NbrEl'][Index]
        VecName=self.Zones[NumZone]['Name'][NumVec]
        title = 'Vector ID: '+VecName
        frame = Mywin(parent=self,title=title,MainW=self)

    #On va recherche les différents paramètres généraux utiles de la simulation selon leur catégorie afin de former un dictionnaire
    def Import_General_Parameters(self,namepath):
        #Dossier Principal
        MainDir = os.path.dirname(namepath)
        MainDir = MainDir+'\\'
        Param={}
        #Fichier habituel
        ParamFile=MainDir+'General_Network.param'
        #On vérifie que le fichier est bien présent
        File_To_Read=os.path.isfile(ParamFile)
        if(File_To_Read):
            Param=Read_Param_file(ParamFile)
        else:
            dlg = wx.MessageDialog(
                None, "No general parameters found. Used default parameters ?", "Default parameters", wx.YES_NO | wx.CENTRE
            )
            result = dlg.ShowModal()
            if result == wx.ID_YES:
                #On applique les paramètres génériques
                ParamFile=MainDir+'General_Network.param.default'
                File_To_Read=os.path.isfile(filename)
                if(File_To_Read):
                    #Procédure identique à faire via le fichier param.default
                    #Il faut introduire à la main les différents paramètres ... A compléter
                    Test=1
                    Param=Read_Param_file(ParamFile)
                else:
                     #Il faut introduire à la main les différents paramètres ... A compléter
                     Test=2
            else:
                Test=3
                dlg = wx.FileDialog(self, "Choose the .param file",
                                    defaultDir = "",
                                    defaultFile = "",
                                    wildcard = "*")
                if dlg.ShowModal() == wx.ID_OK:
                    namepath_local=dlg.GetPath()
                    t=1
                dlg.Destroy()
                Extent='.param'
                extension = os.path.splitext(namepath_local)[1]
                if(extension!=Extent):
                    print('Invalid file type for parameters')
                    return False
            
        return Param
    #La fermeture de la fenêtre secondaire vient donc indiquer que l'utilisateur a potentiellement renseigné ce qui l'intéressait.
    def OnChildFrameClose(self, event):
        #On analyse les items en venant donc extraire les différentes informations disponibles
        Test=1
        if(hasattr(self,'Items')):
            if(bool(self.Items)):
                Param_Simul=[0,0,0,0,0]
                NbTypeResults=len(self.Items)
                for Option in self.Items:
                    Param_Simul[Option]=1

                #if(self.Show_Results):
                title='Time step'
                Max_Val=int(self.Param['Time']['Number of time save steps'][0])
                self.Time_Step=1
                self.Param_Simul=Param_Simul
                self.frame = MyFrame_Slider(parent=self, title=title,Max_Val=Max_Val)
            
            else:
                 Test=1

            Test=1

    def Select_Node(self,LocNode,Discr_Nodes,List_Nodes):
        #Choix à faire du premier ou second noeud de l'Edge : on vient donc associer selon les coordonnées du noeud, celui qui est le plus proche
        Loc_Node,dis=closest_node(LocNode, Discr_Nodes['Coord'][:])

        Ind_Node,dis=closest_node(Discr_Nodes['Coord'][Loc_Node], List_Nodes['Coord'][:])

        if(bool(self.First_Node)):
            #Cela signifie qu'il faut donc bien remplir le deuxième noeud de la nouvelle liaison à ajouter
            self.Last_Node.append(Ind_Node)
            FNode=self.First_Node[0]
            LNode=self.Last_Node[0]
            Nb_edges=len(self.Graph.edges)
            self.Graph.add_edge(FNode,LNode)
            self.Graph[FNode][LNode]['Name']=self.new_edge
            self.Graph[FNode][LNode]['Zone']=0
            self.Graph[FNode][LNode]['Vector']=Nb_edges+1
            #Edges_List=list(self.Graph.edges())
            self.First_Node=[]
            self.Last_Node=[]
            if(hasattr(self,'loc_new_edge')):
                self.loc_new_edge='X'
        else:
            #Premier Noeud qu'il faut remplir
            self.First_Node.append(Ind_Node)
            if(bool(self.First_Node) and bool(self.Last_Node)):
                #Cela ne peut se produire que s'il y a une intervention manuelle infructueuse de l'utilisateur
                Nb_edges=len(self.Graph.edges)
                FNode=self.First_Node[0]
                LNode=self.Last_Node[0]
                self.Graph.add_edge(FNode,LNode)
                self.Graph[FNode][LNode]['Name']=self.new_edge
                self.Graph[FNode][LNode]['Zone']=self.new_edge_Type
                self.Graph[FNode][LNode]['Vector']=Nb_edges+1
                self.First_Node=[]
                self.Last_Node=[]
        Test=1

    #Mise en place des procédures OpenGL
    def Build_Network(self):
        self.List_Nodes_OGL,self.Edg_OGL
        glBegin(GL_LINES)
        for cubeEdge in self.Edg_OGL:
            for cubeVertex in cubeEdge:
                cubeVertex=cubeVertex-1
                Loc_vertex=(float(self.List_Nodes_OGL[cubeVertex][0]),float(self.List_Nodes_OGL[cubeVertex][1]),float(self.List_Nodes_OGL[cubeVertex][2]))
                #Loc_vertex=(int(self.List_Nodes_OGL[cubeVertex][0]),int(self.List_Nodes_OGL[cubeVertex][1]),int(self.List_Nodes_OGL[cubeVertex][2]))
                glVertex3dv(Loc_vertex)
                test=1
        glEnd()

        glBegin(GL_POINTS)
        for cubeVertex in self.List_Nodes_OGL:
            Loc_vertex=(float(cubeVertex[0]),float(cubeVertex[1]),float(cubeVertex[2]))
            glVertex3dv(cubeVertex)
        glEnd()

class MyCanvasBase(glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1)
        self.init = False
        self.context = glcanvas.GLContext(self)

        self.lastx = self.x = 30
        self.lasty = self.y = 30
        #self.size = None
        self.SetSize(500,400)
        self.List_Nodes_OGL=parent.List_Nodes_OGL
        self.Edg_OGL=parent.Edg_OGL
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
        return LocCoord




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
                glVertex3dv(NewVertiList[cubeVertex])
        glEnd()
        glBegin(GL_POINTS)
        for cubeVertex in NewVertiList:
            glVertex3dv(cubeVertex)
        glEnd()  

    def refresh2d(self,width,height):
        #glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, width, 0.0, height, 0.0, 6.0)
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
        glPointSize(10)
        glEnable(GL_POINT_SMOOTH)


    def OnDraw(self):
        # clear color and depth buffers
        glClearColor(1,1,1,0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #glClearColor(0,0,1,0)
        glLoadIdentity()
        self.refresh2d(width,height) 
        glColor3f(0.0, 0.0, 0.0) 
        #self.draw_rect(10, 10, 200, 100) 
        self.wireCube()

        #glTranslatef(0.0, 0.0, -5)


        self.SwapBuffers()

#Frame utilisée pour permettre la mise en place du nouveau noeud    
class NewNodeFrame(wx.Frame):
    """
    Class used for creating frames other than the main one
    """
    def __init__(self, title, parent):
       super(NewNodeFrame, self).__init__(parent, title = title,size = (300,200),style=wx.DEFAULT_FRAME_STYLE|wx.FRAME_FLOAT_ON_PARENT) 
       #Ajout d'un nouveau noeud entraîne à l'activiation du mode d'édition du réseau
       parent.Edition_Mode_Local=True

       vbox = wx.BoxSizer(wx.VERTICAL) 

       self.Centre() 
       frame_sizer = wx.BoxSizer(wx.VERTICAL)
       #frame_sizer.Add(panel, 1, wx.EXPAND| wx.LEFT | wx.RIGHT, wx.ALIGN_CENTER)
       
       #Message d'annonce pour savoir ce qui est à réaliser
       Message='Characteristics of the new node'
       self.message = wx.StaticText(self, -1, Message)
       frame_sizer.Add(self.message, 0, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND)
       
       #Partiée à la grille des coordonnées du noeud 
       self.panel = PanelNode(self,parent)
       frame_sizer.Add(self.panel, 1, wx.EXPAND)
       #Partie liée aux choix de validation ou d'annulation
       sz2 = wx.BoxSizer(wx.HORIZONTAL)
       self.btn=wx.Button(self,-1,"Ok")
       sz2.Add(self.btn,0, wx.ALL, 10)
       self.btn.Bind(wx.EVT_BUTTON,self.Saved_Node) 

       self.btn2=wx.Button(self,-1,"Annuler")
       sz2.Add(self.btn2,0, wx.ALL, 10)
       self.btn2.Bind(wx.EVT_BUTTON,self.CloseFrame) 

       frame_sizer.Add(sz2, 0, wx.ALIGN_CENTER)
       self.SetAutoLayout(True)
       self.SetSizerAndFit(frame_sizer)
       self.Show()
       Test=1
    #Sous-routine utilisée dans le but d'ajouter un noeud supplémentaire au réseau déjà présent
    def Saved_Node(self, e):

       Parent=self.GetParent()
       #Il faut rechercher les valeurs dans la grille pour ajouter un nouveau noeud en faisant test sur le type de noeud 
       
       Nb_Rows=self.panel.thegrid.GetNumberRows()
       self.Main_Attr=['Name','Type(R or J)','Coordinate X','Coordinate Y','Coordinate Z']
       Valid_Test=True
       for Row in range(Nb_Rows):
           Value=self.panel.GridValues[Row]
           if(self.panel.Main_Attr[Row]==self.Main_Attr[1]):
               Type_Node=Value.lower()
               if(Type_Node!='j' and Type_Node!='r'):
                   #Problème de format proposé par l'utilisateur, un évènement doit être appelé
                   dlg = wx.MessageDialog(
                        None, "The proposed format for the type of Node is not good. Impose the J Format ?", "Incorrect format", wx.YES_NO | wx.CANCEL | wx.CENTRE
                    )
                   result = dlg.ShowModal()
                   self.Centre() 
                   self.Show() 
                   Valid_Test=False
                   if result == wx.ID_YES:
                      Type_Node='j'
                      Valid_Test=True
                   else:
                        pass
                   Test=1
       if(Valid_Test):
            #On passe cette fois à l'ajout du noeud dans le réseau
            Nb_Nodes=len(Parent.Graph.nodes)
            Loc_Node=Nb_Nodes+1
            #Initialisation générique
            Parent.Graph.add_node(Loc_Node,pos=('X','X'),posz='X',Index_Position=Loc_Node,name='X')
            New_Node=Parent.Graph.nodes[Nb_Nodes]
            Test=1

            #Evaluation des paramètres importants
            NameNode=self.panel.GridValues[0]
            CoordX=self.panel.GridValues[2]
            CoordY=self.panel.GridValues[3]
            CoordZ=self.panel.GridValues[4]

            #On complète List_nodes également et Nodes
            Current_Coord=(CoordX,CoordY)
            Parent.List_Nodes['Coord'].append(Current_Coord)
            Parent.List_Nodes['IdZone'].append(-1)
            Parent.List_Nodes['NbrEl'].append(Loc_Node)
            Parent.List_Nodes['TypeEl'].append('Node')
            TypeN='Reservoirs'
            if(Type_Node=='j'):
                TypeN='IncJunctions'
            Parent.Nodes[TypeN]['Name'].append(NameNode)
            Parent.Nodes[TypeN]['CoordPlan'].append((float(CoordX),float(CoordY)))
            Parent.Nodes[TypeN]['CoordZ'].append(float(CoordZ))
            Parent.Nodes[TypeN]['IndPos'].append(Loc_Node)
            #S'il s'agit d'un réservoir, on complète également les attributs selon des valeurs standardisées
            if(Type_Node=='r'):
                List_Attr=['Section','Max_H','Min_H','IC_V']
                Standard_Values=[100,10,0,8]
                cpt=0
                for Attr in List_Attr:
                    Parent.Nodes[TypeN][Attr].append(Standard_Values[cpt])
                    cpt=cpt+1

       Test=1
       return Test
            #Remplacement via les données réelles
    #L'annulation étant choisie par l'utilisateur, l'option est donc levée et la fenêtre est simplement fermée
    def CloseFrame(self, e):
       Test=1
       self.Close()
       self.Destroy()

#Création de la grille permettant l'affichage des principaux attributs pour un vecteur
class PanelNode(wx.Panel):
    def __init__(self, parent,MainW):
        super(PanelNode, self).__init__(parent)
    
        #Initialisation de la grille = évaluation du nombre d'attributs à afficher
        Index=int(MainW.LocalNode[0])

        self.Main_Attr=['Name','Type(R or J)','Coordinate X','Coordinate Y','Coordinate Z']
        Nb_attrib=len(self.Main_Attr)
        #Mise en place de la grille + colonne
        mygrid = grid.Grid(self)
        mygrid.CreateGrid( Nb_attrib, 1)
        mygrid.SetColLabelValue(0, "Value")
        #On vient afficher l'ensemble des données utiles pour le noeud
        cpt_row=0

        #On vient également compléter par défaut chaque colonne afin que l'utilisateur puisse rapidement uniquement modifier ce qu'il souhaite
        if(Index==0):
            if(hasattr(MainW,'Graph')):
                if(hasattr(MainW.Graph,'nodes')):
                    if(bool(MainW.Graph.nodes)):
                        #On considère qu'à ce stade-là, la structure attendue est bien respectée et qu'au moins un noeud a déjà été implémenté
                        Nb_Nodes=len(MainW.Graph.nodes)
                        Dflt_Name='Node_'+str(Nb_Nodes+1)
                        Dft_CoordX=str(float(MainW.Graph.nodes[1]['pos'][0])+float(Nb_Nodes)/float(1000))
                        Dft_CoordY=str(float(MainW.Graph.nodes[1]['pos'][1])+float(Nb_Nodes)/float(1000))
                        Dft_CoordZ=MainW.Graph.nodes[1]['posz']
                        Default_Values=[Dflt_Name,'J',Dft_CoordX,Dft_CoordY,Dft_CoordZ]
                    else:
                        Default_Values=['Node_1','J','0.0','0.0','0.0']
                else:
                    Default_Values=['Node_1','J','0.0','0.0','0.0']
            else:
                Default_Values=['Node_1','J','0.0','0.0','0.0']
        else:
            Default_Values=['Node_1','J',str(MainW.LocalNode[0]),str(MainW.LocalNode[1]),'0.0']
        #Remplissage du tableau
        cpt_row=0
        self.GridValues=[]
        for Attr in self.Main_Attr:
            mygrid.SetRowLabelValue(cpt_row,Attr)
            mygrid.SetCellAlignment(cpt_row, 0, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            mygrid.SetCellValue(cpt_row,0, Default_Values[cpt_row])
            self.GridValues.append(Default_Values[cpt_row]) 
            cpt_row=cpt_row+1
        mygrid.AutoSizeColumns(False)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(mygrid, 1, wx.EXPAND)
        self.thegrid=mygrid
        self.SetSizerAndFit(sizer)
        Test=1
        self.modified_grid=False
        self.thegrid.Bind(grid.EVT_GRID_CELL_CHANGED, self.Saved_Modifications)
    def Saved_Modifications(self,e):
        self.modified_grid=True
        #Sauvegarde des valeurs de la grille
        Nb_Rows=self.thegrid.GetNumberRows()
        self.GridValues=[]
        for Row in range(Nb_Rows):
            self.GridValues.append(self.thegrid.GetCellValue(Row,0)) 

#Ouverture d'une nouvelle fenêtre permettant de laisser le choix à l'utilisateur de sélectionner ce qu'il souhaite afficher
class Draw_Options(wx.Frame):
   def __init__(self, parent, title,MainW): 
      super(Draw_Options, self).__init__(parent, title = title,size = (300,200),style=wx.DEFAULT_FRAME_STYLE|wx.FRAME_FLOAT_ON_PARENT)  
      #panel = MyPanel(self,MainW)
      #panel = wx.Panel(self) 
      vbox = wx.BoxSizer(wx.VERTICAL) 

      self.Centre() 
      frame_sizer = wx.BoxSizer(wx.VERTICAL)
      #frame_sizer.Add(panel, 1, wx.EXPAND| wx.LEFT | wx.RIGHT, wx.ALIGN_CENTER)
      #Message d'annonce pour savoir ce qui est à réaliser
      Message='What do you want to draw ?'
      self.message = wx.StaticText(self, -1, Message)
      frame_sizer.Add(self.message, 0, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND)
      Choices=['HeadNodes','Altimetry','Discharge','Diameter']
      Name_Box='Draw_Box'
      self.CheckBox = wx.CheckListBox(self, choices=Choices, name=Name_Box)
      frame_sizer.Add(self.CheckBox, 1, wx.EXPAND | wx.LEFT | wx.RIGHT)
      self.SetSizerAndFit(frame_sizer)

      sz2 = wx.BoxSizer(wx.HORIZONTAL)
      #dlg1=sz2.Add(wx.Button(self, wx.ID_OK, ""), 0, wx.ALL, 10)
      self.btn=wx.Button(self,-1,"Ok")
      sz2.Add(self.btn,0, wx.ALL, 10)
      self.btn.Bind(wx.EVT_BUTTON,self.Param_Read) 

      #dlg2=sz2.Add(wx.Button(self, wx.ID_CANCEL, ""), 0, wx.ALL, 10)
      self.btn2=wx.Button(self,-1,"Annuler")
      sz2.Add(self.btn2,0, wx.ALL, 10)
      self.btn2.Bind(wx.EVT_BUTTON,self.CloseFrame) 

      frame_sizer.Add(sz2, 0, wx.ALIGN_CENTER)
      self.SetAutoLayout(True)
      self.SetSizerAndFit(frame_sizer)
      self.Show() 
      self.CenterOnScreen() 
      #self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
      Test=1
      #fdRet = dlgF.ShowModal()
      List_Params=[]
   
   #L'utilisateur choisit ok, mais on doit bien également s'assurer que des cases ont été cochées pour être capable d'afficher les résultats
   def Param_Read(self, e):
       Test=1
       Parent=self.GetParent()
       Parent.Items=self.CheckBox.GetCheckedItems()
       self.Close()
       self.Destroy()

   #L'annulation étant choisie par l'utilisateur, l'option est donc levée et la fenêtre est simplement fermée
   def CloseFrame(self, e):
       Test=1
       self.Close()
       self.Destroy()

#Frame utilisée pour permettre la mise en place du nouveau noeud    
class NewEdgeFrame(wx.Frame):
    """
    Class used for creating frames other than the main one
    """
    def __init__(self, title, parent):
       super(NewEdgeFrame, self).__init__(parent, title = title,size = (400,300),style=wx.DEFAULT_FRAME_STYLE|wx.FRAME_FLOAT_ON_PARENT) 
       #Ajout d'un nouveau noeud entraîne à l'activiation du mode d'édition du réseau
       parent.Edition_Mode_Local=True

       self.Centre() 
       frame_sizer = wx.BoxSizer(wx.VERTICAL)
       #frame_sizer.Add(panel, 1, wx.EXPAND| wx.LEFT | wx.RIGHT, wx.ALIGN_CENTER)
       
       #Message d'annonce pour savoir ce qui est à réaliser
       Message='Characteristics of the new edge'
       self.message = wx.StaticText(self, -1, Message)
       #frame_sizer.Add(self.message, 0, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND)
       frame_sizer.Add(self.message, 0, wx.EXPAND)
       
       #Partiée à la grille des coordonnées du noeud 
       self.panel = PanelEdge(self,parent)
       frame_sizer.Add(self.panel, 1, wx.EXPAND)
       #Partie liée aux choix de validation ou d'annulation
       sz2 = wx.BoxSizer(wx.HORIZONTAL)
       self.btn=wx.Button(self,-1,"Ok")
       sz2.Add(self.btn,0, wx.ALL, 10)
       self.btn.Bind(wx.EVT_BUTTON,self.Saved_Edge) 

       self.btn2=wx.Button(self,-1,"Annuler")
       sz2.Add(self.btn2,0, wx.ALL, 10)
       self.btn2.Bind(wx.EVT_BUTTON,self.CloseFrame) 

       frame_sizer.Add(sz2, 0, wx.ALIGN_CENTER)
       self.SetAutoLayout(True)
       self.SetSizerAndFit(frame_sizer)
       self.Show()
       Test=1
    #Sous-routine utilisée dans le but d'ajouter un noeud supplémentaire au réseau déjà présent
    def Saved_Edge(self, e):

       Parent=self.GetParent()
       Parent.First_Node=[]
       Parent.Last_Node=[]
       #Il faut rechercher les valeurs dans la grille pour ajouter un nouveau noeud en faisant test sur le type de noeud 
       
       Nb_Rows=self.panel.thegrid.GetNumberRows()
       self.Main_Attr=['First Node Name','Second Node Name']
       Valid_Test=True
       Node_pos=[]
       Node_pos.append(self.panel.GridValues[0])
       Node_pos.append(self.panel.GridValues[1])
       Info_Edge=[]
       Info_Edge.append(self.panel.GridValues[2])
       Info_Edge.append(self.panel.GridValues[3])
       Test=1
       #On va analyser les deux valeurs obtenues pour identifier s'il s'agit bien d'un noeud présent dans le réseau
       #Première analyse est effectuée vis-à-vis des noms disponibles
       TypeNode=['Reservoirs','IncJunctions']
       Func_Expres=['Name']
       Pos_Node=[]
       Attr_Node=[0,0]
       for Attr in range(len(Attr_Node)):
           for Function in range(len(Func_Expres)):
               for Node_Type in TypeNode:
                   Loc_lgth=len(Parent.Nodes[Node_Type][Func_Expres[Function]])
                   for cpt in range(Loc_lgth):
                        Loc_Name=Parent.Nodes[Node_Type][Func_Expres[Function]][cpt]
                        if(Loc_Name==Node_pos[Attr]):
                            Attr_Node[Attr]=1
                            Pos_Node.append([])
                            Pos_Node[len(Pos_Node)-1].append(Node_Type)
                            Pos_Node[len(Pos_Node)-1].append(Parent.Nodes[Node_Type]['IndPos'][cpt])
                            break
                   if(Attr_Node[Attr]==1):
                        break
           if(Attr_Node[Attr]==1):
                break
       if(Attr_Node[0]==1 and Attr_Node[1]==1):
            Test=1
            Nb_edges=len(Parent.Graph.edges)
            Parent.Graph.add_edge(Pos_Node[0][1],Pos_Node[1][1])
            Parent.Graph[FNode][LNode]['Name']=Info_Edge[0]
            Parent.Graph[FNode][LNode]['Zone']=Info_Edge[1]
            Parent.Graph[FNode][LNode]['Vector']=Nb_edges+1
            Parent.First_Node=[]
            Parent.Last_Node=[]
       else:
            #Noms proposés par l'utilisateur ne sont pas conformes : on vérifie lesquels en premier lieu
            if(Attr_Node[0]==0):
                Message="The proposed name for first node is not coherent. Check in the network ?"
                if(Attr_Node[1]==0):
                    Message="The proposed names for first and last node are not coherent. Check in the network ?"
                else:
                    Parent.Last_Node.append(Pos_Node[0][1])
            else:
                Parent.First_Node.append(Pos_Node[0][1])
                Message="The proposed name for last node is not coherent. Check in the network ?"
            dlg = wx.MessageDialog(
                None, Message, "Incorrect format", wx.YES_NO | wx.CANCEL | wx.CENTRE | wx.STAY_ON_TOP
            )
            result = dlg.ShowModal()
            self.Centre() 
            self.Show() 
            Valid_Test=False
            if result == wx.ID_YES:
                Type_Node='j'
                Parent.loc_new_edge=Info_Edge[0]
                Parent.loc_new_edge_type=Info_Edge[1]
            else:
               Parent.First_Node=[]
               Parent.Last_Node=[]
       
       return Test
            #Remplacement via les données réelles
    #L'annulation étant choisie par l'utilisateur, l'option est donc levée et la fenêtre est simplement fermée
    def CloseFrame(self, e):
       Test=1
       self.Close()
       self.Destroy()
    def OnClickNewNode(self, e):
        type_event=e.button
        xdata=e.xdata
        ydata=e.ydata
        self.LocNode=(e.xdata,e.ydata)
        self.type_click=e.button
 #Création de la grille permettant l'affichage des principaux attributs pour un vecteur
class PanelEdge(wx.Panel):
    def __init__(self, parent,MainW):
        super(PanelEdge, self).__init__(parent)
    
        #Initialisation de la grille = évaluation du nombre d'attributs à afficher
        Index=int(MainW.LocalNode[0])

        self.Main_Attr=['First Node Name','Second Node Name','Name Edge','Type Element(P,V or T)']
        Nb_attrib=len(self.Main_Attr)
        #Mise en place de la grille + colonne
        mygrid = grid.Grid(self)
        mygrid.CreateGrid( Nb_attrib, 1)
        mygrid.SetColLabelValue(0, "Value")
        #On vient afficher l'ensemble des données utiles pour le noeud
        cpt_row=0

        #On vient également compléter par défaut chaque colonne afin que l'utilisateur puisse rapidement uniquement modifier ce qu'il souhaite
        Nb_Nodes=len(MainW.Graph.edges)+1
        Edge_Name='Edge_'+str(Nb_Nodes)
        Default_Values=['0','0',Edge_Name,'P']
        #Remplissage du tableau
        cpt_row=0
        self.GridValues=[]
        for Attr in self.Main_Attr:
            mygrid.SetRowLabelValue(cpt_row,Attr)
            mygrid.SetCellAlignment(cpt_row, 0, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            mygrid.SetCellValue(cpt_row,0, Default_Values[cpt_row])
            self.GridValues.append(Default_Values[cpt_row]) 
            cpt_row=cpt_row+1
        #mygrid.AutoSizeColumns(False)
        mygrid.SetRowLabelSize(150)
        mygrid.EnableDragGridSize(True)
        mygrid.SetColSize(0,100)
        #mygrid.AutoSize()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(mygrid, 1, wx.EXPAND)
        self.thegrid=mygrid
        self.SetSizer(sizer)
        #self.SetSizerAndFit(sizer)
        Test=1
        self.modified_grid=False
        self.thegrid.Bind(grid.EVT_GRID_CELL_CHANGED, self.Saved_Modifications)
    
    def Saved_Modifications(self,e):
        self.modified_grid=True
        #Sauvegarde des valeurs de la grille
        Nb_Rows=self.thegrid.GetNumberRows()
        self.GridValues=[]
        for Row in range(Nb_Rows):
            self.GridValues.append(self.thegrid.GetCellValue(Row,0)) 


class Mywin(wx.Frame): 
   def __init__(self, parent, title,MainW): 
      super(Mywin, self).__init__(parent, title = title,size = (300,200),style=wx.DEFAULT_FRAME_STYLE|wx.FRAME_FLOAT_ON_PARENT)  
      panel = MyPanel(self,MainW)
      #panel = wx.Panel(self) 
      vbox = wx.BoxSizer(wx.VERTICAL) 

      """
      self.btn = wx.Button(panel,-1,"click Me") 
      #vbox.AddStretchSpacer()#Elément pour créer un espace supplémentaire
      vbox.Add(self.btn, 0, wx.CENTER)
      #vbox.AddStretchSpacer()
      self.btn.Bind(wx.EVT_BUTTON,self.OnClicked) 

      panel.SetSizer(vbox)
      """
      #On vient donc afficher dans le petit tableau d'exportation le nom de l'attribut ainsi que sa valeur
      Test=1
      self.Centre() 
      frame_sizer = wx.BoxSizer(wx.VERTICAL)
      frame_sizer.Add(panel, 1, wx.EXPAND)
      self.SetSizerAndFit(frame_sizer)
      #self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT)
      self.Show() 
      #self.Fit()  
      Test=1
      self.OrigFrame=MainW
      self.locpanel=panel
      self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

   def OnClicked(self, event): 
      btn = event.GetEventObject().GetLabel()
   
   #Vérification à la sortie de la fenêtre si des valeurs ont été modifiées et si c'est le cas, demande pour enregistrer les modifications
   def OnCloseWindow(self, event):
       #On va rechercher si un évènement de modification a été identifié

       if(self.locpanel.modified_grid):
           #Actions à réaliser afin de permettre la sauvegarde ou non des changements en initiant en premier lieu l'ouverture d'une fenêtre
           dlg = wx.MessageDialog(
                None, "Do you want to save the modifications ?", "Save the results", wx.YES_NO | wx.CANCEL | wx.CENTRE
            )
           result = dlg.ShowModal()
           self.Centre() 
           self.Show() 
           if result == wx.ID_YES:
              Test=1
           if result != wx.ID_CANCEL:
               self.Destroy()
           Test=1
       else:
            self.Destroy()
#Création de la grille permettant l'affichage des principaux attributs pour un vecteur
class MyPanel(wx.Panel):
    def __init__(self, parent,MainW):
        super(MyPanel, self).__init__(parent)
 
        #Initialisation de la grille = évaluation du nombre d'attributs à afficher
        Index=int(MainW.LocalNode[0])
        NumZone=MainW.List_Nodes['IdZone'][Index]
        Nb_attrib=len(MainW.Zones[NumZone]['Princ_Attrib'])
        #Mise en place de la grille + colonne
        mygrid = grid.Grid(self)
        mygrid.CreateGrid( Nb_attrib, 1)
        mygrid.SetColLabelValue(0, "Value")
        #On vient afficher l'ensemble des informations pertinentes du vecteur selon les lignes en les complétant
        NumVec=MainW.List_Nodes['NbrEl'][Index]
        Main_Attr=MainW.Zones[NumZone]['Princ_Attrib']
        cpt_row=0
        for Attr in Main_Attr:
            mygrid.SetRowLabelValue(cpt_row,Attr)
            mygrid.SetCellAlignment(cpt_row, 0, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            if(Attr in MainW.Zones[NumZone]):
                Val_Attr=MainW.Zones[NumZone][Attr][NumVec]
                mygrid.SetCellValue(cpt_row,0, Val_Attr)
                Test=21
            else:
                Val_Attr='X'
            cpt_row=cpt_row+1
        mygrid.AutoSizeColumns(setAsMin=True)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(mygrid, 1, wx.EXPAND)
        self.thegrid=mygrid
        self.SetSizer(sizer)
        Test=1
        self.modified_grid=False
        self.thegrid.Bind(grid.EVT_GRID_CELL_CHANGED, self.Saved_Modifications)
    def Saved_Modifications(self,e):
        self.modified_grid=True
        Test=1
#Partie liée à l'utilisation d'un slider dans le cadre de l'affichage des résultats
class MyFrame_Slider(wx.Frame):
    def __init__(self, parent, title,Max_Val):
        super(MyFrame_Slider, self).__init__(parent, title =title, size = (400,200))
 
 
        self.panel = MyPanel_Slider(self,Max_Val,parent)
        self.Show()
class MyPanel_Slider(wx.Panel):
    def __init__(self, parent,Max_Val,MainW):
        super(MyPanel_Slider, self).__init__(parent)
 
        vbox = wx.BoxSizer(wx.VERTICAL)
        #Partie message d'introduction
        Message='Choice of the time step'
        self.message = wx.StaticText(self, -1, Message)
        vbox.Add(self.message, 0, wx.CENTER)
        #Partie liée à la revue automatique des différents pas de temps en permettant aussi un temps de lecture
        Choices=['Automatic Review']
        Name_Box='Draw_Box'
        frame_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.CheckBox = wx.CheckListBox(self, choices=Choices, name=Name_Box)
        frame_sizer.Add(self.CheckBox, 1, wx.EXPAND | wx.LEFT | wx.RIGHT)
        #self.SetSizerAndFit(frame_sizer)
        vbox.Add(frame_sizer, 0, wx.ALIGN_CENTER)
        #Partie slider
        self.SliderValue = 1
        self.MaxVal=Max_Val
        self.slider = wx.Slider(self, value=1, minValue=1, maxValue=Max_Val,
                             style=wx.SL_HORIZONTAL | wx.SL_LABELS)
 
        vbox.Add(self.slider,-1, flag = wx.EXPAND | wx.TOP, border = 5)
        
        self.btn=wx.Button(self,-1,"Ok")
        vbox.Add(self.btn,0, wx.CENTER) 
        self.btn.Bind(wx.EVT_BUTTON,self.Slider_Read)

        self.Frame=MainW
        self.slider.Bind(wx.EVT_SLIDER, self.OnSliderScroll)
        self.SetSizerAndFit(vbox)
        self.Center()
     
 
    def Slider_Read(self, e):
       Test=1
       Parent=self.GetParent()
       Parent.Automatic=self.CheckBox.GetCheckedItems()
       #self.Close()
       #self.Destroy()
       #Parent.Close()
       #Parent.Destroy()

       Frame_loc=self.Frame
       Frame_loc.Time_Step=self.SliderValue
       if(bool(Parent.Automatic)):
           Nb_cases=int(self.MaxVal)-int(Frame_loc.Time_Step)+1
       else:
           Nb_cases=1
       for cpt_cases in range(Nb_cases): 
           Loc_step=Frame_loc.Time_Step+cpt_cases
           Results_Fig=Show_Results(Frame_loc.Graph,Frame_loc.Draw_Options,Frame_loc.Param_Simul,Frame_loc.Zones,Frame_loc.Nodes,Loc_step)
           #Remplacement de la Figure originale par celle des résultats obtenus
           Frame_loc.figure.clear()
           Frame_loc.figure=Results_Fig
           Frame_loc.canvas = FigureCanvas(Frame_loc, -1, Frame_loc.figure)

           #Remise à la taille correcte de la Figure suivant un agrandissement (à revoir pour la partie réduction)
           Frame_loc.SetSizerAndFit(Frame_loc.sizer)
           Frame_loc.Show_Results=False
           time.sleep(2)
    def OnSliderScroll(self, event):
        obj = event.GetEventObject()
        value = obj.GetValue()
        self.SliderValue=self.slider.GetValue()


#Partie liée à la mise en place d'actions lorsque l'utilisateur souhaite obtenir des informations à propos du réseau ou souhaite le modifier/construire
#Construction de segments pour le réseau
class LineBuilder:
    def __init__(self, line):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        print('click', event)
        if event.inaxes!=self.line.axes: return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()
        xdata=self.xs
        ydata=self.xs
# Python code to sort a list by creating  
##Extract_SubStrings : extraction de substrings séparés par des caractères spéciaux
#string : string complet auquel on va donc extraire la liste de substrings séparés par des caractères spéciaux
#special_char : caractère spécial utilisé pour séparer les substrings entre eux
def Extract_SubStrings(String,Special_char):
    List_Substrings=[]
    cpt_prev=0
    cpt_new=0
    End_Line_Char='\n'
    String=String.lstrip()
    for i in range(len(String)):
        if(String[i]==Special_char or String[i:i+1]==End_Line_Char or i+1==len(String)):
            if(i+1==len(String)):
                cpt_new=cpt_new+1
            List_Substrings.append(String[cpt_prev:cpt_new])
            cpt_new=cpt_new+1
            cpt_prev=cpt_new
        else:
            cpt_new=cpt_new+1
    return List_Substrings

#Lecture du nombre de vecteurs présents dans une zone
def Nb_Vector_in_Zone(filename):
    j=0
    Nb_Vector=0
    for Addit_Word in filename:
        j=j+1
        if(j==1):
            #On a cette fois le nombre de vecteurs au sein de la zone
            Addit_Word=Addit_Word.rstrip('\n')
            Nb_Vector=int(Addit_Word)
            break
    return Nb_Vector

#Lecture des différents vecteurs présents dans une zone
def read_complete_vectors(file,Zones,Nb_vec,Id_Zone):
    #Première ligne est le nom de l'élément
    for i in range(Nb_vec):
        name=file.readline().rstrip('\n')
        NB_vertex=int(file.readline())
        Zones[Id_Zone]['Name'].append(name)
        Zones[Id_Zone]['NbrVertex'].append(NB_vertex)
        Zones[Id_Zone]['Coord'][0].append([])
        Zones[Id_Zone]['Coord'][1].append([])
        Zones[Id_Zone]['Coord'][2].append([])
        Length=len(Zones[Id_Zone]['Coord'][0])-1
        for j in range(NB_vertex):
            Coordinates=file.readline().rstrip('\n')
            Coord=Coordinates.split()
            Zones[Id_Zone]['Coord'][0][Length].append(Coord[0])
            Zones[Id_Zone]['Coord'][1][Length].append(Coord[1])
            Zones[Id_Zone]['Coord'][2][Length].append(Coord[2])
            test=1
        #3 lignes sont alors à lire et ne présentent pas pour le moment un intérêt à être modifiées
        for i in range(3):
            name=file.readline()
    IERR=0
    return IERR
# Importation vise à prendre le fichier vecz afin de rendre en sortie le dictionnaire comprenant l'ensemble des vertex
# Chaque Vertex est décrit via son numéro de zone, numéro de vecteur, nombre de vertex le décrivant et finalement chaque vertex
def Import_vecz(filename):
    #Première phase, on vérifie que l'extension du fichier est la bonne
    Spec_char='.'
    #List_sbstr=Extract_SubStrings(filename,Spec_char)
    Extent='.vecz'
    extension = os.path.splitext(filename)[1]
    if(extension!=Extent):
        print('Invalid file type')
        return False
    file = open(filename,'r')
    i=0
    j=0
    Nb_vec=0
    #Première étape avant d'entrer dans le fichier est d'abord de réaliser la structure de la sauvegarde d'informations
    #Le nom des arguments seront les suivants : nom, numéro du vecteur, nombre de vertex au sein du vertex et puis coordonnées
    Zones=[]
    Vectors={}
    Vectors['Name']=[]
    Vectors['NbrVec']=[]
    Vectors['NbrVertex']=[]
    Vectors['Coord']=[]
    Vectors['Coord'].append([])
    Vectors['Coord'].append([])
    Vectors['Coord'].append([])
    Id_Zone=0
    for New_Word in file:
        #Première partie liée aux informations génériques pour compléter ainsi le dictionnaire de Vecteurs
        i=i+1
        New_Word=New_Word.rstrip('\n')
        if(i==2):
            #Il s'agit du nombre de zones présents
            Nb_zones=int(New_Word)
            loc_zone=0
            for a in range(Nb_zones):
                New_Vectors={}
                #for key in Vectors:
                #    New_Vectors[key]=Vectors[key].copy()
                #Zones.append(New_Vectors)
                Zones.append({})
                Zones[loc_zone]['Name']=[]
                Zones[loc_zone]['NbrVec']=[]
                Zones[loc_zone]['NbrVertex']=[]
                Zones[loc_zone]['Coord']=[]
                Zones[loc_zone]['Coord'].append([])
                Zones[loc_zone]['Coord'].append([])
                Zones[loc_zone]['Coord'].append([])
                loc_zone=loc_zone+1
            name=file.readline().rstrip('\n') #On sait que c'est la première ligne liée à "zone" qui n'a pas d'influence sur le reste
            Nb_vec=Nb_Vector_in_Zone(file)
            r=1
            if(Nb_vec>0):
                Zones[Id_Zone]['NbrVec']=Nb_vec
                IERR=read_complete_vectors(file,Zones,Nb_vec,Id_Zone)
                Id_Zone=Id_Zone+1
        if(i>2):
            Nb_vec=Nb_Vector_in_Zone(file)
            if(Nb_vec>0):
                Zones[Id_Zone]['NbrVec']=Nb_vec
                IERR=read_complete_vectors(file,Zones,Nb_vec,Id_Zone)
            Id_Zone=Id_Zone+1
    file.close()
    return Zones

#Sous-routine de calcul de distance entre deux noeuds
def distance(Node1,Node2):
    dist=((Node1[0]-Node2[0])**2+(Node1[1]-Node2[1])**2)**0.5
    return dist
# Exportation est basée sur le même type de format d'entrée utilisé pour la partie importaion : l'utilisation d'un autre format ne serait donc pas adéquat
# Chaque Vertex est décrit via son numéro de zone, numéro de vecteur, nombre de vertex le décrivant et finalement chaque vertex
def Export_vecz(Zones,filename):
    #Première phase, on vérifie que l'extension du fichier est la bonne
    Spec_char='.'
    List_sbstr=Extract_SubStrings(filename,Spec_char)
    Extent='.vecz'
    extension = os.path.splitext(filename)[1]
    if(extension!=Extent):
        print('Invalid file type')
        return False
    file = open(filename,'w')
    Next_line='\n'
    text_line='0 0'
    file.write(text_line+Next_line)
    
    NbZones=len(Zones)
    file.write(str(len(Zones))+Next_line)
    Blank='  '
    Line1='           0,           1,           0,#FALSE#,#FALSE#,#FALSE#,#FALSE#,           0,#FALSE#'
    Line2='"...",           5,       0.000000,       0.000000,#FALSE#,#FALSE#,"arial",          10,           0,#FALSE#'
    Line3='#TRUE#'
    IERR=0
   
    for i in range(NbZones):
        file.write('zone'+Next_line)
        NbVectors=0
        NbVectors=Zones[i]['NbrVec']
        if(bool(NbVectors)):
            file.write(str(NbVectors)+Next_line)
        else:
            file.write(str(0)+Next_line)
        if(bool(NbVectors)):
            for j in range(NbVectors):
                file.write(Zones[i]['Name'][j]+Next_line)
                NbrVertex=int(Zones[i]['NbrVertex'][j])
                file.write(str(Zones[i]['NbrVertex'][j])+Next_line)
                for k in range(NbrVertex):
                    CoordX=Zones[i]['Coord'][0][j][k]
                    CoordY=Zones[i]['Coord'][1][j][k]
                    CoordZ=Zones[i]['Coord'][2][j][k]
                    Coord=CoordX+Blank+CoordY+Blank+CoordZ
                    file.write(Coord+Next_line)
                test=1
                file.write(Line1+Next_line)
                file.write(Line2+Next_line)
                file.write(Line3+Next_line)
    file.close()
    return IERR

##Creation du réseau en vue de l'affichage via networkx et également sauvegarde de l'ensemble des noeuds présents au sein du réseau
##Creation du réseau en vue de l'affichage via networkx et également sauvegarde de l'ensemble des noeuds présents au sein du réseau
def Create_Network(Zones):
    myfig = plt.figure()
    ax = myfig.add_subplot(111)
    #plt.figure()
    NbZones=len(Zones)
    IERR=0
    G_loc=nx.Graph()
    List_Add_Nodes=[]
    #Création d'un dictionnaire regroupant à la fois l'ensemble des coordonnées (X,Y) des noeuds mais également des CG de chaque vecteur + numéro vecteur/noeud + Type de noeud
    List_Nodes={}
    List_Nodes['Coord']=[]
    List_Nodes['IdZone']=[]
    List_Nodes['NbrEl']=[]
    List_Nodes['TypeEl']=[]
    List_Nodes['InitNode']=[]
    Discr_Nodes={}
    Discr_Nodes['Coord']=[]
    Discr_Nodes['Pos_vertex']=[]


    Node_Prop=[0,0]
    Loc_Node=[0,0]
    cpt_node=0
    cpt_vertex=0
    cpt_loc_ver=0
    cpt_vec=1
    NbZones=len(Zones)
    Pos_Node=0
    Attr2=True
    attrib=True
    Cpt_Total_Node=1
    First_Node=0
    Last_Node=0
    Pos_lox_Node=0
    Complete_Creation=False
    Default_Type_Node='IncJunctions'
    Big_List=0
    edges=[]
    name_edges=[]
    Zone_edge=[]
    Vec_edge=[]
    start_time = time.time()
    for i in range(NbZones):
        NbVectors=Zones[i]['NbrVec']
        #NbVectors=15

        if(bool(NbVectors)):
            for j in range(NbVectors):
                #G_loc.append(nx.Graph())
                cpt_node=cpt_node+1
                NbrVertex=int(Zones[i]['NbrVertex'][j])
                edges_to_add=[]
                for k in range(NbrVertex):
                    if(k>0):
                        Previous_Coord=(float(CoordX),float(CoordY))

                    CoordX=Zones[i]['Coord'][0][j][k]
                    CoordY=Zones[i]['Coord'][1][j][k]
                    CoordZ=Zones[i]['Coord'][2][j][k]

                    Current_Coord=(float(CoordX),float(CoordY))
                    if(k>0):
                        if(Attr2):
                            Node_Test=Current_Coord
                            Attr2 = False
                        #On ajoute également dans la liste l'ensemble des CG de chaque partie de vecteur
                        CG_Coord=((Current_Coord[0]+Previous_Coord[0])/2,(Current_Coord[1]+Previous_Coord[1])/2)
                        List_Nodes['Coord'].append(CG_Coord)
                        List_Nodes['IdZone'].append(i)
                        List_Nodes['NbrEl'].append(j)
                        List_Nodes['TypeEl'].append('Vector')
                        List_Nodes['InitNode'].append(-1)
                        Last_Node=Cpt_Total_Node
                    

                    if(k==0 or (k==NbrVertex-1)):
                        New_Node=True
                        Node_Prop=(float(CoordX),float(CoordY))
                        if(len(Discr_Nodes['Coord'])>0):
                            Ind,dist=closest_node(Node_Prop, Discr_Nodes['Coord'][:])
                            if(dist<0.0001):
                                New_Node=False
                                Pos_lox_Node=Ind+1
                                test=1

                        if(New_Node):
                            cpt_vertex=cpt_vertex+1
                            Pos_Node=Pos_Node+1
                            Pos_lox_Node=Pos_Node
                            List_Nodes['Coord'].append(Current_Coord)
                            List_Nodes['IdZone'].append(-i)
                            List_Nodes['NbrEl'].append(Pos_Node)
                            List_Nodes['TypeEl'].append('Node')
                            List_Nodes['InitNode'].append(-1)
                            Discr_Nodes['Coord'].append(Current_Coord)
                            Discr_Nodes['Pos_vertex'].append(cpt_vertex)
                            G_loc.add_node(cpt_vertex,pos=(CoordX,CoordY),posz=CoordZ,Index_Node=Pos_lox_Node,Type_Node=Default_Type_Node)
                            List_Add_Nodes.append((CoordX,CoordY,CoordZ))
                            loc_vertex=cpt_vertex
                        else:
                            #Recherche de la position de vertex associée
                            loc_vertex= Discr_Nodes['Pos_vertex'][Ind]
                            test=1
                        if(k==0):
                            First_Node=loc_vertex
                        if((k==NbrVertex-1)):
                            Last_Node=loc_vertex
                            edges_to_add.append((First_Node,Last_Node))
                        #else:
                            #G_loc[nodes][Pos_lox_Node][]
                    else:
                        if(Complete_Creation):
                             cpt_vertex=cpt_vertex+1
                             Last_Node=cpt_vertex
                             G_loc.add_node(cpt_vertex,pos=(CoordX,CoordY),posz=CoordZ,Index_Node=-1,Type_Node=Default_Type_Node)
                             List_Add_Nodes.append((CoordX,CoordY,CoordZ))
                             edges_to_add.append((First_Node,Last_Node))
                             First_Node=Last_Node
            
                cpt_vec=cpt_vec+1 
                List_Tuples=int(sum(map(len, edges_to_add))/2)

                plot=edges_to_add[0]
                Vec_Name=Zones[i]['Name'][j] 
                if(Complete_Creation):
                    for s in range(List_Tuples):
                        edges.insert(Big_List,edges_to_add[s])
                        name_edges.insert(Big_List,Vec_Name)
                        Zone_edge.insert(Big_List,i)
                        Vec_edge.insert(Big_List,j)
                        Big_List=Big_List+1
                else:
                    edges.insert(Big_List,edges_to_add[0])
                    name_edges.insert(Big_List,Vec_Name)
                    Zone_edge.insert(Big_List,i)
                    Vec_edge.insert(Big_List,j)
                    Big_List=Big_List+1

                cpt_vec=cpt_vec+1


    #edges = [ (m+1, m+2) for m in range(NbrVertex-1)]
    Edges_OpenGl=edges
    G_loc.add_edges_from(edges,name=Vec_Name)
    
            
    edges = G_loc.edges()
    cpt_edge=0
    #On ajoute propriété de nom aux différents liens
    for u,v in G_loc.edges():
        Test=1
        G_loc[u][v]['Name']=name_edges[cpt_edge]
        G_loc[u][v]['Zone']=Zone_edge[cpt_edge]
        G_loc[u][v]['Vector']=Vec_edge[cpt_edge]

        cpt_edge=cpt_edge+1

    pos2=nx.get_node_attributes(G_loc,'pos')
    Ind_Node=nx.get_node_attributes(G_loc,'Index_Node')
    Nb_Nodes=G_loc.number_of_nodes()

    n_size=[]
    for n in range(Nb_Nodes):
        Index_Final=int(Ind_Node[n+1])
        if(Index_Final>0):
            n_size.append(10)
        else:
            n_size.append(0)

    #Première méthode pour les positions des edges
    pos = nx.spring_layout(G_loc)
    for n in range(Nb_Nodes):
        pos[n+1][0]=float(pos2[n+1][0])
        pos[n+1][1]=float(pos2[n+1][1])

    #Création d'un groupe pour chaque noeud
    Test=1
    for u in G_loc.nodes():
        G_loc.nodes[u]['group']=0
    for u,v in G_loc.edges():
        Test=1
        G_loc[u][v]['group']=0

    #Draw phase
    nx.draw(G_loc,pos=pos,node_size=n_size,ax=ax)

    Draw_Options=[]
    Draw_Options.append(pos)
    Draw_Options.append(n_size)
    #plt.axis('scaled')
    #plt.show()
    end_time = time.time()
    diff_time3=end_time-start_time
    Edition=False
    r=1
    return myfig,G_loc,List_Nodes,Discr_Nodes,Draw_Options,Edition,List_Add_Nodes,Edges_OpenGl


def Create_Network2(Zones):
    myfig = plt.figure()
    ax = myfig.add_subplot(111)
    plt.figure()
    NbZones=len(Zones)
    IERR=0
    G_loc=[]
    #Création d'un dictionnaire regroupant à la fois l'ensemble des coordonnées (X,Y) des noeuds mais également des CG de chaque vecteur + numéro vecteur/noeud + Type de noeud
    List_Nodes={}
    List_Nodes['Coord']=[]
    List_Nodes['IdZone']=[]
    List_Nodes['NbrEl']=[]
    List_Nodes['TypeEl']=[]
    List_Nodes['CoordZ']=[]
    Discr_Nodes={}
    Discr_Nodes['Coord']=[]

    Complete_Creation=False
    Node_Prop=[0,0]
    Loc_Node=[0,0]
    cpt_node=0
    cpt_vertex=0
    cpt_loc_ver=0
    cpt_vec=0
    NbZones=1
    Pos_Node=0
    Attr2=True
    Default_Type_Node='IncJunctions'
    start_time = time.time()
    for i in range(NbZones):
        NbVectors=Zones[i]['NbrVec']
        NbVectors=15

        if(bool(NbVectors)):
            for j in range(NbVectors):
                G_loc.append(nx.Graph())
                cpt_node=cpt_node+1
                NbrVertex=int(Zones[i]['NbrVertex'][j])
                cpt_vertex=0
                for k in range(NbrVertex):
                    if(k>0):
                        Previous_Coord=(float(CoordX),float(CoordY))

                    CoordX=Zones[i]['Coord'][0][j][k]
                    CoordY=Zones[i]['Coord'][1][j][k]
                    CoordZ=Zones[i]['Coord'][2][j][k]

                    Current_Coord=(float(CoordX),float(CoordY))
                    if(k>0):
                        if(Attr2):
                            Node_Test=Current_Coord
                            Attr2 = False
                        CG_Coord=((Current_Coord[0]+Previous_Coord[0])/2,(Current_Coord[1]+Previous_Coord[1])/2)
                        List_Nodes['Coord'].append(CG_Coord)
                        List_Nodes['IdZone'].append(i)
                        List_Nodes['NbrEl'].append(j)
                        List_Nodes['TypeEl'].append('Vector')
                        List_Nodes['CoordZ'].append(CoordZ)
                    Pos_lox_Node=0

                    if(k==0 or (k==NbrVertex-1)):
                        cpt_vertex=cpt_vertex+1
                        New_Node=True
                        Node_Prop=(float(CoordX),float(CoordY))
                        if(len(Discr_Nodes['Coord'])>0):
                            Ind,dist=closest_node(Node_Prop, Discr_Nodes['Coord'][:])
                            if(dist<0.0001):
                                New_Node=False
                                Pos_lox_Node=Ind

                        if(New_Node):
                                Pos_Node=Pos_Node+1
                                Pos_lox_Node=Pos_Node
                                List_Nodes['Coord'].append(Current_Coord)
                                List_Nodes['IdZone'].append(-i)
                                List_Nodes['NbrEl'].append(Pos_Node)
                                List_Nodes['TypeEl'].append('Node')
                                List_Nodes['CoordZ'].append(CoordZ)
                                Discr_Nodes['Coord'].append(Current_Coord)
                        G_loc[cpt_vec].add_node(cpt_vertex,pos=(CoordX,CoordY),posz=CoordZ,Index_Node=Pos_lox_Node,Type_Node=Default_Type_Node)
                    else:
                        if(Complete_Creation):
                            cpt_vertex=cpt_vertex+1
                            G_loc[cpt_vec].add_node(cpt_vertex,pos=(CoordX,CoordY),posz=CoordZ,Type_Node=Default_Type_Node)
                        
  
                if( Complete_Creation):
                    edges = [ (m+1, m+2) for m in range(NbrVertex-1)]
                else:
                    edges = [(1, 2)]
                Vec_Name=Zones[i]['name'][j]    
                G_loc[cpt_vec].add_edges_from(edges,name=Vec_Name)

                pos2=nx.get_node_attributes(G_loc[cpt_vec],'pos')
                Nb_Nodes=G_loc[cpt_vec].number_of_nodes()

                n_size=[]
                for n in range(Nb_Nodes):
                    if(n==0 or (n==Nb_Nodes-1)):
                        n_size.append(10)
                    else:
                        n_size.append(0)

                #Première méthode pour les positions des edges
                pos = nx.spring_layout(G_loc[cpt_vec])
                for n in range(Nb_Nodes):
                    pos[n+1][0]=float(pos2[n+1][0])
                    pos[n+1][1]=float(pos2[n+1][1])

                nx.draw(G_loc[cpt_vec],pos=pos,node_size=n_size,ax=ax)
               
                cpt_vec=cpt_vec+1

    plt.axis('scaled')
    #plt.show()
    end_time = time.time()
    diff_time3=end_time-start_time
    Index=closest_node(Node_Test,  List_Nodes['Coord'][:])
    r=1
    return myfig,List_Nodes

#Sous-routine  ayant pour but d'afficher les résultats selon le choix de paramètres effectué par l'utilisateur
def Show_Results(G_loc,Draw_Options,Param_Simul,Zones,Nodes,Timing):
    plt.clf()
    myfig = plt.figure()
    ax = myfig.add_subplot(111)
    Choices=['HeadNodes','Altimetry','Discharge','Diameter']
    #plt.figure()
    cpt_choices=-1
    pos=Draw_Options[0]
    n_size=Draw_Options[1]
    Attr_Node=False
    Attr_Vector=False
    for Loc_Choice in Choices:
        cpt_choices=cpt_choices+1
        if(Param_Simul[cpt_choices]==1):
 
            #Réinitilisation des groupes
            #Réévaluation du Timing à prendre en compte
            #Méthode des valeurs aux noeuds
            if(cpt_choices<2):
                if(not(Attr_Node)):
                    Test=1
                    for u in G_loc.nodes():
                        G_loc.nodes[u]['group']=0
                        G_loc.nodes[u]['value']=0
                    G_loc=Set_Up_Node_Values(G_loc,Nodes,'Reservoirs',cpt_choices,Timing)
                    G_loc=Set_Up_Node_Values(G_loc,Nodes,'IncJunctions',cpt_choices,Timing)
                    values=Prepare_Node_Values(G_loc)
                    MinVal=min(values)
                    MaxVal=max(values)
                    Attr_Node=True
            else:
                if(not(Attr_Vector)):
                    for u,v in G_loc.edges():
                        G_loc[u][v]['group']=0
                        G_loc[u][v]['value']=0
                    G_loc,values=Set_Up_Vector_Values(G_loc,Zones,cpt_choices,Timing)
                    MinValV=min(values)
                    MaxValV=max(values)
                    Attr_Vector=True
                    #ec = nx.draw_networkx_edges(G_loc, pos=pos, alpha=0.5,ax=ax)
                    #cb2=plt.colorbar(ec)
                    #cb2.ax=ax
                    
                #nx.draw(G_loc,pos=pos,node_size=n_size,ax=ax)
        #cb1=plt.colorbar(nc)
        #cb1.ax=ax
# extract nodes with specific setting of the attribute


    if(Attr_Node):
        nc = nx.draw_networkx_nodes(G_loc, cmap=plt.get_cmap('RdYlGn'),pos=pos,node_size=Draw_Options[3], node_color=values,vmin=MinVal,vmax=MaxVal,ax=ax, node_shape='o',nodelist=Draw_Options[2])
        nc = nx.draw_networkx_nodes(G_loc, cmap=plt.get_cmap('RdYlGn'),pos=pos,node_size=Draw_Options[5], node_color=values,vmin=MinVal,vmax=MaxVal,ax=ax, node_shape='s',nodelist=Draw_Options[4])
        #cb2=plt.colorbar(nc)
        #cb2.ax=ax
        #cb2.set_label('[m]')
    else:
        nc = nx.draw_networkx_nodes(G_loc, pos=pos, alpha=0.5,ax=ax,node_size=Draw_Options[3], node_shape='o',nodelist=Draw_Options[2])
        nc = nx.draw_networkx_nodes(G_loc, pos=pos, alpha=0.5,ax=ax,node_size=Draw_Options[5], node_shape='s',nodelist=Draw_Options[4])
    if(Attr_Vector):
        ec = nx.draw_networkx_edges(G_loc, edge_cmap=plt.get_cmap('RdYlGn'),pos=pos, edge_color=values,edge_vmin=MinValV,edge_vmax=MaxValV,ax=ax)
        #ec = nx.draw_networkx_edges(G_loc, edge_cmap=plt.get_cmap('RdYlGn'),pos=pos, edge_color=values)
        ec.cmap = plt.get_cmap('RdYlGn')
        ec.set_clim(MinValV,MaxValV)
        cb2=plt.colorbar(ec)
        cb2.ax=ax
    else:
        ec = nx.draw_networkx_edges(G_loc, pos=pos, alpha=0.5,ax=ax)
    #Méthode des groupes
    if(Param_Simul==278):
        groups = set(nx.get_node_attributes(G_loc,'group').values())
        mapping = dict(zip(sorted(groups),count()))
        nodes = G_loc.nodes()
        colors = [mapping[G_loc.nodes[n]['group']] for n in nodes]

        # drawing nodes and edges separately so we can capture collection for colobar
        ec = nx.draw_networkx_edges(G_loc, pos, alpha=0.2, ax=ax)
        nc = nx.draw_networkx_nodes(G_loc, pos, node_size=n_size, nodelist=nodes, node_color=colors, cmap=plt.cm.jet,ax=ax)


    #plt.axis('scaled')
    #myfig.colorbar=cb2
    plt.show()
    Test=1
    return myfig

#Sous-routine en complément de Show_Results pour préparer selon chaque type de noeud : à compléter par la suite via les bons choix de valeur
def Set_Up_Node_Values(G_loc,Nodes,Node_Type,Param_Simul,Timing):
    Nb_Node=len(Nodes[Node_Type]['Name'])
    for u in range(Nb_Node):
        Ind_Pos=Nodes[Node_Type]['IndPos'][u]
        if(Param_Simul==0):
            G_loc.nodes[Ind_Pos]['value']=Nodes[Node_Type]['ValueH'][u][Timing]
        if(Param_Simul==1):
            G_loc.nodes[Ind_Pos]['value']=Nodes[Node_Type]['CoordZ'][u]
        Test=1
    return G_loc
#Préparation finale pour la mise en place des informations
def Prepare_Node_Values(G_loc):
    values = []
    cpt_elem=0
    for u in G_loc.nodes():
        cpt_elem=cpt_elem+1
        Loc_Val=G_loc.nodes[u]['value']+float(cpt_elem)/float(1000000000)
        values.append(Loc_Val)
        if(G_loc.nodes[u]['value']==0):
            Test=1
    return values

#Sous-routine parallèle utilisée pour les tronçons cette fois
def Set_Up_Vector_Values(G_loc,Zones,Param_Simul,Timing):
    values = []
    cpt_elem=0
    Timing=Timing-1
    for u,v in G_loc.edges():
        cpt_elem=cpt_elem+1
        Test=1
        Loc_Name=G_loc[u][v]['Name']
        Loc_Zone=G_loc[u][v]['Zone']
        Loc_Vec=G_loc[u][v]['Vector']
        if(Param_Simul==3):
            Diam=Zones[Loc_Zone]['Diameter'][Loc_Vec]
            Diam=float(Diam)+float(cpt_elem)/float(1000000)
            values.append(Diam)
        if(Param_Simul==2):
            Dis=Zones[Loc_Zone]['Value'][Loc_Vec][Timing]
            Dis=abs(float(Dis))+float(cpt_elem)/float(10000000)
            values.append(Dis)
    return G_loc,values
#Sous-routine permettant d'identifier l'index du noeud le plus proche d'une liste 
#node tuple de type (x,y) 
# nodes liste de tuple de type [(x1,y1),(x2,y2),...]
def closest_node(node, nodes):
    nodes = np.asarray(nodes)
    deltas = nodes - node
    dist_2 = np.einsum('ij,ij->i', deltas, deltas)
    return np.argmin(dist_2),min(dist_2)

#Lecture ligne à ligne du fichier de paramètres ayant été établi
def Read_Param_file(ParamFile):
    Param={}
    Category_Name=['Time','Gen_Param','Optimization']
    Param[Category_Name[0]]={}
    Param[Category_Name[1]]={}
    Param[Category_Name[2]]={}
    #Préparation des différentes catégories de paramètres proposés
    Max_categories=2
    Category_Sentence=['Time :','General Parameters of the network :','IPOPT Optimization Parameters :']
    file = open(ParamFile,'r')
    ctgr=-1
    i=0
    Special_Character='%'
    for New_Word in file:
        #Première partie liée aux informations génériques pour compléter ainsi le dictionnaire de Vecteurs
        i=i+1
        New_Word=New_Word.rstrip('\n')
        New_Word=New_Word.lstrip()
        if(New_Word[0]!=Special_Character):
            loc_cat=ctgr+1
            if(loc_cat>Max_categories):
                loc_cat=0
            if(Category_Sentence[loc_cat]==New_Word):
                ctgr=ctgr+1
            else:
                New_Word = New_Word.split('\t')    # string.whitespace contains all whitespace.
                Param[Category_Name[ctgr]][New_Word[0]]=[]
                Param[Category_Name[ctgr]][New_Word[0]].append(New_Word[1])
                Param[Category_Name[ctgr]][New_Word[0]].append(New_Word[2])
                Test=1
        else:
            Test=1
    return Param
#Sous-routine dédiée à obtenir l'ensemble des informations disponibles sur les noeuds présentes dans le dossier du réseau
def Import_Nodes_Attributes(namepath,Graph,List_Nodes,Draw_Option,Param):
    ## Première étape est d'obtenir le réel chemin d'accès aux fichiers géométriques de noeuds
    #Dossier Principal
    MainDir = os.path.dirname(namepath)
    MainDir = MainDir+'\\'
    Nodes={}
    Nodes['Reservoirs']={}
    Nodes['IncJunctions']={}
    #Fichier géométrique
    GeomNodes=MainDir+'Reservoirs.vecr'
    Nodes['Reservoirs']=Read_Geom_Nodes(GeomNodes)
    GeomNodes=MainDir+'Extra_data_Junctions.jun'
    Nodes['IncJunctions']=Read_Geom_Nodes(GeomNodes)
    #Comparaison à effectuer entre la liste de noeuds et les différents noeuds pour numéroter
    i=0
    Type_Node='Reservoirs'
    Test=Define_Node_Pos(Nodes['Reservoirs'],List_Nodes)
    Type_Node='IncJunctions'
    Test=Define_Node_Pos(Nodes['IncJunctions'],List_Nodes)
    #On ajoute à présent dans les noeuds définis l'ensemble des noeuds qui ne se trouvaient pas dans la liste géométrique des noeuds intéressants
    Test=Add_Common_Nodes(Nodes['IncJunctions'],List_Nodes)
    #Recherche des différents attributs importants pour les réservoirs 
    RsrvDir=MainDir+'Reservoirs\\'
    List_Attr=['Section','Max_H','Min_H','IC_V']
    Attr_File=['SECTION.D','Max_Height.D','Minimum_H.D','IC_Reservoir.D']
    Test=Add_Node_Attributes(Nodes['Reservoirs'],RsrvDir,List_Attr,Attr_File)
    #On ajoute également les données temporelles de résultat du réseau
    Nodes=Add_Node_Time(Nodes,'Reservoirs',RsrvDir,Param)
    JuncDir=MainDir+'Extra_data_Junctions\\'
    Nodes=Add_Node_Time(Nodes,'IncJunctions',JuncDir,Param)
    #On va finalement regarder aux différents noeuds de Graph afin d'adopter le type réel de chaque noeud présent dans le réseau tout en modifiant la partie des dessins
    n_size=Draw_Option[1]
    for Ind_Pos in Nodes['Reservoirs']['IndPos']:
        Graph.nodes[Ind_Pos]['Type_Node']='Reservoirs'
        Test=1
    #On peut donc particulariser l'analyse des noeuds et surtout leur affichage selon les jonctions incompressibles d'un côté et les réservoirs de l'autre
    Junction_Nodes=[n for (n,ty) in nx.get_node_attributes(Graph,'Type_Node').items() if ty == 'IncJunctions']
    Junction_Size=[]
    for (n,ty) in nx.get_node_attributes(Graph,'Type_Node').items():
        if ty == 'IncJunctions':
            Junction_Size.append(n_size[n-1])
            Test=1
    Reservoir_Nodes=[n for (n,ty) in nx.get_node_attributes(Graph,'Type_Node').items() if ty == 'Reservoirs']
    Reservoir_Size=[]
    for (n,ty) in nx.get_node_attributes(Graph,'Type_Node').items():
        if ty == 'Reservoirs':
            n_size[n-1]=60
            Reservoir_Size.append(n_size[n-1])

    Draw_Option.append(Junction_Nodes)
    Draw_Option.append(Junction_Size)
    Draw_Option.append(Reservoir_Nodes)
    Draw_Option.append(Reservoir_Size)
    return Nodes,Graph,Draw_Option
#Sous-routine dédiée à obtenir l'ensemble des informations disponibles sur les tronçons présents dans le dossier du réseau
def Import_Vector_Attributes(namepath,Zones,Param):
    Test=1
    ## Première étape est d'obtenir le réel chemin d'accès aux fichiers géométriques de noeuds
    #Dossier Principal
    MainDir = os.path.dirname(namepath)
    MainDir = MainDir+'\\'
    Vectors={}
    Vectors['Pipes']={}
    Vectors['Valves']={}
    Vectors['Pumps']={}
    LocDir=MainDir+'Network_Vectors\\'
    #Partie Pipes
    List_Attr=['Diameter','Length','Rough_Coeff','Material','IC_Cond']
    Attr_File=['Diameter.D','Length.D','Rugosity.D','Material.S','IC_Vector.D']
    Zones=Add_Vector_Attributes(Zones,LocDir,List_Attr,Attr_File)
    #On va également rechercher à sauvegarder l'ensemble des résultats sur les différents pas de temps du réseau
    Zones=Add_Vector_Time(Zones,LocDir,Param)
    return Zones
def Define_Node_Pos(Nodes,List_Nodes):
    
    i=0
    for Coord in Nodes['CoordPlan']:
        #On fait la recherche dans la liste des noeuds établis en s'assurant que la relation soit bien acceptable
        Index,dist=closest_node(Coord, List_Nodes['Coord'][:])
        if(dist<0.1):
            Nodes['IndPos'][i]=List_Nodes['NbrEl'][Index]
            test=1
            List_Nodes['InitNode'][Index]=0
        else:
            print('Node %s is not connected to the network' % Nodes['Name'][i])
        test=1
        i=i+1

    return test
#Lecture d'un fichier géométrique de noeuds
def Read_Geom_Nodes(FilePath):
    #Initialisation
    Nodes={}
    Nodes['Name']=[]
    Nodes['CoordPlan']=[]
    Nodes['CoordZ']=[]
    Nodes['IndPos']=[]
    #Lecture du fichier
    file = open(FilePath,'r')
    Special_char=','
    i=0
    for New_Word in file:
        #Première partie liée aux informations génériques pour compléter ainsi le dictionnaire de Vecteurs
        i=i+1
        New_Word=New_Word.rstrip('\n')
        if(i>1):
            Words=Extract_SubStrings(New_Word,Special_char)
            Nodes['Name'].append(Words[3])
            Nodes['CoordPlan'].append((float(Words[0]),float(Words[1])))
            Nodes['CoordZ'].append(float(Words[2]))
            Nodes['IndPos'].append(-1)
            test=2

    return Nodes
#Ajout de l'ensemble des noeuds qui ne se retrouvent pas dans liste géométrique
def Add_Common_Nodes(Nodes,List_Nodes):
    New_Node='Add_Node'
    cpt_add_node=0
    i=0
    test=1
    for Local_Node in List_Nodes['TypeEl']:
        if(List_Nodes['InitNode'][i]==-1 and List_Nodes['TypeEl'][i]=='Node'):
            cpt_add_node=cpt_add_node+1
            Loc_Name_Node=New_Node+str(cpt_add_node)
            Nodes['Name'].append(Loc_Name_Node)
            Nodes['CoordPlan'].append((float(List_Nodes['Coord'][i][0]),float(List_Nodes['Coord'][i][1])))
            Nodes['CoordZ'].append(float(List_Nodes['CoordZ'][i]))
            Nodes['IndPos'].append(List_Nodes['NbrEl'][i])
        i=i+1
    return test
#Ajout des différents attributs pertinents des réservoirs dans le réseau
def Add_Node_Attributes(El_List,MainDir,List_Attr,Attr_File):
    Spec_char=','
    Cpt_attrib=-1
    for Attr in List_Attr:
        Cpt_attrib=Cpt_attrib+1
        filename=MainDir+Attr_File[Cpt_attrib]
        File_To_Read=os.path.isfile(filename)
        if(File_To_Read):
            file = open(filename,'r')
            El_List[Attr]=[]
            for Element in El_List['Name']:
                El_List[Attr].append('X')
            i=0
            for New_Word in file:
                #Première partie liée aux informations génériques pour compléter ainsi le dictionnaire de Vecteurs
                i=i+1
                New_Word=New_Word.rstrip('\n')
                if(i>=2):
                    List_sbstr=Extract_SubStrings(New_Word,Spec_char)
                    Loc_cpt=0
                    for Element in El_List['Name']:
                        if(Element==List_sbstr[0]):
                            El_List[Attr][Loc_cpt]=List_sbstr[1]
                            break
                        Loc_cpt=Loc_cpt+1
        else:
            print('The following file does not exist : %s' % filename)

    return El_List

#Partie liée aux attributs cette fois pour les différents types de vecteurs
def Add_Vector_Attributes(Zones,MainDir,List_Attr,Attr_File):
    Cpt_attrib=-1
    for Attr in List_Attr:
        Cpt_attrib=Cpt_attrib+1
        filename=MainDir+Attr_File[Cpt_attrib]
        File_To_Read=os.path.isfile(filename)
        if(File_To_Read):
            file = open(filename,'r')
            Nb_Zones=len(Zones)
            ValFix=[]
            for i in range(Nb_Zones):
                ValFix.append(-1)

            i=0
            for New_Word in file:
                #Première partie liée aux informations génériques pour compléter ainsi le dictionnaire de Vecteurs
                i=i+1
                New_Word=New_Word.rstrip('\n')
                #Ligne décomposée en trois parties : numéro de zone, vecteur puis valeur de l'attribut
                List_sbstr=New_Word.split()
                Numero_Zone=int(List_sbstr[0])-1
                if(ValFix[Numero_Zone]==-1):
                    ValFix[Numero_Zone]=0
                    Zones[Numero_Zone][Attr]=[]
                    for Element in Zones[Numero_Zone]['Name']:
                        Zones[Numero_Zone][Attr].append('X')
                Numero_Vec=int(List_sbstr[1])-1
                Zones[Numero_Zone][Attr][Numero_Vec]=List_sbstr[2]
        else:
            print('The following file does not exist : %s' % filename)

    return Zones

#On va ajouter cette fois les valeurs à chaque pas de temps afin de permettre la représentation des résultats à chaque pas de temps
def Add_Vector_Time(Zones,LocDir,Param):
    local_file=['PIPE_FIRST_DIS.pidb','PUMP_FIRST_DIS.pudb','VALVE_FIRST_DIS.vadb']

    for Id_Zone in range(len(Zones)):
        filename=LocDir+local_file[Id_Zone]
        if(os.path.isfile(filename)):
            file = open(filename,'r')
            Zones[Id_Zone]['Value']=[]
            Special_char=','
            Nb_Time=int(Param['Time']['Type of time network evaluation'][0])
            Nb_total_Time=int(Param['Time']['Number of time used steps'][0])
            for New_Word in file:
                New_Word=New_Word.strip('\n')
                New_Word=Extract_SubStrings(New_Word,Special_char)
                NbVec=int(New_Word[1])-1
                Zones[Id_Zone]['Value'].append([])
                cpt_elem=0
                for k in range(Nb_total_Time):
                    Value=file.readline().rstrip('\n')
                    cpt_elem=cpt_elem+1
                    if(cpt_elem<=Nb_total_Time):
                        Zones[Id_Zone]['Value'][NbVec].append(float(Value))
                Test=1

    Test=1
    return Zones

def Add_Node_Time(Nodes,Type_Node,LocDir,Param):
    LocFile=LocDir+'CHR_FIRST_VAL.D'
    #On cherche uniquement à conserver la charge, il faut donc transformer le volume en charge
    file = open(LocFile,'r')
    p_atmospheric=10.3261977573904
    Nodes[Type_Node]['ValueH']=[]
    Special_char=','
    Nb_Time=int(Param['Time']['Type of time network evaluation'][0])
    Nb_total_Time=int(Param['Time']['Number of time used steps'][0])
    #Première partie dédiée à la construction pour chaque noeud de sa propre liste
    Nb_Nodes=len(Nodes[Type_Node]['Name'])
    Nb_Nodes2=file.readline().rstrip('\n')
    for i in range(Nb_Nodes):
        Nodes[Type_Node]['ValueH'].append([])
    for New_Word in file:
        #On accède à ce moment au nom de l'élément
        New_Word=New_Word.strip('\n')
        cpt_elem=0
        #On doit d'abord s'assurer d'identifier correctement l'information
        for Pos_Node in range(Nb_Nodes):
            if(Nodes[Type_Node]['Name'][Pos_Node]==New_Word):
                for k in range(Nb_total_Time):
                    Value=file.readline().rstrip('\n')
                    cpt_elem=cpt_elem+1
                    if(cpt_elem<=Nb_total_Time):
                        if(Type_Node=='Reservoirs'):
                            Alt=float(Nodes[Type_Node]['CoordZ'][Pos_Node])
                            Section=float(Nodes[Type_Node]['Section'][Pos_Node])
                            Value=float(Value)/Section+Alt+p_atmospheric
                            Test=1
                        Nodes[Type_Node]['ValueH'][Pos_Node].append(float(Value))
                break
        Test=1

    Test=1
    return Nodes
#Ajout des différents attributs princopaux devant être montrés à l'utilisateur
def Add_Main_Attributes(Zones):
    Nb_Zones=len(Zones)
    Zones[0]['Princ_Attrib']=['Name','Diameter','Length','Rough_Coeff','Material','IC_Cond']
    if(Nb_Zones==2):
        Zones[1]['Princ_Attrib']=['Name','Diameter','Length','Rough_Coeff','Material','IC_Cond']
    else:
        if(Nb_Zones==3):
            Zones[1]['Princ_Attrib']=['Name','Diameter','Length','Rough_Coeff','Material','IC_Cond']
            Zones[2]['Princ_Attrib']=['Name','Diameter','Length','Rough_Coeff','Material','IC_Cond']
#filename='D:\\ProgThomas\\wolf_oo\Sources-Thomas3\\Solutions\\Unit_Tests\\to_debug\\Jock_Basic\\Network_Vectors.vecz'
#Zones=Import_vecz(filename)
#IERR=Create_Network(Zones)

    return Zones
app = wx.App()
ex = Window_Test(None)
ex.Show()
app.MainLoop()
v=np.array([1, 2, 3])
IERR=Create_Network(Zones)
filename='D:\\ProgThomas\\wolf_oo\Sources-Thomas3\\Solutions\\Unit_Tests\\to_debug\\Network_Vectors_2.vecz'
IERR=Export_vecz(Zones,filename)
r=i
G=nx.Graph()
G.add_node(1,pos=(0.5,2))
G.add_node(2,pos=(1,3))
G.add_edge(1,2)
pos=nx.get_node_attributes(G,'pos')
nx.draw(G,pos=pos)
plt.show()


