import os
import utils
utils.eprint(os.path.dirname(os.path.realpath(__file__)))
os.chdir(os.path.dirname(os.path.realpath(__file__)))
import socrates_ancientc
socrates_ancientc.SocratesGame().run()