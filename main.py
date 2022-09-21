from cmath import sqrt
from pickle import NONE
from sys import float_repr_style
#import syspip
from PIL import Image
from PIL import ImageFile
import os
ImageFile.LOAD_TRUNCATED_IMAGES = True
from pip import main
import tqdm
import requests
import imageio
import json
import shutil


#required commands
#pip install - -upgrade pip
#pip insatll pillow
#pip install tqdm
#pip install requests
#pip install imageio

#attention you nedd tu run file not run code

#put your keys here
Keys = ["631afcfc1d4931.45837230", "631a4bfca3ad85.65557574"]
#variable compteur_key globale
global compteur_key 
compteur_key = 0
global api_enable
#si vous avez des clés fonctionelles vous pouvez les rajouter dans la liste Keys et activer api_enable
api_enable = False

#fonction qui parcours path et qui rajoute un \ dans la string path si il y a un \t,\n,\r,\a,\b,\f,\v
def parcour_path(path):
    #si dans path il y a un \t,\n,\r,\a,\b,\f,\v on rajoute un \ devant
    if path.find('\t') != -1 or path.find('\n') != -1 or path.find('\r') != -1 or path.find('\a') != -1 or path.find('\b') != -1 or path.find('\f') != -1 or path.find('\v') != -1:
        path = path.replace('\t', '\\t')
        path = path.replace('\n', '\\n')
        path = path.replace('\r', '\\r')
        path = path.replace('\a', '\\a')
        path = path.replace('\b', '\\b')
        path = path.replace('\f', '\\f')
        path = path.replace('\v', '\\v')

    return path




#fonction qui génère des dossier dans path (dest_path,png_path,crop_path,dl_path)
def generate_path(path):
    if not os.path.exists(path+"\\"+"png_path"):
        png_path = path + "\\" + "png_path"
        png_path = parcour_path(png_path)
        os.makedirs(png_path)
    else :
        png_path = path + "\\" + "png_path"
        png_path = parcour_path(png_path)
    if not os.path.exists(path+"\\"+"dest_path"):
        dest_path = path + "\\" + "dest_path"
        dest_path = parcour_path(dest_path)
        os.makedirs(dest_path)
    else:
        dest_path = path + "\\" + "dest_path"
        dest_path = parcour_path(dest_path)
    if not os.path.exists(path+"\\"+"crop_path"):
        crop_path = path + "\\" + "crop_path"
        crop_path = parcour_path(crop_path)
        os.makedirs(crop_path)
    else:
        crop_path = path + "\\" + "crop_path"
        crop_path = parcour_path(crop_path)
    if not os.path.exists(path+"\\"+"dl_path"):
        dl_path = path + "\\" + "dl_path"
        dl_path = parcour_path(dl_path)
        os.makedirs(dl_path)
    else:
        dl_path = path + "\\" + "dl_path"
        dl_path = parcour_path(dl_path)
    if not os.path.exists(path+"\\"+"result_path"):
        result_path = path + "\\" + "result_path"
        result_path = parcour_path(result_path)
        os.makedirs(result_path)
    else:
        result_path = path + "\\" + "result_path"
        result_path = parcour_path(result_path)
    if not os.path.exists(path+"\\"+"reduced_path"):
        reduced_path = path + "\\" + "reduced_path"
        reduced_path = parcour_path(reduced_path)
        os.makedirs(reduced_path)
    else:
        reduced_path = path + "\\" + "reduced_path"
        reduced_path = parcour_path(reduced_path)
    
    return  (dest_path,png_path,crop_path,dl_path,result_path,reduced_path)






#fonction qui vide les dossier de leur contenu
def empty_dir(path):
    for root, dirs, files in os.walk(path):
        for file in tqdm.tqdm (files, desc="emptying folders", ascii=False, ncols=75):
            os.remove(path + '\\' + file)



#fonction qui convertit l'image en png
def convert_png(path,dest_path):
    for root, dirs, files in os.walk(path):
        for file in tqdm.tqdm (files, desc="converting images", ascii=False, ncols=75):
            #si l'image n'esxiste pas déjà dans le dossier dest_path
            if not os.path.exists(dest_path + '\\' + file[:-4] + '.png'):
                if file.endswith(".jpg") or file.endswith(".jpeg"):
                    img = Image.open(path + '\\' + file)
                    img.save(dest_path + '\\' + file[:-4] + '.png')
                #sinon si l'image est en png on la copie dans le dossier dest_path
                elif file.endswith(".png"):
                    img = Image.open(path + '\\' + file)
                    img.save(dest_path + '\\' + file)


