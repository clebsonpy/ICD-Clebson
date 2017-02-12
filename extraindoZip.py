import zipfile, os
import arquivoTxt as txt

def listaArq(caminho):
    listaDir = os.listdir(caminho)
    listaZip = []
    listaTxt = []
    for arquivo in listaDir:
        if os.path.isfile(os.path.join(caminho, arquivo)) and arquivo[-3:] == 'ZIP':
            listaZip.append(arquivo)
        elif os.path.isfile(os.path.join(caminho, arquivo)) and arquivo[-3:] == 'TXT':
            listaTxt.append(arquivo[:-4])
    return listaZip, listaTxt

def extraindoZip(caminho, listaZip):
	for zip in listaZip:
		with zipfile.ZipFile(os.path.join(caminho,zip)) as arquivo:
			arquivo.extractall(caminho)
		txt.renomearTxt(caminho, txt.listaTxt(caminho))
		print('Arquivo Extraido!')

if __name__ == "__main__":
    caminho = os.getcwd()
    extraindoZip(caminho, listaArq(caminho)[0])
		
