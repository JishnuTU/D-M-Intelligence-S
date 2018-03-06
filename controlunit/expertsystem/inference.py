import clips
from computation import prone_area_checking,message_dealer,resource_handler,message_handler
from controlunit.models import Messagebox

from home.models import User
from account.models import Volunteer,Hospital,Pronearea,Accomadation

facts = []
fields = []
eng_var = []
list_map=[]

def system_run(input_ set):
    if 'hazard' in input_set:
        clips.Clear()
        clips.Reset()

        eng_var[:]=[]

        eng_var.append(input_set['lat'])

        eng_var.append(input_set['long'])

        eng_var.append(clips.BuildTemplate("entity", """
        (slot aid (type STRING))
        (slot latitude (type NUMBER))
        (slot longitude (type NUMBER))
        (slot quantity (type NUMBER))
        """, "template for a entity"))

        eng_var.append(clips.BuildTemplate("allies", """
        (slot username (type STRING))
        (slot foraid (type STRING))
        (slot action (type STRING))
        (slot quantity (type NUMBER))
        """, "template for a allies"))

        eng_var.append(input_set['control'])

        eng_var.append(clips.BuildTemplate("disaster", """
        (slot hazard (type STRING))
        (slot latitude (type NUMBER))
        (slot longitude (type NUMBER))
        (slot span (type NUMBER))
        """, "template for a disaster"))

        d=clips.Fact(eng_var[5])
        d.Slots['hazard'] = input_set['hazard']
        d.Slots['latitude'] = input_set['lat']
        d.Slots['longitude'] = input_set['long']
        d.Slots['span'] = input_set['span']
        d.Assert()

        facts[:] = []
        fields[:] = []
        list_map[:] = []

        clips.RegisterPythonFunction(invoke_pronearea)
        clips.RegisterPythonFunction(display_disaster)
        clips.RegisterPythonFunction(invoke_entity)
        clips.RegisterPythonFunction(invoke_useralert)
        clips.RegisterPythonFunction(invoke_user_allocate )
        clips.RegisterPythonFunction(invoke_user_deallocate)
        clips.RegisterPythonFunction(invoke_message)
        clips.RegisterPythonFunction(invoke_alert_area)

        clips.BatchStar("/home/jishnu/PycharmProjects/dmis/controlunit/expertsystem/inference.clp")
        clips.Run()

    if 'refresh' in input_set:
        if len(eng_var)==0:
            return {'fact': facts, 'field': fields,'map_data':list_map}
        message_dealer(input_set['control'],eng_var[0],eng_var[1],eng_var[2])
        user_status_checking()
        clips.Run()

    if 'send' in input_set:
        if len(eng_var)==0:
            return {'fact': facts, 'field': fields,'map_data':list_map}
        message_handler(input_set['control'],input_set['selectaid'],input_set['parameter'])

    if 'deallocate' in input_set:
        try:
            clips.Assert("(DeallocateAll)")
        except clips.ClipsError:
            print("Error in Deallocation")
        clips.Run()
        facts[:] = []
        fields[:] = []
        list_map[:] = []

    clips.SendCommand("run")
    print (clips.PrintFacts())
    list_temp=list(facts)
    list_temp.reverse()
    return {'fact':list_temp,'field':list(set(fields)),'map_data':list_map}


def display_disaster(a,b,c,d):
    string='Hazard : '+a+' @ Latitude : '+str(b)+' & Longitude : '+str(c)+' # Span : '+str(d)
    #print (string)
    facts.append(string)


def invoke_entity(a,b,c,d):
    string='Required Aid : '+a+' @ Latitude : '+str(b)+' & Longitude : '+str(c)+' # Quantity : '+str(d)
    resource_handler(a,float(b), float(c), int(d), eng_var[3])
    print(string)
    facts.append(string)
    fields.append(a)


def invoke_pronearea(la,lo):
    string = 'Prone area Checking Invoked : ' + ' @ Latitude : '+str(la)+' & Longitude : '+str(lo)
    facts.append(string)
    prone_area_checking(la,lo,eng_var[3])