#fonction qui fait une rotation de 270° en gardant les proportions de l'image
def rotate_90(path, name,dest_path):
    #on convertit l'image en png
    img = Image.open(path + '\\' + name)
    #on ouvre l'image
    img = Image.open(path + '\\' + name)
    #on calcule la nouvelle taille de l'image
    new_size = (int(img.size[1]), int(img.size[0]))
    #on crée une nouvelle image avec la nouvelle taille 
    new_img = Image.new('RGBA', new_size, (255, 255, 255, 0))
    #on calcule la position de l'image
    pos = (int((new_size[0] - img.size[0]) / 2), int((new_size[1] - img.size[1]) / 2))
    #on colle l'image sur la nouvelle image
    new_img.paste(img, pos)
    #on fait la rotation de 270°
    new_img = new_img.rotate(270)
    #on sauvegarde l'image
    new_img.save(dest_path + '\\' + name)

#fonction qui parcour toutes les images du dossier path
def parcour(path,dest_path):
    for root, dirs, files in os.walk(path):
        for file in tqdm.tqdm (files, desc="rotating images", ascii=False, ncols=75):
            #si l'image n'esxiste pas déjà dans le dossier dest_path
            if not os.path.exists(dest_path + '\\' + file):
                if file.endswith(".png"):
                    rotate_90(path, file,dest_path)




#fonction qui coupe l'image
def crop(image,filename,path):

    top = 0
    bottom = image.size[1]
    find_color = False
    find_transparent = False


    #parcour les pixels de l'image de haut en bas
    for y in range(image.size[1]) :#tqdm.tqdm(, desc="cropping", ascii=False, ncols=75)
       
        #quand on trouve un pixel de couleur 
        if image.getpixel((0, y)) != (0, 0, 0 ,0) and find_color == False :
            top = y
            find_color = True
            #print("top : " + str(top))
            

        #quand on retrouve un pixel transparent
        if image.getpixel((0, y)) == (0, 0, 0, 0) and find_color == True and find_transparent == False:
            bottom = y
            find_transparent = True
            #print("bottom : " + str(bottom))

            
    #on coupe de 0 à top
    image = image.crop((0, top, image.size[0], bottom))

    #on resize l'image pour qu'elle fasse 500*500
    image = image.resize((500, 500))
    


    #on sauvegarde l'image
    image.save(path + '\\' + filename,optimize=True,quality=20)

#fonction qui parcours les fichiers dans path
def parcour_file(path,crop_path):
    #on parcours les fichiers dans path
    for file in  tqdm.tqdm(os.listdir(path), desc="cropping", ascii=False, ncols=75):
        #si l'image n'esxiste pas déjà dans le dossier crop_path
        if not os.path.exists(crop_path + '\\' + file):
            #si le fichier est un .png ou .jpg
            if file.endswith(".png") :
                #on ouvre l'image
                image = Image.open(path + '\\' + file)
                #on coupe l'image
                crop(image,file,crop_path)

#fonction create_gif qui crée un gif à partir des images dans path
def create_gif(path,dest_path):
    #on crée une liste vide
    images = []
    #on parcours les fichiers dans path
    for file in tqdm.tqdm(os.listdir(path), desc="creating gif", ascii=False, ncols=75):
        #si l'image n'esxiste pas déjà dans le dossier dest_path
        if not os.path.exists(dest_path + '\\' + file[:-4] + '.gif'):
            #si le fichier est un .png ou .jpg
            if file.endswith(".png") or file.endswith(".jpg"):
                #on ouvre l'image
                images.append(imageio.imread(path + '\\' + file))
    #si il y a plus de 2 images et que l'image n'esxiste pas déjà dans le dossier dest_path
    if len(images) > 2 and not os.path.exists(dest_path + '\\' + file[:-4] + '.gif'):
        #on crée le gif
        imageio.mimsave(dest_path + '\\' + 'gif.gif', images, duration=0.080)
        #si la taille du gif est >= à 1Mo on returne False
        if os.path.getsize(dest_path + '\\' + 'gif.gif') >= 1000000:
            print("gif trop lourd",os.path.getsize(dest_path + '\\' + 'gif.gif'))
            return False

#fonction api
    """
    It downloads images from a folder, sends them to an API, and saves the results in another folder
    
    :param path: the path to the folder containing the images you want to remove the background from
    :param dl_path: The path to the folder where you want to save the images
    :return: the value of the variable api_enable.
    """
