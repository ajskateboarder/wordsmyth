"""A single module variable"""
import warnings

from src.algo.deepmoji import Emojize
from src.algo.roberta import Roberta


warnings.filterwarnings("ignore")


emoji = Emojize()
roberta = Roberta()
