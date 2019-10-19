from .Preprocessor import Preprocessor
from .Interpreter import Interpreter
from .Memory import Memory
from .Registers import Registers
from .static import *


class Simulator(Interpreter):
    shell_magic = {
        "%help": lambda: print(
            """
        %help      : Print help message
        %t/%a/%r   : print all the datas in t/s/all registers
        %t0        : print the datas in t0 register
        %t0 = 6    : set the datas in t0 to 6
        %about     : See more information about this project
        %q/%exit   : exit this shell
        """
        ),
        "%t": lambda: Registers.print("t"),
        "%a": lambda: Registers.print("a"),
        "%q": exit,
        "%about": lambda: print("""
        ______                                       
        |  ___|                                      
        | |_ ___ _ __   __ _ _   _  ___  _ __   __ _ 
        |  _/ _ \ '_ \ / _` | | | |/ _ \| '_ \ / _` |
        | ||  __/ | | | (_| | |_| | (_) | | | | (_| |
        \_| \___|_| |_|\__, |\__, |\___/|_| |_|\__, |
                        __/ | __/ |             __/ |
                       |___/ |___/             |___/ \n\n
        Authored by CQU-AI: Loopyme, Sean, Charles\n
        See more information at https://github.com/CQU-AI/pymips/"""),
        "%exit": exit,
    }

    def __init__(self):
        raise SyntaxError("Simulator can not be instantiate. Please use static method.")

    @classmethod
    def run_file(cls, path):
        with open(path, "r") as f:
            insts = f.read()
        cls.hist_inst, cls.label = Preprocessor.prep(insts, return_label=True)
        while cls.curr_inst < len(cls.hist_inst):
            cls.run_line(cls.hist_inst[cls.curr_inst], False)

    @classmethod
    def run_shell(cls):
        print("Fengyong mips shell")
        print('Type "%help" for more information.')
        while True:
            inst = input(">>> ")
            if len(inst.replace(" ", "")) < 1:
                pass
            elif "%" not in inst:
                try:
                    cls.run_line(inst)
                except Exception as e:
                    print("[Fail] {}".format(e))
            else:
                inst = inst.replace(" ", "")
                if inst in cls.shell_magic.keys():  # magic
                    cls.shell_magic[inst]()
                elif "$" + inst[1:] in reg_to_index.keys():  # get reg
                    print(
                        "  {} = {}".format(inst[1:], Registers.reg_get("$" + inst[1:]))
                    )
                elif "=" in inst:  # set reg
                    if "$" + inst.split("=")[0][1:] not in reg_to_index.keys():
                        print(
                            '[Fail] Unknown reg:"{}"'.format("$" + inst.split("=")[0])
                        )
                    else:
                        try:
                            Registers.reg_set(
                                "$" + inst.split("=")[0][1:],
                                RegData(inst.split("=")[1]),
                            )
                        except Exception as e:
                            print(
                                "[Fail] Can set {} to {}:{}".format(
                                    "$" + inst.split("=")[0][1:], inst.split("=")[1], e
                                )
                            )
                else:
                    print("[Fail] Unknown command:{}".format(inst))
