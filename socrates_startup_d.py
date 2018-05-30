import os
import utils
utils.eprint(os.path.dirname(os.path.realpath(__file__)))
os.chdir(os.path.dirname(os.path.realpath(__file__)))
import imp
socrates_ancientc = imp.load_dynamic("socrates_ancientc", "socrates_ancientd.pyd")
socrates_ancientc.SocratesGame().run()