# Criado por Vitor Henrique
# Última modificação: 29/11/2018

class Disco:
	def __init__(self, name):
		with open(name) as f:
			line = [l for l in f]
		self.pinicial = line[0] 
		self.tfilaespera = line[1]
		self.filaespera = line[2]

	@property
	def pinicial(self):
		return self.__pinicial
		
	@pinicial.setter
	def pinicial(self, pinicial):
		self.__pinicial = int(pinicial)

	@property
	def tfilaespera(self):
		return self.__tfilaespera

	@tfilaespera.setter
	def tfilaespera(self, tfilaespera):
		self.__tfilaespera = int(tfilaespera)

	@property
	def filaespera(self):
		return self.__filaespera

	@filaespera.setter
	def filaespera(self, filaespera):
		self.__filaespera = list(map(int,filaespera.split()))

	def __str__(self):
		return "{}\n{}\n{}\n".format(self.pinicial,self.tfilaespera," ".join(self.filaespera))
		
class Escalonamento:
	def __init__(self, disco, extremities=(0,199)):
		self.minextremity, self.maxextremity = extremities
		#TO-DO: Fazer com que um disco seja salvo aqui também
		self.fcfs, self.sstf, self.scansobe, self.scandesce = disco, disco, disco, disco

	@property
	def scandesce(self):
		return self.__scandesce

	@scandesce.setter
	def scandesce(self, disco):
		def between(a, b, x):
			return a <= x and x <=b
		ordem = [disco.pinicial]
		tmplist = disco.filaespera.copy()
		under = sorted(list(filter(lambda k: between(self.minextremity,disco.pinicial,k), tmplist)),reverse=True)
		ordem+=under
		tmplist = [ i for i in tmplist if i not in under]
		upper = sorted(list(filter(lambda k: between(self.minextremity,self.maxextremity,k), tmplist)))
		ordem+=upper 
		cilindros = sum([abs(ordem[i] - ordem[i+1]) for i in range(len(ordem)-1)])
		self.__scandesce = "\n\tOrdem: {}\n\tCilindro: {}".format(" ".join(map(str, ordem)),cilindros)

	@property
	def scansobe(self):
		return self.__scansobe
	
	@scansobe.setter
	def scansobe(self, disco):
		def between(a, b, x):
			return a <= x and x <=b
		ordem = [disco.pinicial]
		tmplist = disco.filaespera.copy()
		upper = sorted(list(filter(lambda k: between(disco.pinicial,self.maxextremity,k), tmplist))) 
		ordem+=upper
		tmplist = [ i for i in tmplist if i not in upper]
		under = sorted(list(filter(lambda k: between(self.minextremity,self.maxextremity,k), tmplist)), reverse=True)
		ordem+=under
		cilindros = sum([abs(ordem[i] - ordem[i+1]) for i in range(len(ordem)-1)])
		
		self.__scansobe = "\n\tOrdem: {}\n\tCilindro: {}".format(" ".join(map(str, ordem)),cilindros)

	@property
	def sstf(self):
		return self.__sstf
	
	@sstf.setter
	def sstf(self, disco):
		def minDistance(atual,auxlist):
			#Considero que ele mantem a mesma ordem de indices em relação ao array original
			distances = list(map(lambda v: abs(atual-v),auxlist))
			mindist = min(distances)
			return distances.index(mindist), mindist

		ordem = [disco.pinicial]
		head = disco.pinicial
		cilindros = 0
		aux = disco.filaespera.copy()
		while len(aux)!=0:
			idx, smallestDist = minDistance(head,aux)
			cilindros += smallestDist
			head = aux[idx]
			ordem.append(head)
			aux.pop(idx)
			
		self.__sstf = "\n\tOrdem: {}\n\tCilindro: {}".format(" ".join(map(str, ordem)),cilindros)
	
	@property
	def fcfs(self):
		return self.__fcfs

	@fcfs.setter
	def fcfs(self,disco):
		ordem = [disco.pinicial] + disco.filaespera
		cilindros = sum([abs(ordem[i] - ordem[i+1]) for i in range(len(ordem)-1)])
		self.__fcfs = "\n\tOrdem: {}\n\tCilindro: {}".format(" ".join(map(str, ordem)),cilindros)
	
	def __str__(self):
		return "FCFS{}\nSSTF{}\nSCAN SOBE{}\nSCAN DESCE{}".format(self.fcfs,self.sstf,self.scansobe,self.scandesce)


def main():
	d = Disco(input("Caminho do arquivo: "))
	esc = Escalonamento(d)
	print(esc)


main()