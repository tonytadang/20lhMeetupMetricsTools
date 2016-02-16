print '###################################################'
print '# EVENTS HOSTED OVER SPECIFIC TIME PERIOD FETCHER #'
print '###################################################'
print ''

import urllib2 #allows use of .urlopen()
import json #allows .load of json file

#################################################################
# PART1- Get epoch timestamps for starting and ending event IDs #
#################################################################

event_id_start = raw_input('Enter starting event ID: ') #ex: 217748822
event_id_end = raw_input('Enter ending event ID: ') #ex: 218749511
print ''

print 'Running script...'
print ''

#meetup api url to get epoch timestamp via the starting event IDs using '/2/events' method (no api key required):
url = 'https://api.meetup.com/2/events?&sign=true&photo-host=public&group_urlname=20letshang&event_id='+event_id_start+'&status=past&page=999&only=id,time'

#loads json from above url
data = json.load(urllib2.urlopen(url))

#obtain epoch timestamp for starting event ID:
for x in data['results']:
	epoch_start = x['time']

#meetup api url to get epoch timestamp via the ending event IDs using '/2/events' method (no api key required):
url = 'https://api.meetup.com/2/events?&sign=true&photo-host=public&group_urlname=20letshang&event_id='+event_id_end+'&status=past&page=999&only=id,time'

#loads json from above url
data = json.load(urllib2.urlopen(url))

#obtain epoch timestamp for ending event ID:
for x in data['results']:
	epoch_end = x['time']

#change epoch timestamps into strings:
epoch_start = str(epoch_start)
epoch_end = str(epoch_end)

###################################################################
# PART2- Get list of event_ids from start to end epoch timestamps #
###################################################################

#meetup api url to get event IDs within epoch timestamps period using '/2/events' method (no api key required):
url = 'https://api.meetup.com/2/events?&sign=true&photo-host=public&group_urlname=20letshang&time=' + epoch_start + ',' + epoch_end + '&status=past&page=200&only=id,time'

#loads json from above url
data = json.load(urllib2.urlopen(url))

#creates event IDs list and populates up to first 200 event IDs:
event_ids = []
for item in data['results']:
	event_ids.append(item['id'])

#keeps changing api url to get next 200 event IDs until no more events:
while data['meta']['next'] != "":
	url = data['meta']['next']
	data = json.load(urllib2.urlopen(url))
	for item in data['results']:
		event_ids.append(item['id'])

########################################################
# PART3- Get list of event hosts (via their member_id) #
########################################################

meetup_api_key = '4b5e1025523d10283f602d7056327875'

#creates list of event_host_ids for all meetups since 20lh group inception:
event_host_ids = []

#populates event_host_ids list:
for event_id in event_ids:
	url = 'https://api.meetup.com/2/rsvps?key='+meetup_api_key+'&sign=true&photo-host=public&fields=host&rsvp=yes&event_id='+event_id+'&page=200&only=host,member'
	data = json.load(urllib2.urlopen(url))
	for item in data['results']:
		if item['host'] == True:
			event_host_ids.append(item['member']['member_id'])

####################################################################
# PART4- Get list of all_members_names and all_members_ids in 20LH #
####################################################################

#meetup api url to fetch all_members_names & all_members_ids using '/2/members' method (api key required):
url = 'https://api.meetup.com/2/members?key='+meetup_api_key+'&sign=true&photo-host=public&group_urlname=20LetsHang&page=200&only=name,id'

#loads json from above url
data = json.load(urllib2.urlopen(url))

#creates all_members_names & all_members_ids list and populates up to first 200 members:
all_members_names = []
all_members_ids = []
for item in data['results']:
	all_members_names.append(item['name'])
	all_members_ids.append(item['id'])

#keeps changeing api url to get next 200 member names and ids until no more members:
while data['meta']['next'] != "":
	url = data['meta']['next']
	data = json.load(urllib2.urlopen(url))
	for item in data['results']:
		all_members_names.append(item['name'])
		all_members_ids.append(item['id'])

#########################################################################
# PART4- Counts how many events each member (by member_id) has attended #
#########################################################################

#counts how many events each member (by member_id) has attended:
events_hosted = []
for member_id in all_members_ids:
	events_hosted.append(event_host_ids.count(member_id))

#######################################################################################
# PART5- Print event_ids, all_member_names, all_member_ids, and events_hosted lists #
#######################################################################################

print 'LIST OF EVENT IDs:'
for event_id in event_ids:
	print event_id

print ''

print 'LIST OF MEMBER NAMES:'
for member_name in all_members_names:
	member_name = member_name.encode("utf-8") #to get weird symbols to show up
	print member_name

print ''

print 'LIST OF MEMBER IDs:'
for member_id in all_members_ids:
	print member_id

print ''

print 'COUNT OF EVENTS HOSTED FOR EACH MEMBER:'
for count in events_hosted:
	print count

print ''

print 'END OF SCRIPT'
input("Press any key to exit...")