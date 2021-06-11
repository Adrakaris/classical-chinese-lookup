from tkinter import *
from typing import List
from csv import reader


# functions
def read_csv(filename: str) -> List[List[str]]:
    """
    Reads a csv file into a 2D array
    
    :param filename: file to read
    :return: csv entries
    """
    dictionary: List[List[str]] = []
    with open(filename) as fn:
        text = reader(fn)
        next(text)  # skip the header
        for ln in text:
            dictionary.append(ln)
    return dictionary


def binary_search(chinese: str, low: int, high: int, dictionary: List) -> int:
    """
    Binary search on the dictionary. Returns the index of the found item.
    
    :param chinese: The character to search for
    :param low: Call with 0
    :param high: Call with length of array
    :param dictionary: Array
    :return: The index of the character entry in the dictionary
    """
    if high >= low:
        mid = (high + low) // 2
        # print(f"high {high} low {low} mid {mid}")
        # print(dictionary[mid][0])
        
        if dictionary[mid][0] == chinese:
            return mid  # dictionary[mid]
        elif dictionary[mid][0] > chinese:
            return binary_search(chinese, low, mid-1, dictionary)
        else:
            return binary_search(chinese, mid+1, high, dictionary)
    else:
        return -1  # ["[" + chinese + "]" for _ in range(len(dictionary[0]))]  # not found, yields a [x]
    

def binary_interface(chinese: str) -> List[str]:
    """
    Chinese is not a perfect one-to-one language, and nor is this dictionary. Thus, we have to not only search for
    a character, but also search around it for adjacent entries with the same character. For example, 長 has two entries
    in Chang and Zhang.
    
    Since the entries are sorted by character unicode order, all characters which are the same are in a contiguous
    block.
    
    Mutliple entries are concactenated together using "/" for ease of display later
    
    :param chinese: Character to search for
    :return: Entry(s) for that character
    """
    index: int = binary_search(chinese, 0, len(DICT)-1, DICT)
    
    if index == -1:  # if character not found
        return ["[" + chinese + "]" for _ in range(len(DICT[0]))]
    
    # else we have to do a bit of searching
    yuan: List[List[str]] = [DICT[index]]
    # search up and down
    offset = 1
    while 0 <= index + offset < len(DICT) and \
            (DICT[index + offset][0] == yuan[0][0] or DICT[index - offset][0] == yuan[0][0]):
        if DICT[index + offset][0] == yuan[0][0]:
            yuan.append(DICT[index + offset])
        if DICT[index - offset][0] == yuan[0][0]:
            yuan.append(DICT[index - offset])
        offset += 1
        
    out: List[str] = []
    for column in zip(*yuan):
        out.append("/".join(column))
    out[SIMP] = f"[({out[SIMP]})]" if len(out[SIMP]) > 1 else f"[{out[SIMP]}]"
    return out


DICT = read_csv("dictionary.csv")
DICT.sort(key=lambda v: v[0])  # sort by traditional chinese
# table keys
TRAD = 0
SIMP = 1
PY = 2
MC = 3
OC = 5
DEF = 6


class Window:
    def __init__(self, base: Tk):
        self.base = base
        base.title("Classical Lookup")

        self.title = Label(base, text="古文字典", font=("SimSun", 30))
        self.title.grid(row=0, column=0, columnspan=2, sticky=E + W)

        self.l_search = Label(base, text="Enter traditional chinese:", font=("Georgia", 12))
        self.l_search.grid(row=1, column=0, columnspan=2, sticky=W)

        self.search_field = Text(base, width=72, height=3, font=("SimSun", 14))
        self.search_field.grid(row=2, column=0, columnspan=2, sticky=E + W)

        self._temp1 = Label(base)
        self._temp1.grid(row=3, column=0, columnspan=2)

        self.activate = Button(base, text="Search", font=("Georgia", 14), command=self.search_interface)
        self.activate.grid(row=4, column=0, sticky=W+E)
        self.clear = Button(base, text="Clear", font=("Georgia", 14), command=self.clear_interface)
        self.clear.grid(row=4, column=1, sticky=W+E)

        self._temp2 = Label(base)
        self._temp2.grid(row=5, column=0, columnspan=2)
        
        # results
        self.l_py = Label(base, text="Modern Pinyin", font=("Georgia", 12))
        self.l_py.grid(row=6, column=0, columnspan=2, sticky=W)

        self.py = Text(base, width=72, height=6, font=("SimSun", 14))
        self.py.grid(row=7, column=0, columnspan=2, sticky=E + W)

        self.l_anc = Label(base, text="Middle Chinese", font=("Georgia", 12))
        self.l_anc.grid(row=8, column=0, columnspan=2, sticky=W)

        self.anc = Text(base, width=72, height=6, font=("SimSun", 14))
        self.anc.grid(row=9, column=0, columnspan=2, sticky=E + W)

        self.l_anoc = Label(base, text="Old Chinese", font=("Georgia", 12))
        self.l_anoc.grid(row=10, column=0, columnspan=2, sticky=W)

        self.anoc = Text(base, width=72, height=6, font=("SimSun", 14))
        self.anoc.grid(row=11, column=0, columnspan=2, sticky=E + W)

        self.l_sim = Label(base, text="Simplified", font=("Georgia", 12))
        self.l_sim.grid(row=12, column=0, columnspan=2, sticky=W)

        self.sim = Text(base, width=72, height=3, font=("SimSun", 14))
        self.sim.grid(row=13, column=0, columnspan=2, sticky=E + W)

        self.l_def = Label(base, text="Definitions (If you put too many characters it will overflow a bit)",
                           font=("Georgia", 12))
        self.l_def.grid(row=14, column=0, columnspan=2, sticky=W)

        self.defs = Text(base, width=72, height=8, font=("SimSun", 14))
        self.defs.grid(row=15, column=0, columnspan=2, sticky=E + W)

    def search_interface(self):
        self.clear_outputs()
        query_list = self.search_field.get("1.0", END)[:-1]  # need to do query individually
        # print(repr(query_list))
        for char in query_list:
            if char == "\n":
                r = ["\r\n" for _ in range(12)]
                r[0] = ""
                r[DEF] = "\r"
                r[SIMP] = "[\n]"
                self.insert_intos(r)
            else:
                self.insert_intos(binary_interface(char))

    def clear_interface(self):
        self.search_field.delete("1.0", END)
        self.clear_outputs()
    
    def clear_outputs(self):
        self.py.delete("1.0", END)
        self.anc.delete("1.0", END)
        self.anoc.delete("1.0", END)
        self.sim.delete("1.0", END)
        self.defs.delete("1.0", END)
        
    def insert_intos(self, row):
        self.py.insert(INSERT, row[PY]+" ")
        self.anc.insert(INSERT, row[MC]+" ")
        self.anoc.insert(INSERT, row[OC]+"; ")
        self.sim.insert(INSERT, row[SIMP][1:-1])
        self.defs.insert(INSERT, f"{row[0]}: {row[DEF]}\n")
        

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = Tk()
    gui = Window(root)
    root.mainloop()
