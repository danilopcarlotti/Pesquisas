import pandas as pd
from main_class import main_class


class create_database(main_class):
    def __init__(self):
        super(create_database, self).__init__()
        self.files = [i for i in self.rec.find_files(self.PATH) if i[-3:] == "csv"]
        self.SEP = ","
        # self.SEP = ';'
        self.ENCODING = "utf-8"
        # self.ENCODING = 'latin-1'

    def create_db(self):
        for f in self.files:
            print(f)
            df = pd.read_csv(f, sep=self.SEP, encoding=self.ENCODING)
            df[self.COLUMN_SOURCE] = df[self.COLUMN_SOURCE].astype(str)
            session = self.myclient.start_session()
            for _, row in df.iterrows():
                normal_text = None
                if len(row[self.COLUMN_SOURCE]) > 5:
                    # if not re.search(r'',row[COLUMN_SOURCE],re.I):
                    #     normal_text = ' '.join(txtN.normalize_texts(row[COLUMN_SOURCE],one_text=True))
                    normal_text = " ".join(
                        self.txtN.normalize_texts(
                            row[self.COLUMN_SOURCE], one_text=True
                        )
                    )
                else:
                    normal_text = " ".join(
                        self.txtN.normalize_texts(
                            row[self.ALTERNATE_COLUMN_SOURCE].split("-")[1],
                            one_text=True,
                        )
                    )
                if normal_text:
                    X = [
                        float(i)
                        for i in list(
                            self.vectorizer.transform([normal_text]).toarray()[0]
                        )
                    ]
                    dic_aux = {}
                    for c in df.columns:
                        dic_aux[c] = row[c]
                    dic_aux["vetor"] = X
                    self.mydb[self.COLLECTION].insert_one(dic_aux)
            self.myclient.admin.command(
                "refreshSessions", [session.session_id], session=session
            )


if __name__ == "__main__":
    cdb = create_database()
    cdb.create_db()