def invoke_useralert(username,aid,qt):
    string = 'Alerted User : ' + str(username) + ' For Aid : ' + str(aid) + ' Posses Asset About : ' + str(qt)
    facts.append(string)
    msg = Messagebox()
    msg.fromaddr = eng_var[4]
    msg.toaddr = str(username)
    msg.topic = "Request for Service"
    msg.message = str(aid)
    msg.parameter = int(qt)
    msg.save()
    usnm=User.objects.get(username=str(username))
    tmap = {}
    tmap['title'] = str(username)
    tmap['lat'] = usnm.latitude
    tmap['lng'] = usnm.longitude
    tmap['aid'] = str(aid)
    tmap['status'] = "Alerted"
    tmap['description'] = "Currently Available Service :" + str(qt)
    list_map.append(tmap)


def invoke_user_allocate(usernm, aid, q):
    string = 'User Responded and Allocated : ' + str(usernm) + ' For Aid : ' + str(aid) + 'Posses Asset About : ' + str(q)
    facts.append(string)
    member = User.objects.get(username=str(usernm))
    if member.category == "volunteer":
        mem = Volunteer.objects.get(user=member)
    if member.category == 'hospital':
        mem = Hospital.objects.get(user=member)
    if member.category == 'accommodation':
        mem = Accomadation.objects.get(user=member)
    if member.category == 'pronearea':
        mem = Pronearea.objects.get(user=member)
    if mem.status == 0:
        mem.status = 1
        mem.loyalto = eng_var[4]
        mem.save()
    try:
        a = clips.Fact(eng_var[3])
        a.Slots['username'] = usernm
        a.Slots['foraid'] = aid
        a.Slots['action'] = "Allocated"
        a.Slots['quantity'] = q
        a.Assert()
    except clips.ClipsError:
        print  ("Already Asserted Fact")

    for tmap in list_map:
        if tmap['title'] == str(usernm) and tmap['aid']==str(aid):
            tmap['status']="Allocated"

    # usnm = User.objects.get(username=str(usernm))
    # tmap = {}
    # tmap['title'] = str(usernm)
    # tmap['lat'] = usnm.latitude
    # tmap['lng'] = usnm.longitude
    # tmap['aid'] = str(aid)
    # tmap['status'] = "Allocated"
    # tmap['description'] = "Currently Available Service :" + str(q)
    # list_map.append(tmap)


def invoke_user_deallocate(usernm):
    member = User.objects.get(username=usernm)
    if member.category == "volunteer":
        mem = Volunteer.objects.get(user=member)
    if member.category == 'hospital':
        mem = Hospital.objects.get(user=member)
    if member.category == 'accommodation':
        mem = Accomadation.objects.get(user=member)
    if member.category == 'pronearea':
        mem = Pronearea.objects.get(user=member)
    if mem.status == 1:
        mem.status = 0
        mem.loyalto = "nil"
        mem.save()


def invoke_message(mess):
    facts.append(str(mess))


def invoke_alert_area(pname,p):
    string = 'Prone Area Found : ' + str(pname) + ' Alerted the Area '
    facts.append(string)
    msg = Messagebox()
    msg.fromaddr = eng_var[4]
    msg.toaddr = str(pname)
    msg.topic = "Alert"
    msg.message = "NearBy Hazard Need To Displace To safer Location"
    msg.parameter = 0
    msg.save()
    try:
        member = User.objects.get(username=str(pname))
        d = clips.Fact(eng_var[5])
        d.Slots['hazard'] ="displace"
        d.Slots['latitude'] = member.latitude
        d.Slots['longitude'] = member.longitude
        d.Slots['span'] = int(p)
        d.Assert()
    except clips.ClipsError:
        print("Clips Error")


def user_status_checking():
    dealers = Messagebox.objects.filter(fromaddr=eng_var[4], topic="Request for Service", ack=1, nack=0)
    a = clips.Fact(eng_var[3])
    print (clips.PrintFacts())
    for dealer in dealers:
        try:
            a.Slots['username'] = dealer.toaddr
            a.Slots['foraid'] = dealer.message
            a.Slots['action'] = "Allocate"
            a.Slots['quantity'] = dealer.parameter
            a.Assert()
            dealer.nack = 1
            dealer.save()
        except clips.ClipsError:
            print ("Already Asserted Fact")