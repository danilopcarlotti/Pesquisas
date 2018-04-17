from common.download_path import path
from pdf_to_text import pdf_to_text
import time, os

arq_go = open("go"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_trf1 = open("trf1"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_trt = open("trt"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_sp = open("sp"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_al = open("al"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_am = open("am"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_ce = open("ce"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_ms = open("ms"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_ro = open("ro"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_to = open("to"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_rn = open("rn"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_ma = open("ma"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_rr = open("rr"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_pi = open("pi"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_df = open("df"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_pa = open("pa"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_stf = open("stf"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_stj = open("stj"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_ap = open("ap"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_trf5 = open("trf5"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_trf4 = open("trf4"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_trf3 = open("trf3"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_trf2 = open("trf2"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_ac = open("ac"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_pr = open("pr"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_sc = open("sc"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_pe = open("pe"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_rs = open("rs"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_pb = open("pb"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_ba = open("ba"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_rj = open("rj"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_mg = open("mg"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_se = open("se"+dia+mes+ano+".txt",'a',encoding="utf-8")
arq_mt = open("mt"+dia+mes+ano+".txt",'a',encoding="utf-8")

arqs_i = os.listdir(path)
arqs_f = []
pdf_2_txt = pdf_to_text()

re_diarios = [[r".+MA\.pdf$",arq_ma],[r".+RO\.pdf$",arq_ro],[r".+PA\.pdf$",arq_pa],[r".+TO\.pdf$",arq_to],[r".+STF\.pdf$",arq_stf],\
              [r".+RR\.pdf$",arq_rr],[r".+PI\.pdf$",arq_pi],[r".+MT\.pdf$",arq_mt],[r".+SE\.pdf$",arq_se],[r"^Diário.*?.pdf$",arq_trf5],\
              [r".+STJ\.pdf$",arq_stj],[r"\d.+TRF1\.pdf$",arq_trf1],[r"\d+GO\.pdf$",arq_go],[r"^Diario_\d{4}_.+\.pdf$",arq_trt],\
              [r"^tjapDJE.+\.pdf$",arq_ap],[r".+RN\.pdf$",arq_rn],[r"^de_jud_"+ano+mes+dia+"\d+.+\.pdf$",arq_trf4],[r"^de_[jJ]ud.+TRF.+\.pdf$",arq_trf3],\
              [r"^DE"+ano+mes+dia+"\.pdf$",arq_ac],[r"^Diário da Justi.+\.pdf$",arq_pr],[r"^diario_\d+_cad.+\.pdf$",arq_sc],\
              [r"^caderno\d-Judicial.+\.pdf$",arq_sp],[r"^Caderno\d-Jurisdicional.+\.pdf$",arq_al],\
              [r"^Caderno\d-Judiciario.+\.pdf$",arq_am],[r"^Caderno4.+\.pdf$",arq_am],[r"^caderno2-Judiciario\.pdf$",arq_ce],[r"^Caderno\d-Judicial.+\.pdf$",arq_ms],\
              [r"^\d+\.pdf$",arq_rs],[r"^diario_\d+-\d+-\d+\.pdf$",arq_pb],[r"^bahia.pdf$",arq_ba],[r"^riodejaneiro\d+.pdf$",arq_rj],\
              [r"^CADERNO_\d+_.+.pdf$",arq_trf2],[r"^DJ.+\.PDF$",arq_pe],[r"^DJ.+\.PDF$",arq_df]]

for i in arqs_i:
    if i not in arqs_f:
        for d in re_diarios:
            aux = re.search(d[0],i)
            if aux != None:
                try:
                    d[1].write(pdf_2_txt.convert_pdfminer(i))
                    arqs_f.append(i)
                    break
                except:
                    # log?
                    pass