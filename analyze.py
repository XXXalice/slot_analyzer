import pprint

from tqdm import tqdm
import os
import itertools

class Analyzer:
    def __init__(self, dir_path="files"):
        self.version = "0.1.0"
        self.dir_name = dir_path
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
        return list(itertools.chain.from_iterable(rows))

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
    def get_value_ratio_at_machine(self, rows):
        data_dict = {}
        for row in rows:
            items = row.split(",")
            # タイトル
            slot_title = items[1]
            # 台番号
            slot_id = items[2]
            slot_name = f"{slot_title}_{slot_id}"
            # 日付
            timestamp = items[0]
            # g数
            game_num = int(items[3])
            if game_num == 0:
                continue
            # 差枚数
            diff = int(items[4])
            # 機械割  (G数3)+(差枚数))/(G数3)
            ratio = (game_num * 3 + diff) / (game_num * 3)
            if slot_name not in data_dict:
                data_dict[slot_name] = {}
            data_dict[slot_name][timestamp] = ratio
        return data_dict

    # /     , 2023-01-01, 2023-01-02
    # aaa_12, 98        , 99
    # aaa_13, 100       , 70
    def to_csv(self, data_dict, fname="統計データ.csv"):
        # データに存在する日付
        valid_date_list = [list(slot_param.keys()) for slot_param in data_dict.values()]
        valid_date_list_flatten = sorted(set(itertools.chain.from_iterable(valid_date_list)))
        with open(f"./{fname}", mode="w") as f:
            column = ["機種名_台番号↓/日付→"] + valid_date_list_flatten
            f.write(",".join(column) + "\n")


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
    data_dict = analyzer.get_value_ratio_at_machine(rows=rows)
    analyzer.to_csv(data_dict=data_dict)


if __name__ == '__main__':
    main()