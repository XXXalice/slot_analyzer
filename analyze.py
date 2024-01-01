import pprint

from tqdm import tqdm
import os
import itertools

class Analyzer:
    def __init__(self, dir_path="files"):
        self.version = "0.2.0"
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



    # get_value_ratio_at_machine()のパーセンテージver
    def get_value_ratio_percent_at_machine(self, rows, dcm_place=1):
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
            percent = round(ratio * 100, dcm_place)
            if slot_name not in data_dict:
                data_dict[slot_name] = {}
            data_dict[slot_name][timestamp] = percent
        return data_dict


    # 機種番号ではなくタイトルで様って出す
    def get_get_value_ratio_percent_at_title(self, rows, dcm_place=1):
        data_dict = {}
        for row in rows:
            items = row.split(",")
            # タイトル
            slot_title = items[1]
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
            percent = round(ratio * 100, dcm_place)
            # dictにタイトルが記録されていないとき
            if slot_title not in data_dict:
                # タイトルを空のdictで初期化
                data_dict[slot_title] = {}
            # data_dictの[slot_title]にtimestampが登録されてないとき
            if timestamp not in data_dict[slot_title]:
                # [タイトル][timestamp]に機械割集計用のリストを導入
                data_dict[slot_title][timestamp] = []
            # パーセント導入
            data_dict[slot_title][timestamp].append(percent)

        return data_dict


    # /     , 2023-01-01, 2023-01-02
    # aaa_12, 98        , 99
    # aaa_13, 100       , 70
    def to_csv(self, data_dict, fname="統計データ.csv"):
        # データに存在する日付
        valid_date_list = [list(slot_param.keys()) for slot_param in data_dict.values()]
        valid_date_list_flatten = sorted(set(itertools.chain.from_iterable(valid_date_list)))
        with open(f"./{fname}", mode="w", encoding="utf-8") as f:
            column = ["機種名_台番号↓/日付→"] + valid_date_list_flatten
            f.write(",".join(column) + "\n")

            # 縦軸
            slot_specs = list(data_dict.keys())
            for slot_name in slot_specs:
                rows = []
                rows.append(slot_name)
                slot_data_dict = data_dict.get(slot_name)
                # 横列
                slot_spec_data_list = []
                for valid_date in valid_date_list_flatten:
                    if valid_date in slot_data_dict.keys():
                        # valid_date（例2023-11-11）に該当するマシンのデータがあった場合
                        slot_spec_data_list.append(str(slot_data_dict[valid_date]))
                    else:
                        # valid_date（例2023-11-11）に該当するマシンのデータがなかった場合
                        slot_spec_data_list.append("-")

                slot_row = rows + slot_spec_data_list
                f.write(",".join(slot_row) + "\n")


    # 多機種でsummaryを出す場合に使用するto_csv()
    def to_csv_summary(self, data_dict, fname="統計データ.csv", dcm_place=1):
        # データに存在する日付
        valid_date_list = [list(slot_param.keys()) for slot_param in data_dict.values()]
        valid_date_list_flatten = sorted(set(itertools.chain.from_iterable(valid_date_list)))
        with open(f"./{fname}", mode="w", encoding="utf-8") as f:
            column = ["機種名_台番号↓/日付→"] + valid_date_list_flatten
            f.write(",".join(column) + "\n")

            # 縦軸
            slot_specs = list(data_dict.keys())
            for slot_name in slot_specs:
                rows = []
                rows.append(slot_name)
                slot_data_dict = data_dict.get(slot_name)
                # 横列
                slot_spec_data_list = []
                for valid_date in valid_date_list_flatten:
                    if valid_date in slot_data_dict.keys():
                        data_list = slot_data_dict[valid_date]
                        summary_data = round(sum(data_list) / len(data_list), 1)
                        slot_spec_data_list.append(str(summary_data))
                    else:
                        # valid_date（例2023-11-11）に該当するマシンのデータがなかった場合
                        slot_spec_data_list.append("-")

                slot_row = rows + slot_spec_data_list
                f.write(",".join(slot_row) + "\n")


    def _fetch_from_file(self, path):
        with open(path, mode="r", encoding="utf-8") as f:
            rows = [row.rstrip() for row in f.readlines() if row.split(",")[1] != "閉鎖"][1:]
        return rows


    def _print_about(self):
        print("スロットアナライザー")
        print(f"ver {self.version}")


def main():
    analyzer = Analyzer()
    rows = analyzer.collect_datas()
    data_dict = analyzer.get_get_value_ratio_percent_at_title(rows=rows)
    # analyzer.to_csv(data_dict=data_dict)
    # TODO 機種毎と台番号毎で切り替えられるように
    analyzer.to_csv_summary(data_dict=data_dict)

if __name__ == '__main__':
    main()