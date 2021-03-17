from common.recursive_folders import recursive_folders
from common.parallel_programming import parallel_programming
from crawlers.common.conexao_local import cursorConexao
from common_nlp.parserTextoJuridico import parserTextoJuridico
import re, pandas as pd, subprocess


def csv_base(filepath):
    cursor = cursorConexao()
    df = pd.read_csv(filepath, error_bad_lines=False)
    for _, row in df.iterrows():
        # if not re.search(r'penal',row['texto_publicacao'],re.I) and re.search(r'saúde|medicamento|médic',row['texto_publicacao'],re.I) and re.search(r'(concedo|autorizo|defiro).{1,30}(antecipa..o.{1,20}tutela|tutela.{1,20}emerg.ncia|tutela.{,20}antecipada|liminar)',row['texto_publicacao'].lower(),flags=re.DOTALL|re.I):
        if re.search(
            r"previdenciário|inss|instituto nacional.{1,5}seguro social|previdência",
            row["texto_publicacao"].lower(),
            flags=re.DOTALL | re.I,
        ):
            cursor.execute(
                'INSERT INTO previdenciario.extracao (nCnj, texto_publicacao) VALUES ("%s","%s")'
                % (
                    row["numero_processo"],
                    row["texto_publicacao"]
                    .replace("\n", " ")
                    .replace('"', "")
                    .replace("\\", ""),
                )
            )


def main(path_diarios, path_relatorio_final):
    print("comecei", path_diarios)
    rec_f = recursive_folders()
    # parallel = parallel_programming()
    arquivos_path = rec_f.find_files(path_diarios)
    diarios_processar = [i for i in arquivos_path if i[-3:] == "csv"]
    # parallel.run_f_nbatches(csv_base,diarios_processar)
    for d in diarios_processar:
        try:
            csv_base(d)
        except:
            pass
    print("terminei de inserir dados na base")

    # print('gerando o csv com publicacoes')
    # rows = []
    # cursor = cursorConexao()
    # cursor.execute('SELECT nCnj, texto_publicacao from previdenciario.extracao')
    # dados = cursor.fetchall()
    # for numero_processo, texto in dados:
    # 	rows.append({'nCnj':numero_processo, 'texto_publicacao':texto})
    # data_frame = pd.DataFrame(rows, index=[i for i in range(len(rows))])
    # data_frame.to_csv(path_relatorio_final)
    # print('fim')


if __name__ == "__main__":
    path_diarios = [
        "/home/deathstar/Documents/Diarios/Diarios_trf1",
        "/home/deathstar/Documents/Diarios/Diarios_trf3",
        "/home/deathstar/Documents/Diarios/Diarios_trf4",
        "/home/deathstar/Documents/Diarios/Diarios_trf5",
    ]
    for p in path_diarios:
        main(p, "")
