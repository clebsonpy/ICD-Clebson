import zipfile, os
import arquivoTxt as txt

def listaZip(caminho):
	listaDir = os.listdir(caminho)
	listaArquivo = []
	for arquivo in listaDir:
		if os.path.isfile(os.path.join(caminho,arquivo)) and arquivo[-3:] == 'ZIP':
			listaArquivo.append(arquivo)
	
	return listaArquivo

def extraindoZip(caminho, listaZip):
	for zip in listaZip:
		with zipfile.ZipFile(os.path.join(caminho,zip)) as arquivo:
			arquivo.extractall(caminho)
		txt.renomearTxt(caminho, txt.listaTxt(caminho))
		print('Arquivo Extraido!')

caminho = os.getcwd()
extraindoZip(caminho, listaZip(caminho))
		
