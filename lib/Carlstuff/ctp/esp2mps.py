from __future__ import division
import numpy as np




class PSite(object):
	def __init__(self, name, charge):
		self.name = name
		self.charge = charge
		

class Collection(object):
	def __init__(self):
		self.psites = []

	def esp2self(self, infile):
		intt = open(infile, 'r')
	
		psites = []
		for ln in intt.readlines():
		
			ln = ln.split()
			if ln == []:
				continue
		
			name = ln[1]
			chrg = float(ln[2])		
			psites.append( PSite(name,chrg) )	
	
		self.psites = psites
		
	def self2mps(self, outfile):
		
		outt = open(outfile, 'w')
		
		outt.write('! GENERATED BY: ESP2MPS.PY \n')
		outt.write('! COMPOUND ... ... ... ... \n')
		outt.write('Units bohr \n')
		
		for site in self.psites:
			outt.write('%4s 0.000 0.000 0.000 Rank 0 \n' % (site.name) )
			outt.write('     %4.7f \n' % (site.charge) )
			

sites = Collection()
sites.esp2self('crg.dat')
sites.self2mps('NORMA_h.mps')

sites = Collection()
sites.esp2self('neutr.dat')
sites.self2mps('NORMA.mps')
		

		
	



 
