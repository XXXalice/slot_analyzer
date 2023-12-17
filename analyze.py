from tqdm import tqdm
import os

class Analyzer:
    def __init__(self):
        self.version = "0.1.0"
        self.dir_name = "files"

        self._print_about()

        rows = self._collect_datas()



    def _collect_datas(self):
        print("csvファイルをロードします")
        files = os.listdir(f"./{self.dir_name}")
        files = [file for file in files if file[-3:] == "csv"]
        rows = []
        for fname in tqdm(files):
            path = f"./{self.dir_name}/{fname}"
            rows.append(self._fetch_from_file(path))


    def _fetch_from_file(self, path):
        with open(path, mode="r") as f:
            rows = [row.rstrip() for row in f.readlines()][1:]
        return rows

    def _print_about(self):
        print("スロットアナライザー")
        print(f"ver {self.version}")


def main():
    analyzer = Analyzer()



if __name__ == '__main__':
    main()