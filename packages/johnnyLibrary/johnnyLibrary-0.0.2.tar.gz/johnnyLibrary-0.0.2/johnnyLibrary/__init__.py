from PCpranks import shutdownPC
from CalIPv4 import kal_IP_GUI, VLSM_GUI

def shutdown():
    shutdownPC.main()

def calIPv4():
    kal_IP_GUI.root.mainloop()

def vlsm():
    VLSM_GUI.root.mainloop()
