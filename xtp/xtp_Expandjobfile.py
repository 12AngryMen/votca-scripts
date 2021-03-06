#!/usr/bin/env python
from __tools__ import *
import argparse as ap


parser=ap.ArgumentParser(description="Parsing two jobfiles and merging one into the other")
parser.add_argument("-j1","--jobfile1",required=True, help="jobfile to expand")
parser.add_argument("-j2","--jobfile2",required=True, help="jobfile to integrate")
args=parser.parse_args()

# In[2]:


def IntegrateJobfile(doneroot,openroot):
	used=[]
	for entry2 in doneroot.iter("job"):
		used.append(False)
	length=0
	for entry1 in openroot.iter('job'):
		length+=1
	
	print "{} has {} jobs".format(args.jobfile2,len(used))
	print "{} has {} jobs".format(args.jobfile1,length)
	for progress,entry1 in enumerate(openroot.iter('job')):
		update_progress(progress/float(length))
		inputs1=entry1.find("input")
		status1=entry1.find("status")
		if status1.text=="COMPLETE":
			continue
		for i,j in enumerate(inputs1.iter("segment")):
			if i==0:
				seg1_1=(int(j.text))
			elif i==1:
				seg2_1=(int(j.text))
			else:
				print "More than two segments in input"
		
		for index,entry2 in enumerate(doneroot.iter("job")):
			if used[index]:
				continue
			inputs2=entry2.find("input")
			status2=entry2.find("status")
			if status2.text!="COMPLETE":
				used[index]=True
				continue
			for i,j in enumerate(inputs2.iter("segment")):
				if i==0:
					seg1_2=(int(j.text))
				elif i==1:
					seg2_2=(int(j.text))
				else:
					print "More than two segments in input"
			if seg1_2==seg1_1 and seg2_1==seg2_2:
				used[index]=True
				output=entry2.find("output")
				host=entry2.find("host")
				
				time=entry2.find("time")
				status1.text="COMPLETE"
				entry1.append(host)
				entry1.append(time)
				entry1.append(output)
				break


# In[3]:

print "Reading in {}".format(args.jobfile2)
doneroot=XmlParser(args.jobfile2)
print "Reading in {}".format(args.jobfile1)
openroot=XmlParser(args.jobfile1)


# In[4]:

print "Checking which jobs can be moved from {} to {}".format(args.jobfile2,args.jobfile1)
IntegrateJobfile(doneroot,openroot)


# In[5]:

print "Writing to {}".format(args.jobfile1)
XmlWriter(openroot,args.jobfile1)


# In[ ]:




