def extractseq(goi,ref):
    import pandas as pd 
    from pandas import DataFrame
    import Bio
    from Bio import SeqIO
    from Bio.SeqUtils import GC
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord
    from Bio.Align import MultipleSeqAlignment
    from Bio.Align.Applications import ClustalwCommandline
    import collections
    from Bio import AlignIO
    import random
    import numpy as np
    in_f =open (ref, 'r+')
    seqs=[]
    su=0
    for line in in_f:
    #    print(line)
        if su==1:
            if line[0]=='>':
                su=0
                if lout[0]!='>':
    #                print(lout)
                    seqs.append(lout)
            else:
                lout=lout+line[:-1]       
        if line in goi:
            seqs.append(line)
            su=1
            lout=''
    return seqs

def extract_seqs(genes,ref,column='Gene'):
    import pandas as pd 
    from pandas import DataFrame
    import Bio
    from Bio import SeqIO
    from Bio.SeqUtils import GC
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord
    from Bio.Align import MultipleSeqAlignment
    from Bio.Align.Applications import ClustalwCommandline
    import collections
    from Bio import AlignIO
    import random
    import numpy as np
    in_f =open (ref, 'r+')
    headers=list()
    for line in in_f:
    #    print(line)
        if line[0] == '>':
            headers.append(line)
    #        print(line)
    dictionary=dict()
    header=[]
    seq=[]
    genesexp=genes[column].unique()
    listo=[]
    lista=[]
    for ici in genesexp:
        icis='('+ici+')'
        matching = [s for s in headers if icis in s]
        lista.append(len(matching))
        listo.append(matching)
    
    return(genesexp,listo,lista)

def findtargets (mrna,refpath,ie,outfiles,plp_length=30,gc_min=50,gc_max=65):
    import pandas as pd 
    from pandas import DataFrame
    import Bio
    from Bio import SeqIO
    from Bio.SeqUtils import GC
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord
    from Bio.Align import MultipleSeqAlignment
    from Bio.Align.Applications import ClustalwCommandline
    import collections
    from Bio import AlignIO
    import random
    import numpy as np
    targets = pd.DataFrame(columns=['Gene', 'Position', 'Sequence'])
    end = len(mrna)-(plp_length-1)
    #print (end)
    for i in range (0, end):
        #print (mrna[i:i+30])
    #The next line checks if position 16 (remember python is 0-indexed) is a C or G
        if mrna.seq[i+round(plp_length/2)] == 'C' or mrna.seq[i+round(plp_length/2)] == 'G' :
            #The next line filters out any probe with GC content <= 50 and >=65
            if GC(mrna.seq[i:i+plp_length]) > gc_min:
                if GC(mrna.seq[i:i+plp_length]) < gc_max:
                    if mrna.seq[i:i+plp_length].count("AAA")==0 and mrna.seq[i:i+plp_length].count("TTT")==0 and mrna.seq[i:i+plp_length].count("GGG")==0 and mrna.seq[i:i+plp_length].count("CCC")==0:
                    #Here I create a dataframe with all the suitable targets, where column 1 is the start position and column 2 is the actual sequence.
                        #print (GC(mrna.seq[i:i+30]))
                        targets = targets.append({'Gene': mrna.id, 'Position': i, 'Sequence':mrna.seq[i:i+plp_length]}, ignore_index=True)  
                        pato=refpath+ '/target_regions_'+mrna.id+'_'+str(ie)+'.csv'
                        outfiles.append(pato)
                        targets.to_csv(pato)
    return [targets,outfiles]   


def plot_alignment(refpath,alignment,common):
    import pandas as pd 
    from pandas import DataFrame
    import Bio
    from Bio import SeqIO
    from Bio.SeqUtils import GC
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord
    from Bio.Align import MultipleSeqAlignment
    from Bio.Align.Applications import ClustalwCommandline
    import collections
    from Bio import AlignIO
    import random
    import numpy as np
    import matplotlib.pyplot as plt
    fig=plt.figure(figsize=(10,3))
    plt.plot(range(0,alignment.get_alignment_length()),common,c='grey')
    plt.hlines(len(alignment)+0.1,linestyles='--',xmin=0,xmax=alignment.get_alignment_length(),colors='r')
    plt.xlim([0,alignment.get_alignment_length()])
    plt.savefig(refpath+'/common_regions_though_variants.png')
    plt.close(fig)





def extract_and_align(genes,ref,path,pathclustal):
    import pandas as pd 
    import os
    from pandas import DataFrame
    import Bio
    from Bio import SeqIO
    from Bio.SeqUtils import GC
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord
    from Bio.Align import MultipleSeqAlignment
    from Bio.Align.Applications import ClustalwCommandline
    import collections
    from Bio import AlignIO
    import random
    import numpy as np
    import matplotlib.pyplot as plt
    isExist = os.path.exists(path+'/gene_info')
    if not isExist:
        os.makedirs(path+'/gene_info') 
    outfiles=[]
    genesexp,listoref,lista=extract_seqs(genes,ref)
    listaref=lista
    lista=[]
    listo=[]
    for el in listoref:
        ls=[]
        for ele in el:
            check=ele.find('PREDICTED')==-1
            if check==True:
                ls.append(ele)
        lista.append(len(ls))
        listo.append(ls)
    notfound=[]
    for holi in range(0,len(genesexp)):
        ie=0
        refpath=path+"/gene_info/"+genesexp[holi]
        if lista[holi]<2:
            if lista[holi]==0:
                print("Gene "+genesexp[holi] +" was not found")
                notfound.append(genesexp[holi])
            if lista[holi]==1:
                gen=genesexp[holi]
                goi=listo[holi]
                print('Starting '+gen)
                refpath=path+'/gene_info'+'/'+gen
                import os
                if not os.path.exists(refpath):
                    os.makedirs(refpath)
                seqs=extractseq(goi,ref)
                with open(refpath+'/seqs.fasta', 'w') as f:
                    comseq=1
                    for item in seqs:
                        f.write(">"+ gen+ " Seq"+str(comseq)+ "\n" )
                        f.write("%s\n" % item)
                        comseq=comseq+1
                    records=[]
                for ia in range(0,len(goi)-1):
                    records.append(SeqRecord(Seq(seqs[ia]),id=goi[ia]))       
                ie=0
                for seq_record in SeqIO.parse(refpath+"/seqs.fasta", "fasta"):
                    ie=ie+1
                    seq_record = seq_record.upper()
                    targetsall,outfiles = findtargets(seq_record,refpath,ie,outfiles)       
        else:   
            gen=genesexp[holi]
            goi=listo[holi]
            print('Starting '+gen)
            print()
            refpath=path+'/gene_info'+'/'+gen
            import os
            if not os.path.exists(refpath):
                os.makedirs(refpath)
            seqs=extractseq(goi,ref)
            with open(refpath+'/seqs.fasta', 'w') as f:
                for item in seqs:
                    f.write("%s\n" % item)
            clustalw_exe = pathclustal
            cmd = ClustalwCommandline(clustalw_exe,
            infile=refpath+'/seqs.fasta')
            stdout, stderr = cmd()
            alignment = AlignIO.read(refpath+'/seqs.aln', "clustal")
            st=''
            cseqs=[]
            common=[]
            for esa in range(0,alignment.get_alignment_length()):
                un=alignment[:,esa]
                col=collections.Counter(un).most_common(1)[0]
                common.append(col[1])
                if col[1]==len(alignment):
                    st=st+str(col[0])
                else:
                    if len(st)>35:
                        cseqs.append(st)
            #            cseqs=[]
                        st=''
            if len(st)>35:
                        cseqs.append(st)
                        st=''
            freqseq=np.zeros([len(alignment[:,1]),int(alignment.get_alignment_length())])
            for es2 in range(0,alignment.get_alignment_length()):
                        un=alignment[:,es2]
                        for pos2 in range(0,len(un)):
                            if un[pos2]=='-':
                                freqseq[pos2,es2]==0
                            else:
                                cnt=0
                                for el in un:
                                    cnt=cnt+(un[pos2]==el)*1
                                freqseq[pos2,es2]=cnt

            plot_alignment(refpath,alignment,common)
            plot_alignment_of_variants(refpath,freqseq,alignment)
            with open(refpath+'/aligned_seqs.fasta', 'w') as f:
                comseq=1
                for item in cseqs:
                    f.write(">"+ gen+ " Seq"+str(comseq)+ "\n" )
                    f.write("%s\n" % item)
                    comseq=comseq+1
            records=[]
            for ia in range(0,len(goi)-1):
                records.append(SeqRecord(Seq(seqs[ia]),id=goi[ia]))       
            # Loads fasta
            ie=0
            for seq_record in SeqIO.parse(refpath+"/aligned_seqs.fasta", "fasta"):
                seq_record = seq_record.upper()
                #print (seq_record)
                ie=ie+1
                targetsall,outfiles = findtargets(seq_record,refpath,ie,outfiles)
    #           print(targetsall)
    of=pd.DataFrame(outfiles)
    of.to_csv(path+'/outfiles.csv')
    selected,unigene=retrieve_targets(outfiles,path)
    hits=dict(zip(genesexp,listaref))
    selected['exp_hits']=selected['Gene'].map(hits)
    return selected,unigene,notfound




def retrieve_targets(outfiles,path):
    print("Extracting all possible targets for all genes")
    import numpy as np
    import pandas as pd
#    outfiles=pd.DataFrame(outfiles)
#    outfiles.to_csv(path+'/outfiles.csv')
    fil=np.unique(outfiles)
    pan=pd.read_csv(fil[0])
    for s in fil:
       pe=pd.read_csv(s)
       pan=pd.concat([pan,pe])
    selected=pd.DataFrame(pan,columns=pan.columns)
    unigene=pan['Gene'].unique()
    return selected,unigene



def select_sequences(path,selected,genes_required,number_of_selected,subgroup=1):
    import pandas as pd
    import random 
    pan=selected
    selected2=pd.DataFrame(columns=selected.columns)
    unigene=genes_required
    for e in unigene:
        ele=pan[pan['Gene']==e]
        if ele.shape[0]<number_of_selected:
            sele=ele
        else:    
            randomlist = random.sample(range(0, ele.shape[0]), number_of_selected) 
            sele=ele.iloc[randomlist,:]
        selected2=pd.concat([selected2,sele])
    selected2.to_csv(path+'/selected_targets_group'+str(subgroup)+'.csv')
    return selected2

def check_plps(bcf_all,final_designed,genes,path,subgroup=1):
    import pandas as pd
    import numpy as np
    import random
    bcf_all2=bcf_all[bcf_all['Gene'].isin(genes['Gene'])]
    bcf_all['same']=(bcf_all['exp_hits']==bcf_all['number_of_hits'])*1
    bcf=bcf_all.loc[bcf_all['same'].isin([1])]
    bcfexc=bcf_all.loc[~bcf_all['same'].isin([1])]
    bcfexc_todesign=bcfexc[~bcfexc['Gene'].isin(bcf['Gene'])]
    bcfexc_todesign=bcfexc_todesign[bcfexc_todesign['Gene'].isin(genes['Gene'])]
    nondesigned=bcf_all2[~bcf_all2['Gene'].isin(bcf['Gene'])]
    ND=nondesigned[nondesigned['Gene'].isin(genes['Gene'])]
    ND.to_csv(path+'/untargeted_genes.csv')
    selected=pd.DataFrame(columns=bcf.columns)
    unigene=bcf['Gene'].unique()
    for e in unigene:
        ele=bcf[bcf['Gene']==e]
        if ele.shape[0]<final_designed:
            sele=ele
        else:    
            randomlist = random.sample(range(0, ele.shape[0]), final_designed) 
            sele=ele.iloc[randomlist,:]
        selected=pd.concat([selected,sele])
    bcf=selected
    bcf.to_csv(path+'/good_targets'+str(subgroup)+'.csv')
    genes_too_low_PLPs=bcf.groupby(['Gene']).count()[bcf.groupby(['Gene']).count()['hits']<final_designed]
    genes_too_low_PLPs=genes_too_low_PLPs.iloc[:,0:1]
    genes_too_low_PLPs.columns=['number_of_PLPs']
    genes_good_PLPs=bcf.groupby(['Gene']).count()[bcf.groupby(['Gene']).count()['hits']>(final_designed-1)]
    genes_good_PLPs=genes_good_PLPs.iloc[:,0:1]
    genes_good_PLPs.columns=['number_of_PLPs']
    genes_too_low_PLPs=bcf.groupby(['Gene']).count()[bcf.groupby(['Gene']).count()['hits']<final_designed]
    genes_too_low_PLPs= genes_too_low_PLPs.iloc[:,0:1]
    genes_too_low_PLPs.columns=['number_of_PLPs']
    genes_no_PLPs=bcfexc_todesign['Gene'].unique()
    bcf.to_csv(path+'/specific_targets_'+str(subgroup)+'.csv')
    return bcf,genes_good_PLPs, genes_too_low_PLPs, genes_no_PLPs


def build_plps(path,specific_seqs_final,L_probe_library,plp_length,how='start',on=201): #starts, end, customized
    import pandas as pd
    import numpy as np
    from Bio.Seq import Seq
    import Bio
    from Bio import SeqIO
    from Bio.SeqUtils import GC
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord
    from Bio.Align import MultipleSeqAlignment
    from Bio.Align.Applications import ClustalwCommandline
    import collections
    from Bio import AlignIO
    import random
    import numpy as np
    bcf=specific_seqs_final
    if how=='customized':
#        print(customized)
        selected_ID_to_gene=pd.read_csv(on,sep=',')
        column_names = ["Larm", "idseq", "anchor", "Rarm","LbarID", "AffyID", "Gene"]
        probesP1 = pd.DataFrame (columns = column_names)
        gene_names_ID_columns = ['gene', "idseq", 'Lbar_ID', 'AffyID']
        gene_names_ID = pd.DataFrame(columns=gene_names_ID_columns)
        sbh=pd.read_csv(L_probe_library)
        gene2ID=dict(zip(selected_ID_to_gene['Gene'],selected_ID_to_gene['Lbar_ID']))
        gname = bcf['Gene']
        gname = gname.unique()
        column_names = ["Larm", "idseq", "anchor", "Rarm", "AffyID", "Gene"]
        n=0
        for g in gname:
            gene_names_ID = gene_names_ID.append({"gene": g, "idseq" : np.array(sbh.loc[sbh['Lbar_ID']==gene2ID[g],'ID_Seq'])[0], "Lbar_ID" : str(np.array(sbh.loc[sbh['Lbar_ID']==gene2ID[g],'Lbar_ID'])[0]), "AffyID" : np.array(sbh.loc[sbh['Lbar_ID']==gene2ID[g],'L_Affy_ID'])[0] }, ignore_index=True)
            n=n+1
        gene_names_ID2=gene_names_ID.set_index("gene", drop = False)
        dictiocodes=dict(zip(sbh['L_Affy_ID'],sbh['Barcode_Combi']))
        gene_names_ID2['code']=list(gene_names_ID2['AffyID'].map(dictiocodes))
        gene_names_ID2.to_csv(path+'/codebook.csv')
    if how=='start':
        #this step assings a unique barcode to a gene (meaning that all the probes for the same gene will have the same barcode)
        #generate an empty dataframe to populate with the probe sequence, and useful counters to access stats at the end.
        #ID=LbarID-200
        gname = bcf['Gene']
        gname = gname.unique()
        column_names = ["Larm", "idseq", "anchor", "Rarm","LbarID", "AffyID", "Gene"]
        probesP1 = pd.DataFrame (columns = column_names)
        gene_names_ID_columns = ['gene', "idseq", 'Lbar_ID', 'AffyID']
        gene_names_ID = pd.DataFrame(columns=gene_names_ID_columns)
        ID=on
        sbh=pd.read_csv(L_probe_library)
        n=0
        for g in gname:
            gene_names_ID = gene_names_ID.append({"gene": g, "idseq" : np.array(sbh.loc[sbh['number']==ID+n,'ID_Seq'])[0], "Lbar_ID" : str(np.array(sbh.loc[sbh['number']==ID+n,'Lbar_ID'])[0]), "AffyID" : np.array(sbh.loc[sbh['number']==ID+n,'L_Affy_ID'])[0] }, ignore_index=True)
            n=n+1
        gene_names_ID2=gene_names_ID.set_index("gene", drop = False)
        dictiocodes=dict(zip(sbh['L_Affy_ID'],sbh['Barcode_Combi']))
        gene_names_ID2['code']=list(gene_names_ID2['AffyID'].map(dictiocodes))
        gene_names_ID2.to_csv(path+'/codebook.csv')
    if how=='end':
        #this step assings a unique barcode to a gene (meaning that all the probes for the same gene will have the same barcode)
        #generate an empty dataframe to populate with the probe sequence, and useful counters to access stats at the end.
        #ID=LbarID-200
        gname = bcf['Gene']
        gname = gname.unique()
        column_names = ["Larm", "idseq", "anchor", "Rarm","LbarID", "AffyID", "Gene"]
        probesP1 = pd.DataFrame (columns = column_names)
        gene_names_ID_columns = ['gene', "idseq", 'Lbar_ID', 'AffyID']
        gene_names_ID = pd.DataFrame(columns=gene_names_ID_columns)
        ID=on-len(gname)
        sbh=pd.read_csv(L_probe_library)
        n=0
        for g in gname:
            gene_names_ID = gene_names_ID.append({"gene": g, "idseq" : np.array(sbh.loc[sbh['number']==ID+n,'ID_Seq'])[0], "Lbar_ID" : str(np.array(sbh.loc[sbh['number']==ID+n,'Lbar_ID'])[0]), "AffyID" : np.array(sbh.loc[sbh['number']==ID+n,'L_Affy_ID'])[0] }, ignore_index=True)
            n=n+1
        gene_names_ID2=gene_names_ID.set_index("gene", drop = False)
        dictiocodes=dict(zip(sbh['L_Affy_ID'],sbh['Barcode_Combi']))
        gene_names_ID2['code']=list(gene_names_ID2['AffyID'].map(dictiocodes))
        gene_names_ID2.to_csv(path+'/codebook.csv')
    for index, row in bcf.iterrows():
        r = (row['Gene'])
        x = Seq(row['Sequence'])
        y = x.reverse_complement()
        y = y.upper()
        if y[round(plp_length/2)-1] == "C" or y[round(plp_length/2)-1] == "G":
            probesP1 = probesP1.append({"Rarm": str(y[0:round(plp_length/2)]), "Larm": str(y[round(plp_length/2):plp_length]), "anchor" : "TGCGTCTATTTAGTGGAGCC", "idseq" : gene_names_ID2.loc[r]['idseq'], "Lbar_ID" : gene_names_ID2.loc[r]['Lbar_ID'], "AffyID" : gene_names_ID2.loc[r]['AffyID'], "Gene" : gene_names_ID2.loc[r]['gene'] }, ignore_index=True)
            n=n+1
        else:
            print ("Are you sure you have a C or G at the ligation site?")
    print ("I just processed",n,"unique target sequences. I am done")
    #The "probes" dataframe at this stage contains the sequences of the probes, before transforming the last base to RNA for ordering 
    probe_col = ["sequence","Lbar_ID", "AffyID", "Gene"]
    probes = pd.DataFrame (columns = probe_col)
    probes["sequence"] = probesP1 ["Larm"] + probesP1 ["idseq"]+ probesP1 ["anchor"]+ probesP1["Rarm"]
    probes["Lbar_ID"] = probesP1 ["Lbar_ID"]
    probes["AffyID"] = probesP1 ["AffyID"]
    probes["Gene"]= probesP1["Gene"]
    # In[ ]: this bit of the script extracts the 3' terminal base of each probe, converts it to RNA code for IDT and rewrites the sequence in the dataframe. Then it outputs a CSV file.
    rnaprobes = []
    for pad in probes.itertuples():
        capt = pad.sequence
        rnabase = (capt[-1])
        plp = (capt [0:-1]+"r"+rnabase)
        rnaprobes.append (plp)
        #print (plp)
    #print (rnaprobes)
    probes["sequence"] = rnaprobes
    #print (probes)
    probes['code']=list(probes['AffyID'].map(dictiocodes))
    probes.to_csv(path+'/designed_PLPs_final.csv')
    return probes






def extract_align_variants(genes,ref,path,pathclustal,selection):
    import pandas as pd 
    import os
    from pandas import DataFrame
    import Bio
    from Bio import SeqIO
    from Bio.SeqUtils import GC
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord
    from Bio.Align import MultipleSeqAlignment
    from Bio.Align.Applications import ClustalwCommandline
    import collections
    from Bio import AlignIO
    import random
    import numpy as np
    import matplotlib.pyplot as plt
    genes=genes.loc[genes['Gene']==selection,:]
    isExist = os.path.exists(path+'/gene_info')
    if not isExist:
        os.makedirs(path+'/gene_info') 
    outfiles=[]
    genesexp,listoref,lista=extract_seqs(genes,ref)
    listaref=lista
    lista=[]
    listo=[]
    for el in listoref:
        ls=[]
        for ele in el:
            check=ele.find('PREDICTED')==-1
            if check==True:
                ls.append(ele)
        lista.append(len(ls))
        listo.append(ls)
    
    
    for holi in range(0,len(genesexp)):
        ie=0
        notfound=[]
        refpath=path+"/gene_info/"+genesexp[holi]
        if lista[holi]<2:
            if lista[holi]==0:
                print("Gene "+genesexp[holi] +" was not found")
                notfound.append(genesexp[holi])
            if lista[holi]==1:
                gen=genesexp[holi]
                goi=listo[holi]
                print('Starting '+gen)
                refpath=path+'/gene_info'+'/'+gen
                import os
                if not os.path.exists(refpath):
                    os.makedirs(refpath)
                seqs=extractseq(goi,ref)
                with open(refpath+'/seqs_variants.fasta', 'w') as f:
                    comseq=1
                    for item in seqs:
                        f.write(">"+ gen+ " Seq"+str(comseq)+ "\n" )
                        f.write("%s\n" % item)
                        comseq=comseq+1
                    records=[]
                for ia in range(0,len(goi)-1):
                    records.append(SeqRecord(Seq(seqs[ia]),id=goi[ia]))       
                ie=0
                for seq_record in SeqIO.parse(refpath+"/seqs_variants.fasta", "fasta"):
                    ie=ie+1
                    seq_record = seq_record.upper()
                    targetsall,outfiles = findtargets(seq_record,refpath,ie,outfiles)       
        else:   
            gen=genesexp[holi]
            goi=listo[holi]
            print('Starting '+gen)
            print()
            refpath=path+'/gene_info'+'/'+gen
            import os
            if not os.path.exists(refpath):
                os.makedirs(refpath)
            seqs=extractseq(goi,ref)
            with open(refpath+'/seqs_variants.fasta', 'w') as f:
                for item in seqs:
                    f.write("%s\n" % item)
            clustalw_exe = pathclustal
            cmd = ClustalwCommandline(clustalw_exe,
            infile=refpath+'/seqs_variants.fasta')
            stdout, stderr = cmd()
            alignment = AlignIO.read(refpath+'/seqs_variants.aln', "clustal")
            st=''
            cseqs=[]
            common=[]
            for esa in range(0,alignment.get_alignment_length()):
                un=alignment[:,esa]
                col=collections.Counter(un).most_common(1)[0]
                common.append(col[1])
                if col[1]==len(alignment):
                    st=st+str(col[0])
                else:
                    if len(st)>35:
                        cseqs.append(st)
            #            cseqs=[]
                        st=''
            if len(st)>35:
                        cseqs.append(st)
                        st=''
            freqseq=np.zeros([len(alignment[:,1]),int(alignment.get_alignment_length())])
            for es2 in range(0,alignment.get_alignment_length()):
                        un=alignment[:,es2]
                        for pos2 in range(0,len(un)):
                            if un[pos2]=='-':
                                freqseq[pos2,es2]==0
                            else:
                                cnt=0
                                for el in un:
                                    cnt=cnt+(un[pos2]==el)*1
                                freqseq[pos2,es2]=cnt

            plot_alignment(refpath,alignment,common)
            plot_alignment_of_variants(refpath,freqseq,alignment)
    return genesexp,listo,lista


def plot_alignment_of_variants(refpath,freqseq,alignment):
    import pandas as pd 
    import Bio
    import matplotlib.pyplot as plt
    from Bio import SeqIO
    from Bio.SeqUtils import GC
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord
    from Bio.Align import MultipleSeqAlignment
    from Bio.Align.Applications import ClustalwCommandline
    import collections
    from Bio import AlignIO
    import random
    import numpy as np
    colors=['r','b','g','c','o','p','y','r','b','g','c','o','r','b','g','c','o','r','b','g','c','o','r','b','g','c','o','p','y','r','b','g','c','o','r','b','g','c','o','r','b','g','c','o']
    fig, ax = plt.subplots(figsize=(10,(5*(np.size(freqseq,axis=0)))),nrows=np.size(freqseq,axis=0),ncols=1)  
    for s in range(0,np.size(freqseq,axis=0)):
        ax[s].plot(range(0,alignment.get_alignment_length()),freqseq[s,:],c=colors[s])
        ax[s].set_title(alignment[s].id)
#        ax[s].set_xlab('Bases of the transcript')
#        ax[s].set_ylab('Numb. of variants matching the base')
        ax[s].hlines(len(alignment)+0.01,linestyles='--',xmin=0,xmax=alignment.get_alignment_length(),colors=[0,0,0])

    plt.savefig(refpath+'/common_regions_though_variants.png')


def extract_seqs_for_variants(path,genesexp,listo,lista,ref,pathclustal):
    import pandas as pd 
    import Bio
    from Bio import SeqIO
    from Bio.SeqUtils import GC
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord
    from Bio.Align import MultipleSeqAlignment
    from Bio.Align.Applications import ClustalwCommandline
    import collections
    from Bio import AlignIO
    import random
    import numpy as np
    outfiles=[]
    for holi in range(0,len(genesexp)):
        ie=0
        notfound=[]
        refpath=path+"/gene_info/"+genesexp[holi]
        if lista[holi]<2:
            if lista[holi]==0:
                print("Gene "+genesexp[holi] +" was not found")
                notfound.append(genesexp[holi])
            if lista[holi]==1:
                gen=genesexp[holi]
                goi=listo[holi]
                print('Starting '+gen)
                refpath=path+'/gene_info'+'/'+gen
                import os
                if not os.path.exists(refpath):
                    os.makedirs(refpath)
                seqs=extractseq(goi,ref)
                with open(refpath+'/seqs.fasta', 'w') as f:
                    comseq=1
                    for item in seqs:
                        f.write(">"+ gen+ " Seq"+str(comseq)+ "\n" )
                        f.write("%s\n" % item)
                        comseq=comseq+1
                    records=[]
                for ia in range(0,len(goi)-1):
                    records.append(SeqRecord(Seq(seqs[ia]),id=goi[ia]))       
                ie=0
                for seq_record in SeqIO.parse(refpath+"/seqs.fasta", "fasta"):
                    ie=ie+1
                    seq_record = seq_record.upper()
                    targetsall,outfiles = findtargets(seq_record,refpath,ie,outfiles)       
        else:   
            gen=genesexp[holi]
            goi=listo[holi]
            print('Starting '+gen)
            print()
            refpath=path+'/gene_info'+'/'+gen
            import os
            if not os.path.exists(refpath):
                os.makedirs(refpath)
            seqs=extractseq(goi,ref)
            with open(refpath+'/seqs.fasta', 'w') as f:
                for item in seqs:
                    f.write("%s\n" % item)
            clustalw_exe = pathclustal
            cmd = ClustalwCommandline(clustalw_exe,
            infile=refpath+'/seqs.fasta')
            stdout, stderr = cmd()
            alignment = AlignIO.read(refpath+'/seqs.aln', "clustal")
            st=''
            cseqs=[]
            common=[]
            for esa in range(0,alignment.get_alignment_length()):
                un=alignment[:,esa]
                col=collections.Counter(un).most_common(1)[0]
                common.append(col[1])
                if col[1]==len(alignment):
                    st=st+str(col[0])
                else:
                    if len(st)>35:
                        cseqs.append(st)
            #            cseqs=[]
                        st=''
            if len(st)>35:
                        cseqs.append(st)
                        st=''
            plot_alignment(refpath,alignment,common)
            with open(refpath+'/aligned_seqs.fasta', 'w') as f:
                comseq=1
                for item in cseqs:
                    f.write(">"+ gen+ " Seq"+str(comseq)+ "\n" )
                    f.write("%s\n" % item)
                    comseq=comseq+1
            records=[]
            for ia in range(0,len(goi)-1):
                records.append(SeqRecord(Seq(seqs[ia]),id=goi[ia]))       
            # Loads fasta
            ie=0
            for seq_record in SeqIO.parse(refpath+"/aligned_seqs.fasta", "fasta"):
                seq_record = seq_record.upper()
                #print (seq_record)
                ie=ie+1
                targetsall,outfiles = findtargets(seq_record,refpath,ie,outfiles)
    #           print(targetsall)
    of=pd.DataFrame(outfiles)
    of.to_csv(path+'/outfiles.csv')
    selected,unigene=retrieve_targets(outfiles,path)
    hits=dict(zip(genesexp,lista))
    selected['exp_hits']=selected['Gene'].map(hits)
    return selected,unigene,notfound
