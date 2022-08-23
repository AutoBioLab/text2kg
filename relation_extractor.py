import os
import subprocess
import glob
import pandas as pd

manipulate_list=["add","agitate","aliquot","aspirate","bake","batch","calibrate","catalysis","catalyst","centrifuge","chop","mince","chromatograph","clump","coat","collect","combine","combustion","concentrate","condense","crush","decant","dehydrate","digest","dilute","discard","dissolution","dissolve","distill","down","droplet","electrophoresis","electrotransformation","elute","equilibrate","evaporate","extract","fermentation","filtrate","filtration","flow","foster","grind","harvest","homogenize","hydrolysis","incubate","inoculate","lysate","measure","mix","neutralize","normalize","passage","pellet","perfusion","pipette","plate","precipitate","probe","purify","quench","remove","replace","resuspend","rinse","screen","sediment","shake","slurry","spin","sterilize","suction","supernatant","thaw","transfer","transform","turbid","ultrasonication","ventilate","viscous","vortex"]
def Stanford_Relation_Extractor():

    
    print('Relation Extraction Started')

    for f in glob.glob(os.getcwd() + "/data/output/kg/*.txt"):        
        print("Extracting relations for " + f.split("/")[-1])
        current_directory = os.getcwd()
        os.chdir(current_directory + '/stanford-openie')

        p = subprocess.Popen(['./process_large_corpus.sh',f,f + '-out.csv'], stdout=subprocess.PIPE)

        output, err = p.communicate()
   

    print('Relation Extraction Completed')


if __name__ == '__main__':

    Stanford_Relation_Extractor()
