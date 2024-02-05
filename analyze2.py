import pprint

from tqdm import tqdm
import os
import itertools

class Analyzer:
    def __init__(self, mode=0, dir_path="files"):
        self.version = "0.1.2"
        self.dir_name = dir_path
        self.mode = mode
        self._print_about()


    # CSVからデータを引っこ抜いてくる
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

    # 台基準で表を作成
    def calcurate_rows_at_machine(self, rows):
        print("生成するファイルに載せる値を算出します")
        result_rows = []
        # rowをひとつづつ計算させて最終形にする
        for row in tqdm(rows):
            items = row.split(",")

            #左軸
            title = f"{items[2]}_({items[1]})"
            game_num = int(items[3])
            diff = int(items[4])
            bb = int(items[5])
            rb = int(items[6])
            if bb == 0 or rb == 0:
                continue

            bb_probability = round(game_num / bb, 1)
            rb_probability = round(game_num / rb, 1)
            total_probability = round(game_num / (bb + rb), 1)
            rate = round((game_num * 3 + diff) / (game_num * 3) * 100, 1)

            result_rows.append(
                ",".join([
                    str(title),
                    str(game_num),
                    str(diff),
                    str(bb),
                    str(rb),
                    str(bb_probability),
                    str(rb_probability),
                    str(total_probability),
                    str(rate),
                    str(game_num),
                    str(diff)
                ])
            )

        return result_rows

    # タイトル基準で表を作成
    def calcurate_rows(self, rows):
        print("生成するファイルに載せる値を算出します")
        slot_name_list = self._get_slot_name_list(rows=rows)
        # 全体の生成品
        result_rows = []
        for slot_name in tqdm(slot_name_list):
            game_num_at_slot = []
            diff_at_slot = []
            bb_at_slot = []
            rb_at_slot = []

            for row in rows:
                row_list = row.split(",")
                row_slot_name = row_list[1]
                row_game_num = row_list[3]
                row_diff = row_list[4]
                row_bb = row_list[5]
                row_rb = row_list[6]
                if row_bb == 0 or row_rb == 0:
                    continue

                if slot_name == row_slot_name:
                    game_num_at_slot.append(int(row_game_num))
                    diff_at_slot.append(int(row_diff))
                    bb_at_slot.append(int(row_bb))
                    rb_at_slot.append(int(row_rb))

            #G数平均
            game_num_result = round(sum(game_num_at_slot) / len(game_num_at_slot))
            #差枚平均
            diff_result = round(sum(diff_at_slot) / len(diff_at_slot))
            #BB平均
            bb_result = round(sum(bb_at_slot) / len(bb_at_slot))
            #RB平均
            rb_result = round(sum(rb_at_slot) / len(rb_at_slot))
            #BB確率
            bb_probability_result = 0 if bb_result == 0 else round(game_num_result / bb_result, 1)
            #RB確率
            rb_probability_result = 0 if rb_result == 0 else round(game_num_result / rb_result, 1)
            #合成確率
            total_probability_result = 0 if rb_result == 0 else round(game_num_result / (bb_result + rb_result), 1)
            #機械割
            rate_result = 0 if game_num_result == 0 else round((game_num_result * 3 + diff_result) / (game_num_result * 3) * 100, 1)
            #総G数
            total_game_num_result = sum(game_num_at_slot)
            #総差枚
            total_diff_result = sum(diff_at_slot)

            items = ",".join([
                str(slot_name),
                str(game_num_result),
                str(diff_result),
                str(bb_result),
                str(rb_result),
                str(bb_probability_result),
                str(rb_probability_result),
                str(total_probability_result),
                str(rate_result),
                str(total_game_num_result),
                str(total_diff_result)
            ])
            result_rows.append(items)

        return result_rows

    def to_csv(self, result_rows, path="./統計データ_総合版.csv"):
        header_row = [self._get_header_row()]
        csv_rows = header_row + result_rows

        with open(path, mode="w", encoding="utf-8") as f:
            for csv_row in csv_rows:
                f.write(csv_row + "\n")

        print("ファイル生成が正常に完了しました。")



    def _fetch_from_file(self, path):
        with open(path, mode="r", encoding="utf-8") as f:
            rows = [row.rstrip() for row in f.readlines() if row.split(",")[1] != "閉鎖"][1:]
        return rows


    # slot名のリスト返却
    def _get_slot_name_list(self, rows):
        slot_name_list = []
        # 2023-11-01,アイムジャグラーEX-TP,560,7374,-100,22,25,1/156.9,1/335.2,1/295.0
        for row in rows:
            slot_name = row.split(",")[1]
            if slot_name not in slot_name_list:
                slot_name_list.append(slot_name)
            else:
                pass

        return slot_name_list

    def _get_header_row(self):
        return ",".join([
            "機種名", "G数", "差枚", "BB", "RB", "BB確率", "RB確率", "合成確率", "機械割", "総G数", "総差枚"
        ])


    def _print_about(self):
        print("スロットアナライザー統合版")
        print(f"ver {self.version}")

    def operation(self):
        rows = self.collect_datas()
        if self.mode == 1:
            print("タイトルごとに集計します")
            result_rows = self.calcurate_rows(rows=rows)
        elif self.mode == 2:
            print("台番号ごとに集計します")
            result_rows = self.calcurate_rows_at_machine(rows=rows)
        else:
            print("モードを正しく指定してください")
            exit(0)
        self.to_csv(result_rows=result_rows)

if __name__ == '__main__':
    mode = int(input("起動したいモードを選択してください タイトルごと:1 台番号ごと:2  :"))
    analyzer = Analyzer(mode=mode)
    analyzer.operation()