def api(path,dl_path):
    global compteur_key
    global api_enable
    if api_enable == False:
        print("api disabled")
        return 0
    else :
        #on parcours les fichiers dans path
        compteur_actual = 0
        compteur_dl = 0
        for file in tqdm.tqdm(os.listdir(path), desc="api", ascii=False, ncols=75):
            #si des fichiers existent déjà dans dl_path
            for dir in os.listdir(dl_path):
                if os.path.isfile(os.path.join(dl_path, dir)):
                    compteur_dl += 1
            if compteur_actual > compteur_dl:
                print(compteur_dl," fichiers déjà téléchargés détectés -> passage au téléchargement à partir du fichier ",compteur_actual)
                #si le fichier est un .png
                if file.endswith(".png"):
                    url = "https://api.removal.ai/3.0/remove"

                    payload={'image_url': 'url_to_image'}
                    files=[
                    ('image_file',(file,open(path+'\\'+file,'rb'),'image/png'))
                    ]
                    headers = {
                    'Rm-Token': Keys[compteur_key]
                    }

                    print("->sending requests")

                    response = requests.request("POST", url, headers=headers, data=payload, files=files)

                    print(response.text)
                    #créer un dictionnaire à partir de la chaine de caractère response.text
                    data = json.loads(response.text)
                    #fonction qui renvoye l'attribut qui correspond à la clé key
                    def get_value(response,key):
                        #si la clé key est dans le dictionnaire data
                        if key in data:
                            #on renvoie la valeur de la clé key
                            return data[key]
                        #sinon
                        else:
                            #on renvoie None
                            return None

                    #télécharge l'image
                    def download_image(url,filename,dl_path):
                        #on télécharge l'image
                        r = requests.get(url, allow_redirects=True)
                        #on sauvegarde l'image
                        open(dl_path + '\\' + filename, 'wb').write(r.content)

                    #si get value renvoye USER_CREDIT_ERROR
                    if get_value(data,"error") == "USER_CREDIT_ERROR":
                        #on ajoute 1 au compteur_key
                        compteur_key += 1
                        #si la liste Keys à une valeure accessible à l'indice compteur_key
                        if len(Keys) > compteur_key:
                            print("->changing key")
                            #on relance la fonction api
                            return api(path,dl_path)
                        else :
                            print("no more keys or key outdated you need to add more keys or upgrade your account here : https://removal.ai/pricing")
                            continu = input("did you want to continue whithout api ? (y or n)")
                            if continu == "y":
                                print("->continuing without api")
                                api_enable = False
                                compteur_key = 0
                                return api_enable
                            else:
                                exit("Sorry dude I can't do anything without api")
                    else :
                        print(get_value(data,"preview_demo"))
                        #on télécharge l'image
                        download_image(get_value(data,"preview_demo"),file,dl_path)
            compteur_actual += 1
            compteur_dl = 0

#fonction réduction de taille des images
def reduce_img(path,dest_path):
    for file in tqdm.tqdm(os.listdir(path), desc="reduce images", ascii=False, ncols=75):
        if file.endswith(".png"):
            #on réduit de la taille de l'image de 50%
            image = Image.open(path + '\\' + file)
            x = int(image.size[0] * 0.5)
            y = int(image.size[1] * 0.5)
            if x > 112 and y > 112:
                image = image.resize((x,y))
                #on sauvegarde l'image
                image.save(dest_path + '\\' + file)
            else :
                #on ferme l'image
                image.close()
    if create_gif(dest_path, dest_path) == False:
        return "ERROR"


#fonction main qui lance toutes les fonctions
def main(path):
    path = path
    path = parcour_path(path)
    #assignement des variable a partir de la fonction generate_path
    dest_path,png_path,crop_path,dl_path,result_path,reduced_path = generate_path(path)
    # empty_dir(dest_path)
    # empty_dir(png_path)
    # empty_dir(crop_path)
    #empty_dir(dl_path)
    empty_dir(result_path)
    convert_png(path,png_path)
    parcour(png_path,dest_path)
    parcour_file(dest_path,crop_path)
    if api_enable:
        api(crop_path,dl_path)
        reduce_img(dl_path, reduced_path)
        create_gif(reduced_path, result_path)
    else:
        reduce_img(crop_path, reduced_path)
        create_gif(reduced_path, result_path)
    


mainpath = r"C:\Users\alexa\Documents\save_from_pc\projects perso\twich luxouille\emote\raw"
mainpath = parcour_path(mainpath)

#on parcours tous les dossier dans mainpath on appelle main pour chaque dossier

for root, dirs, files in os.walk(mainpath):
    print("entering folder : ",root)
    for dir in dirs:
        print("-----------------------------------",dir,"-----------------------------------")
        main(mainpath + "\\" + dir)