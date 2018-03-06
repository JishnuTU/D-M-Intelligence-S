import math
import clips
from home.models import User
from account.models import Volunteer,Hospital,Pronearea,Accomadation
from controlunit.models import Food,Water,Machine,TransportGoods,TransportHuman,Rescuetool,Firstaid,Messagebox

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d


def message_handler(toaddr,selectaid,parameter):
    msg=Messagebox()
    msg.fromaddr=toaddr
    msg.toaddr=toaddr
    msg.topic="Request"
    msg.message=selectaid
    msg.parameter=parameter
    msg.ack=1
    msg.save()


def message_dealer(usernm,lat3,long3,obj):
    dealers = Messagebox.objects.filter(toaddr=usernm,topic="Request",ack=1,nack=0)
    e = clips.Fact(obj)
    print (clips.PrintFacts())
    for dealer in dealers:
        try:
            e.Slots['aid'] = dealer.message
            e.Slots['latitude'] = lat3
            e.Slots['longitude'] =long3
            e.Slots['quantity']= dealer.parameter
            e.Assert()
            dealer.nack = 1
            dealer.save()
        except clips.ClipsError:
            print ("Already Asserted Fact")


def resource_handler(req_aid, lat, longt, quantity, allies):
    if quantity == 0:
        return
    gathered_quantity = 0
    rangedistance = 50
    if req_aid == "Food":
        try:
            food = Food.objects.all()
            while (gathered_quantity <= quantity) and (rangedistance <= 1500):
                for aid in food:
                    print (str(lat) +" " + str(longt) + "acquired " + str(aid.user.latitude) + " " + str(aid.user.longitude) + " " + str(rangedistance) + " " + str(quantity) + " gr" + str(gathered_quantity))
                    if distance((lat, longt), (aid.user.latitude , aid.user.longitude)) <= rangedistance:
                        try:
                            print ("got " + aid.user.username)
                            a = clips.Fact(allies)
                            a.Slots['username'] = aid.user.username
                            a.Slots['foraid'] = req_aid
                            a.Slots['action'] = "Alert"
                            a.Slots['quantity'] = aid.packet
                            a.Assert()
                            gathered_quantity=gathered_quantity+aid.packet
                        except clips.ClipsError:
                            print  ("Already Asserted Fact")
                rangedistance = rangedistance + 50
        except Food.DoesNotExist:
            pass
    if req_aid == "Volunteer":
        try:
            vol = Volunteer.objects.all()
            while (gathered_quantity <= quantity) and (rangedistance <= 1500):
                for aid in vol:
                    #print (str(lat)+" "+str(long)+"acquired " + str(aid.user.latitude) + " " + str(aid.user.longitude)+" "+str(rangedistance)+" "+str(quantity)+" gr"+str(gathered_quantity))
                    if distance((lat, longt), (aid.user.latitude , aid.user.longitude)) <= rangedistance:
                        try:
                            print ("got " + aid.user.username)
                            a = clips.Fact(allies)
                            a.Slots['username'] = aid.user.username
                            a.Slots['foraid'] = req_aid
                            a.Slots['action'] = "Alert"
                            a.Slots['quantity'] = aid.humanaid
                            a.Assert()
                            gathered_quantity=gathered_quantity+aid.humanaid
                        except clips.ClipsError:
                            print  ("Already Asserted Fact")
                rangedistance = rangedistance + 50
        except Volunteer.DoesNotExist:
            pass
    if req_aid == "Hospital":
        try:
            hos = Hospital.objects.all()
            while (gathered_quantity <= quantity) and (rangedistance <= 1500):
                for aid in hos:
                    #print (str(lat)+" "+str(long)+"acquired " + str(aid.user.latitude) + " " + str(aid.user.longitude)+" "+str(rangedistance)+" "+str(quantity)+" gr"+str(gathered_quantity))
                    if distance((lat, longt), (aid.user.latitude , aid.user.longitude)) <= rangedistance:
                        try:
                            print ("got " + aid.user.username)
                            a = clips.Fact(allies)
                            a.Slots['username'] = aid.user.username
                            a.Slots['foraid'] = req_aid
                            a.Slots['action'] = "Alert"
                            a.Slots['quantity'] = aid.canoccupy
                            a.Assert()
                            gathered_quantity=gathered_quantity+aid.canoccupy
                        except clips.ClipsError:
                            print  ("Already Asserted Fact")
                rangedistance = rangedistance + 50
        except Hospital.DoesNotExist:
            pass
    if req_aid == "Accommodation":
        try:
            acc =Accomadation .objects.all()
            while (gathered_quantity <= quantity) and (rangedistance <= 1500):
                for aid in acc:
                    #print (str(lat)+" "+str(long)+"acquired " + str(aid.user.latitude) + " " + str(aid.user.longitude)+" "+str(rangedistance)+" "+str(quantity)+" gr"+str(gathered_quantity))
                    if distance((lat, longt), (aid.user.latitude , aid.user.longitude)) <= rangedistance:
                        try:
                            print ("got " + aid.user.username)
                            a = clips.Fact(allies)
                            a.Slots['username'] = aid.user.username
                            a.Slots['foraid'] = req_aid
                            a.Slots['action'] = "Alert"
                            a.Slots['quantity'] = aid.capacity
                            a.Assert()
                            gathered_quantity=gathered_quantity+aid.capacity
                        except clips.ClipsError:
                            print  ("Already Asserted Fact")
                rangedistance = rangedistance + 50
        except Accomadation.DoesNotExist:
            pass
    if req_aid == "Water":
        try:
            wat = Water.objects.all()
            while (gathered_quantity <= quantity) and (rangedistance <= 1500):
                for aid in wat:
                    #print (str(lat)+" "+str(long)+"acquired " + str(aid.user.latitude) + " " + str(aid.user.longitude)+" "+str(rangedistance)+" "+str(quantity)+" gr"+str(gathered_quantity))
                    if distance((lat, longt), (aid.user.latitude , aid.user.longitude)) <= rangedistance:
                        try:
                            print ("got " + aid.user.username)
                            a = clips.Fact(allies)
                            a.Slots['username'] = aid.user.username
                            a.Slots['foraid'] = req_aid
                            a.Slots['action'] = "Alert"
                            a.Slots['quantity'] = aid.quantity
                            a.Assert()
                            gathered_quantity=gathered_quantity+aid.quantity
                        except clips.ClipsError:
                            print  ("Already Asserted Fact")
                rangedistance = rangedistance + 50
        except Water.DoesNotExist:
            pass
    if req_aid == "RescueTool":
        try:
            restool = Rescuetool.objects.all()
            while (gathered_quantity <= quantity) and (rangedistance <= 1500):
                for aid in restool:
                    #print (str(lat)+" "+str(long)+"acquired " + str(aid.user.latitude) + " " + str(aid.user.longitude)+" "+str(rangedistance)+" "+str(quantity)+" gr"+str(gathered_quantity))
                    if distance((lat, longt), (aid.user.latitude , aid.user.longitude)) <= rangedistance:
                        try:
                            print ("got " + aid.user.username)
                            a = clips.Fact(allies)
                            a.Slots['username'] = aid.user.username
                            a.Slots['foraid'] = req_aid
                            a.Slots['action'] = "Alert"
                            a.Slots['quantity'] = aid.box
                            a.Assert()
                            gathered_quantity=gathered_quantity+aid.box
                        except clips.ClipsError:
                            print  ("Already Asserted Fact")
                rangedistance = rangedistance + 50
        except Rescuetool.DoesNotExist:
            pass
    if req_aid == "FirstAid":
        try:
            firstaid = Firstaid.objects.all()
            while (gathered_quantity <= quantity) and (rangedistance <= 1500):
                for aid in firstaid:
                    #print (str(lat)+" "+str(long)+"acquired " + str(aid.user.latitude) + " " + str(aid.user.longitude)+" "+str(rangedistance)+" "+str(quantity)+" gr"+str(gathered_quantity))
                    if distance((lat, longt), (aid.user.latitude , aid.user.longitude)) <= rangedistance:
                        try:
                            print ("got " + aid.user.username)
                            a = clips.Fact(allies)
                            a.Slots['username'] = aid.user.username
                            a.Slots['foraid'] = req_aid
                            a.Slots['action'] = "Alert"
                            a.Slots['quantity'] = aid.kit
                            a.Assert()
                            gathered_quantity=gathered_quantity+aid.kit
                        except clips.ClipsError:
                            print  ("Already Asserted Fact")
                rangedistance = rangedistance + 50
        except Firstaid.DoesNotExist:
            pass
    if req_aid == "Transport-Human":
        try:
            thuman = TransportHuman.objects.all()
            while (gathered_quantity <= quantity) and (rangedistance <= 1500):
                for aid in thuman:
                    #print (str(lat)+" "+str(long)+"acquired " + str(aid.user.latitude) + " " + str(aid.user.longitude)+" "+str(rangedistance)+" "+str(quantity)+" gr"+str(gathered_quantity))
                    if distance((lat, longt), (aid.user.latitude , aid.user.longitude)) <= rangedistance:
                        try:
                            print ("got " + aid.user.username)
                            a = clips.Fact(allies)
                            a.Slots['username'] = aid.user.username
                            a.Slots['foraid'] = req_aid
                            a.Slots['action'] = "Alert"
                            a.Slots['quantity'] = aid.capacity
                            a.Assert()
                            gathered_quantity=gathered_quantity+aid.capacity
                        except clips.ClipsError:
                            print  ("Already Asserted Fact")
                rangedistance = rangedistance + 50
        except TransportHuman.DoesNotExist:
            pass
    if req_aid == "Transport-Goods":
        try:
            tgoods = TransportGoods.objects.all()
            while (gathered_quantity <= quantity) and (rangedistance <= 1500):
                for aid in tgoods:
                    #print (str(lat)+" "+str(long)+"acquired " + str(aid.user.latitude) + " " + str(aid.user.longitude)+" "+str(rangedistance)+" "+str(quantity)+" gr"+str(gathered_quantity))
                    if distance((lat, longt), (aid.user.latitude , aid.user.longitude)) <= rangedistance:
                        try:
                            print ("got " + aid.user.username)
                            a = clips.Fact(allies)
                            a.Slots['username'] = aid.user.username
                            a.Slots['foraid'] = req_aid
                            a.Slots['action'] = "Alert"
                            a.Slots['quantity'] = aid.capacity
                            a.Assert()
                            gathered_quantity=gathered_quantity+aid.capacity
                        except clips.ClipsError:
                            print  ("Already Asserted Fact")
                rangedistance = rangedistance + 50
        except TransportGoods.DoesNotExist:
            pass
    if req_aid == "JCB":
        try:
            mach1 = Machine.objects.all()
            while (gathered_quantity <= quantity) and (rangedistance <= 1500):
                for aid in mach1:
                    if aid.jcb!=0:
                    #print (str(lat)+" "+str(long)+"acquired " + str(aid.user.latitude) + " " + str(aid.user.longitude)+" "+str(rangedistance)+" "+str(quantity)+" gr"+str(gathered_quantity))
                        if distance((lat, longt), (aid.user.latitude , aid.user.longitude)) <= rangedistance:
                            try:
                                print ("got " + aid.user.username)
                                a = clips.Fact(allies)
                                a.Slots['username'] = aid.user.username
                                a.Slots['foraid'] = req_aid
                                a.Slots['action'] = "Alert"
                                a.Slots['quantity'] = aid.jcb
                                a.Assert()
                                gathered_quantity=gathered_quantity+aid.jcb
                            except clips.ClipsError:
                                print  ("Already Asserted Fact")
                rangedistance = rangedistance + 50
        except Machine.DoesNotExist:
            pass
    if req_aid == "FireEngine":
        try:
            mach2 = Food.objects.all()
            while (gathered_quantity <= quantity) and (rangedistance <= 1500):
                for aid in mach2:
                    if aid.fireengine!=0:
                    #print (str(lat)+" "+str(long)+"acquired " + str(aid.user.latitude) + " " + str(aid.user.longitude)+" "+str(rangedistance)+" "+str(quantity)+" gr"+str(gathered_quantity))
                        if distance((lat, longt), (aid.user.latitude , aid.user.longitude)) <= rangedistance:
                            try:
                                print ("got " + aid.user.username)
                                a = clips.Fact(allies)
                                a.Slots['username'] = aid.user.username
                                a.Slots['foraid'] = req_aid
                                a.Slots['action'] = "Alert"
                                a.Slots['quantity'] = aid.fireengine
                                a.Assert()
                                gathered_quantity=gathered_quantity+aid.fireengine
                            except clips.ClipsError:
                                print  ("Already Asserted Fact")
                rangedistance = rangedistance + 50
        except Machine.DoesNotExist:
            pass
    if req_aid == "Ambulance":
        try:
            mach3 = Machine.objects.all()
            while (gathered_quantity <= quantity) and (rangedistance <= 1500):
                for aid in mach3:
                    if aid.ambulance!=0:
                    #print (str(lat)+" "+str(long)+"acquired " + str(aid.user.latitude) + " " + str(aid.user.longitude)+" "+str(rangedistance)+" "+str(quantity)+" gr"+str(gathered_quantity))
                        if distance((lat, longt), (aid.user.latitude , aid.user.longitude)) <= rangedistance:
                            try:
                                print ("got " + aid.user.username)
                                a = clips.Fact(allies)
                                a.Slots['username'] = aid.user.username
                                a.Slots['foraid'] = req_aid
                                a.Slots['action'] = "Alert"
                                a.Slots['quantity'] = aid.ambulance
                                a.Assert()
                                gathered_quantity=gathered_quantity+aid.ambulance
                            except clips.ClipsError:
                                print  ("Already Asserted Fact")
                rangedistance = rangedistance + 50
        except Machine.DoesNotExist:
            pass
    if gathered_quantity < quantity :
        try:
            clips.Assert("(Message \"Searched Aid : "+req_aid+" # Quantity is Unavailable in Perimeter , Gathered Quantity :"+str(gathered_quantity)+"\")")
        except clips.ClipsError:
            print ("Error")
    return


def prone_area_checking(lat, longt, obj1, dist=500):
    print ('Prone area checking invoked')
    try:
        prone_area=Pronearea.objects.all()
        for area in prone_area:
            if distance((lat, longt), (area.user.latitude, area.user.longitude)) <= dist :
                try:
                    a = clips.Fact(obj1)
                    a.Slots['username'] = area.user.username
                    a.Slots['foraid'] = "ProneArea"
                    a.Slots['action'] = "AlertArea"
                    a.Slots['quantity']= area.population
                    a.Assert()
                except clips.ClipsError:
                    print ('Clips Error')
    except Pronearea.DoesNotExist:
        pass