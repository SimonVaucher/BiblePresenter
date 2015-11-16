
desk = QDesktopWidget()
desk.screenGeometry(0) # main screenGeometry
desk.screenGeometry(1) # secondary screenGeometry

desk.screenCount() # Duh

bla.txtView.setDocument(anotherBla.txtView.document())

one QWidget >> presenter
second QWidget >> "viewPort"

inside the OTHER widget (full screen, secondary screen):
>> self.setWindowFlags(Qt.FramelesssWindowHint)

when showing viewport:
>> self.viewport.move(desk.screenGeometry(1).topLeft()) # important
>> self.viewport.showFullScreen() # no reason to fiddle with it, it is a presenter

