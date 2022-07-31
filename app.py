from deepmoj import Emojize
import warnings

warnings.filterwarnings('ignore')

emoji = Emojize()
print(emoji.predict('So interesting!'))