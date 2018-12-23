'''
     Data: CO hourly level (ppm) data for year 2017 across counties in United States
     Data source: United States Environmental Protection Agency (EPA)
     Data source url: https://aqs.epa.gov/aqsweb/airdata/download_files.html#Raw
'''


PACKET={'Data':{'destination':'dummy'}}
HOST='10.0.0.18'
PORT=8081
CONTROLLER_ADDR='http://6fae1c03.ngrok.io'
DATA_FILE="data_files/HOURLY_DATA.csv"
DATA_FILE_DIR="data_files/"
LOC_FILE_DIR="loc_files/"
CLOUD_ADDR=""

TEST_DF=["Ramsey.txt","Jefferson.txt","Hennepin.txt","Anoka.txt","Minnehaha.txt"]


DATA_POINT_COUNT=500

FILE_NAMES=['Jefferson.txt', 'Anchorage .txt', 'Fairbanks North Star .txt', 'La Paz.txt', 'Maricopa.txt',
'Pima.txt', 'Pulaski.txt', 'Alameda.txt', 'Butte.txt', 'Contra Costa.txt', 'Fresno.txt', 'Humboldt.txt', 
'Imperial.txt', 'Inyo.txt', 'Kern.txt', 'Los Angeles.txt', 'Madera.txt', 'Marin.txt', 'Monterey.txt', 
'Napa.txt', 'Orange.txt', 'Riverside.txt', 'Sacramento.txt', 'San Bernardino.txt', 'San Diego.txt', 'San Francisco.txt', 
'San Joaquin.txt', 'San Mateo.txt', 'Santa Barbara.txt', 'Santa Clara.txt', 'Solano.txt', 'Sonoma.txt', 'Stanislaus.txt', 
'Sutter.txt', 'Adams.txt', 'Denver.txt', 'El Paso.txt', 'La Plata.txt', 'Larimer.txt', 'Mesa.txt', 'Weld.txt', 'Fairfield.txt',
'Hartford.txt', 'Litchfield.txt', 'New Haven.txt', 'New Castle.txt', 'District of Columbia.txt', 'Broward.txt', 'Duval.txt', 
'Hillsborough.txt', 'Miami-Dade.txt', 'Pinellas.txt', 'Wakulla.txt', 'DeKalb.txt', 'Fulton.txt', 'Honolulu.txt', 'Ada.txt',
'Champaign.txt', 'Cook.txt', 'Saint Clair.txt', 'Lake.txt', 'Marion.txt', 'Vanderburgh.txt', 'Linn.txt', 'Polk.txt', 'Scott.txt',
'Wyandotte.txt', 'Edmonson.txt', 'East Baton Rouge.txt', 'Orleans.txt', 'Aroostook.txt', 'Cumberland.txt', 'Hancock.txt', 
'Baltimore.txt', 'Dorchester.txt', 'Garrett.txt', 'Howard.txt', 'Essex.txt', 'Hampden.txt', 'Suffolk.txt',
'Worcester.txt', 'Kent.txt', 'Wayne.txt', 'Anoka.txt', 'Dakota.txt', 'Hennepin.txt', 'Ramsey.txt', 'Hinds.txt', 'Jackson.txt', 
'St. Louis City.txt', 'Gallatin.txt', 'Lewis and Clark.txt', 'Douglas.txt', 'Clark.txt', 'Washoe.txt', 'Rockingham.txt', 'Bergen.txt',
'Camden.txt', 'Hudson.txt', 'Union.txt', 'Bernalillo.txt', 'Albany.txt', 'Bronx.txt', 'Erie.txt', 'Monroe.txt', 'New York.txt',
'Queens.txt', 'Steuben.txt', 'Mecklenburg.txt', 'Wake.txt', 'Burleigh.txt', 'Belmont.txt', 'Cuyahoga.txt', 'Franklin.txt',
'Hamilton.txt', 'Montgomery.txt', 'Preble.txt', 'Stark.txt', 'Summit.txt', 'Adair.txt', 'Oklahoma.txt', 'Tulsa.txt', 'Multnomah.txt',
'Washington.txt', 'Allegheny.txt', 'Cambria.txt', 'Lackawanna.txt', 'Philadelphia.txt', 'York.txt', 'Providence.txt', 'Richland.txt', 
'Minnehaha.txt', 'Blount.txt', 'Davidson.txt', 'Shelby.txt', 'Bexar.txt', 'Cameron.txt', 'Dallas.txt', 'Harris.txt', 'McLennan.txt', 
'Tarrant.txt', 'Travis.txt', 'Webb.txt', 'Salt Lake.txt', 'Utah.txt', 'Weber.txt', 'Chittenden.txt', 'Rutland.txt', 'Arlington.txt', 
'Fairfax.txt', 'Henrico.txt', 'Roanoke.txt', 'Hampton City.txt', 'Norfolk City.txt', 'Richmond City.txt', 'Clallam.txt', 'King.txt', 
'Kanawha.txt', 'Dodge.txt', 'Milwaukee.txt', 'Converse.txt', 'Laramie.txt', 'Teton.txt', 'Caguas.txt', 'Guaynabo.txt', 'Ponce.txt', 
'San Juan.txt']




CONNECTION_STRINGS=["HostName=CSCI8980MS.azure-devices.net;DeviceId=DEVICE_JEFFERSON;SharedAccessKey=fhJPa6Lri4y9bkl8NC7sNJtuRDDa/axJZ4KL3I2ETSQ=",
"HostName=CSCI8980MS.azure-devices.net;DeviceId=DEVICE_HENNEPIN;SharedAccessKey=eNOfNpNcDjEnKyrMO9pAthirQHhcvPPfg3LwTUl2yKQ=",
"HostName=CSCI8980MS.azure-devices.net;DeviceId=DEVICE_ANOKA;SharedAccessKey=JQlIDmkJ7W3t5fUroVPGrg0cp6TyRSjsUnfsWjhabX0=",
"HostName=CSCI8980MS.azure-devices.net;DeviceId=DEVICE_RAMSEY;SharedAccessKey=kjrjW/6R2rjvrx/PgyhPWzf9RWHmBGz0QY0IE0BcSWg=",
"HostName=CSCI8980MS.azure-devices.net;DeviceId=DEVICE_MINNEHAHA;SharedAccessKey=BDFEuRIy2mojOs2DAf/C+7M0DqrrYDofhZRl0G4EIX0="
]

class HEADER_DICT:   
    @classmethod
    def create(self,id,x,y,persist_time=10):
        header_dict={}
        header_dict['id']=id
        header_dict['x_loc']=x
        header_dict['y_loc']=y
        header_dict['persist_time']=persist_time
        return header_dict
