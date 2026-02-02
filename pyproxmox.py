# ***************************************************************
# ***************************************************************
# ***************************************************************
# 
#      respository: https://github.com/marcosTGit/pyproxmox
#      Author: https://github.com/marcosTGit
#
# ***************************************************************
# ***************************************************************
# ***************************************************************
# ***************************************************************



import requests
import urllib3
urllib3.disable_warnings()

# Cargar variables del archivo .env
import os
from dotenv import load_dotenv
load_dotenv()


class Promox(): 
    
    # 000000000000000000000000000000000000000000000000000000000000000000000000000000000
    # 000000000000000000000000000000000000000000000000000000000000000000000000000000000
    # 000000000000000000000000000000000000000000000000000000000000000000000000000000000
    def __init__(self):
        # INICIALIZAMOS LAS LA CLASE
        self.data={}
        self.vm_id=False
        self.proxmoxhost=os.getenv('PROXMOX_HOST')
        self.username=os.getenv('USER_NAME')
        self.password=os.getenv('PASSWORD')
        self.nodename=os.getenv('NODENAME')
        self.uri = f"https://{self.proxmoxhost}:8006/api2/json/access/ticket" # url para crear la sesion sesion 
        self.ticketrequestbody = {
            "username": self.username,
            "password": self.password
        }
        self.headers = { "Content-Type": "application/x-www-form-urlencoded"}
        

        
        try:   
            self.ticketresponse = requests.post(self.uri, verify=False, data= self.ticketrequestbody, headers= self.headers)
            if self.ticketresponse.status_code == 200:
                try:
                    self.ticketdata = self.ticketresponse.json()
                    
                except ValueError:
                    self.data['errors']={"Error": "Unable to parse JSON response"}
            else:
                self.data['errors']={f"Request failed with status code {self.ticketresponse.status_code}"}

            self.ticket = self.ticketdata['data']['ticket']
            self.CSRFPreventionToken = self.ticketdata['data']['CSRFPreventionToken']
        except:
            self.data['errors']={ "Error":"ticket request failed" }
            return self.data
        
        self.session = requests.Session()
        self.session.cookies.set('PVEAuthCookie', self.ticket)
        self.apiheaders = { 'CSRFPreventionToken': self.CSRFPreventionToken }
        
    
    # 000000000000000000000000000000000000000000000000000000000000000000000000000000000
    # 000000000000000000000000000000000000000000000000000000000000000000000000000000000
    # 000000000000000000000000000000000000000000000000000000000000000000000000000000000
    # 000000000000000000000000000000000000000000000000000000000000000000000000000000000
    # 000000000000000000000000000000000000000000000000000000000000000000000000000000000
    def getVersion (self):
        # 000000000000000000000000000000000000000000000000000000000000
        # intentamos obenter la version 
        # 000000000000000000000000000000000000000000000000000000000000
        
        self.url_version = f"https://{self.proxmoxhost}:8006/api2/json/version"
        try:
            response_version = self.session.get(self.url_version, headers=self.apiheaders, verify=False)
        except:
            self.data['errors']={"Error": "API Request  version Failed" }
            return self.data

        
        if response_version.status_code == 200:
            versioninfo = response_version.json()
            pveversion = versioninfo['data']['version']
            self.data['version']=pveversion
        
        else:
            self.data['errors']={ "Error": f"API request failed with status code {response_version.status_code}"}
        return self.data
    
    

    
    # 000000000000000000000000000000000000000000000000000000000000000000000000000000000
    # 000000000000000000000000000000000000000000000000000000000000000000000000000000000
    # 000000000000000000000000000000000000000000000000000000000000000000000000000000000
    # 000000000000000000000000000000000000000000000000000000000000000000000000000000000

    def getInfoVMI(self, vm_id=False, path='status/current'):        
        # 000000000000000000000000000000000000000000000000000000000000
        # intentamos obenter el estado de la vm_id accion por defecto  'status/current'
        # 000000000000000000000000000000000000000000000000000000000000
        
        def Convertir_MG_GB(mb):
            valorGB=1024*1024*1024
            return round(mb / valorGB, 2)
        
        
        def ObtenerPorcetajeDeUso(maxmem, mem):
            return round(((mem / maxmem) * 100), 1)
        
        
        # 000000000000000000000000000000000000000000000000000000000000
        # 000000000000000000000000000000000000000000000000000000000000
        # 000000000000000000000000000000000000000000000000000000000000
        
        if vm_id:
            baseuri = f"https://{self.proxmoxhost}:8006/api2/json/nodes/{self.nodename}/qemu/{vm_id}/{path}"
            
            try:
                response_init = self.session.get(baseuri, headers=self.apiheaders, verify=False)
            except:
                self.data['errors']={"Error": "API Request nodes Failed"}
                return self.data

            if response_init.status_code == 200:
                vmstatusinfo = response_init.json()
                vmstatus = vmstatusinfo['data']['qmpstatus']
                self.data['qmpstatus']=vmstatusinfo['data']
        
            else:
                self.data['errors']={ "Error": f"API request failed with status code {response_init.status_code} o la maquina virtual no existe" }
                return self.data
            
            if vmstatus != "running":
                dostartup = False
                if vmstatus == "paused":
                    baseuri = f"https://{self.proxmoxhost}:8006/api2/json/nodes/{self.nodename}/qemu/{vm_id}/status/resume"
                    dostartup = True
                elif vmstatus == "stopped":
                    baseuri = f"https://{self.proxmoxhost}:8006/api2/json/nodes/{self.nodename}/qemu/{vm_id}/status/start"
                    dostartup = True
                else:
                    self.data['info']={ "mensaje" : "VM not detected as running but not in paused or stopped state - no action taken." }

                if dostartup == True:
                    startbody = {
                    "node": self.nodename,
                    "vmid": vm_id
                    }
                    
                    try:
                        response = self.session.post(baseuri, headers=self.apiheaders, verify=False)
                    except:
                        self.data['errors']={"Error: API Request Failed"}
                        return self.data
                        
                    
                    if response.status_code == 200:
                        runstateinfo = response.json()
                        runstate = runstateinfo['data']
                        self.data ['data']['runstateinfo']=runstate
        
                    else:
                        self.data['errors']={ "Error" : f"API request failed with status code {response.status_code}" }
                        return self.data
                    
        # esta lineas son para darle formato a los datos obtenidos
        self.data['qmpstatus']['resources']={}
        self.data['qmpstatus']['resources']['mem_use']=Convertir_MG_GB(self.data['qmpstatus']['mem'])  # MEMORIA EN USO 
        self.data['qmpstatus']['resources']['mem_available']=Convertir_MG_GB(self.data['qmpstatus']['maxmem']) # MEMORIA DISPONNIBLE
        self.data['qmpstatus']['resources']['mem_free']=Convertir_MG_GB(self.data['qmpstatus']['freemem']) # MEMORIA LIBRE
        self.data['qmpstatus']['resources']['mem_use_per']=ObtenerPorcetajeDeUso(self.data['qmpstatus']['maxmem'], self.data['qmpstatus']['mem'] ) # MEMORIA LIBRE
        return self.data
        


    # 000000000000000000000000000000000000000000000000000000000000000000000000000000000
    # 000000000000000000000000000000000000000000000000000000000000000000000000000000000
    # 000000000000000000000000000000000000000000000000000000000000000000000000000000000
    

px=Promox()

datos=px.getInfoVMI(105)

print(datos['qmpstatus']['resources'])

# for d in datos['qmpstatus']:
#     print(f"\t{d}:\t {datos['qmpstatus'][d]}")

