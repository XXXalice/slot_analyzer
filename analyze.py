from tqdm import tqdm
import os

class Analyzer:
    def __init__(self):
        self.version = "0.1.0"
        self.dir_name = "files"
        self._print_about()


    def collect_datas(self):
        print("csvファイルをロードします")
        files = os.listdir(f"./{self.dir_name}")
        files = [file for file in files if file[-3:] == "csv"]
        rows = []
        for fname in tqdm(files):
            path = f"./{self.dir_name}/{fname}"
            rows.append(self._fetch_from_file(path))
        print("データのロードに成功しました")
        return rows

    # JSON風dict作成
    # 例
    # {
    #     "アイムジャグラーEX_116": {
    #         "2022-09-06": 102,
    #         "2022-09-07": 99
    #     },
    #     "アイムジャグラーEX_117": {
    #         "2022-09-06": 80,
    #         "2022-09-07": 95
    #     }
    # }
    def total(self, rows):
        data_dict = {}
        for row in rows:
            items = row.split(",")
            # タイトル
            slot_title = items[1]
            # 台番号
            slot_id = items[2]
            slot_name = f"{slot_title}_{slot_id}"



    def _fetch_from_file(self, path):
        with open(path, mode="r") as f:
            rows = [row.rstrip() for row in f.readlines() if row.split(",")[1] != "閉鎖"][1:]
        return rows


    def _print_about(self):
        print("スロットアナライザー")
        print(f"ver {self.version}")


def main():
    analyzer = Analyzer()
    rows = analyzer.collect_datas()



if __name__ == '__main__':
    main()