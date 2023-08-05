
from hvc.datasets.beijing_air_quality import BeijingAirQuality
from hvc.datasets.isolet import ISOLET
from hvc.datasets.european_languages import EuropeanLanguages
from hvc.datasets.ucihar import UCIHAR
from hvc.datasets.airfoil_self_noise import AirfoilSelfNoise
from hvc.datasets.emg_hand_gestures import EMGHandGestures
from hvc.datasets.pamap import PAMAP
from hvc.datasets.ccpp import CyclePowerPlant
from hvc.datasets.dataset import CollectionDataset
from hvc.datasets.dataset import DatasetFourFold
from hvc.datasets.dataset import DatasetTrainTest
from hvc.datasets.dataset import UCIClassificationBenchmark
from hvc.datasets.abalone import Abalone
from hvc.datasets.adult import Adult
from hvc.datasets.acute_inflammation import AcuteInflammation
from hvc.datasets.acute_nephritis import AcuteNephritis
from hvc.datasets.annealing import Annealing
from hvc.datasets.arrhythmia import Arrhythmia
from hvc.datasets.audiology_std import AudiologyStd
from hvc.datasets.balance_scale import BalanceScale
from hvc.datasets.balloons import Balloons
from hvc.datasets.bank import Bank
from hvc.datasets.blood import Blood
from hvc.datasets.breast_cancer import BreastCancer
from hvc.datasets.breast_cancer_wisc import BreastCancerWisc
from hvc.datasets.breast_cancer_wisc_diag import BreastCancerWiscDiag
from hvc.datasets.breast_cancer_wisc_prog import BreastCancerWiscProg
from hvc.datasets.breast_tissue import BreastTissue
from hvc.datasets.car import Car
from hvc.datasets.cardiotocography_3clases import Cardiotocography3Clases
from hvc.datasets.cardiotocography_10clases import Cardiotocography10Clases
from hvc.datasets.chess_krvk import ChessKrvk
from hvc.datasets.chess_krvkp import ChessKrvkp
from hvc.datasets.congressional_voting import CongressionalVoting
from hvc.datasets.conn_bench_sonar_mines_rocks import ConnBenchSonarMinesRocks
from hvc.datasets.conn_bench_vowel_deterding import ConnBenchVowelDeterding
from hvc.datasets.connect_4 import Connect4
from hvc.datasets.contrac import Contrac
from hvc.datasets.credit_approval import CreditApproval
from hvc.datasets.cylinder_bands import CylinderBands
from hvc.datasets.dermatology import Dermatology
from hvc.datasets.echocardiogram import Echocardiogram
from hvc.datasets.ecoli import Ecoli
from hvc.datasets.energy_y1 import EnergyY1
from hvc.datasets.energy_y2 import EnergyY2
from hvc.datasets.fertility import Fertility
from hvc.datasets.flags import Flags
from hvc.datasets.glass import Glass
from hvc.datasets.haberman_survival import HabermanSurvival
from hvc.datasets.hayes_roth import HayesRoth
from hvc.datasets.heart_cleveland import HeartCleveland
from hvc.datasets.heart_hungarian import HeartHungarian
from hvc.datasets.heart_switzerland import HeartSwitzerland
from hvc.datasets.heart_va import HeartVa
from hvc.datasets.hepatitis import Hepatitis
from hvc.datasets.hill_valley import HillValley
from hvc.datasets.horse_colic import HorseColic
from hvc.datasets.ilpd_indian_liver import IlpdIndianLiver
from hvc.datasets.image_segmentation import ImageSegmentation
from hvc.datasets.ionosphere import Ionosphere
from hvc.datasets.iris import Iris
from hvc.datasets.led_display import LedDisplay
from hvc.datasets.lenses import Lenses
from hvc.datasets.letter import Letter
from hvc.datasets.libras import Libras
from hvc.datasets.low_res_spect import LowResSpect
from hvc.datasets.lung_cancer import LungCancer
from hvc.datasets.lymphography import Lymphography
from hvc.datasets.magic import Magic
from hvc.datasets.mammographic import Mammographic
from hvc.datasets.miniboone import Miniboone
from hvc.datasets.molec_biol_promoter import MolecBiolPromoter
from hvc.datasets.molec_biol_splice import MolecBiolSplice
from hvc.datasets.monks_1 import Monks1
from hvc.datasets.monks_2 import Monks2
from hvc.datasets.monks_3 import Monks3
from hvc.datasets.mushroom import Mushroom
from hvc.datasets.musk_1 import Musk1
from hvc.datasets.musk_2 import Musk2
from hvc.datasets.nursery import Nursery
from hvc.datasets.oocytes_merluccius_nucleus_4d import OocytesMerlucciusNucleus4d
from hvc.datasets.oocytes_merluccius_states_2f import OocytesMerlucciusStates2f
from hvc.datasets.oocytes_trisopterus_nucleus_2f import OocytesTrisopterusNucleus2f
from hvc.datasets.oocytes_trisopterus_states_5b import OocytesTrisopterusStates5b
from hvc.datasets.optical import Optical
from hvc.datasets.ozone import Ozone
from hvc.datasets.page_blocks import PageBlocks
from hvc.datasets.parkinsons import Parkinsons
from hvc.datasets.pendigits import Pendigits
from hvc.datasets.pima import Pima
from hvc.datasets.pittsburg_bridges_material import PittsburgBridgesMaterial
from hvc.datasets.pittsburg_bridges_rel_l import PittsburgBridgesRelL
from hvc.datasets.pittsburg_bridges_span import PittsburgBridgesSpan
from hvc.datasets.pittsburg_bridges_t_or_d import PittsburgBridgesTOrD
from hvc.datasets.pittsburg_bridges_type import PittsburgBridgesType
from hvc.datasets.planning import Planning
from hvc.datasets.plant_margin import PlantMargin
from hvc.datasets.plant_shape import PlantShape
from hvc.datasets.plant_texture import PlantTexture
from hvc.datasets.post_operative import PostOperative
from hvc.datasets.primary_tumor import PrimaryTumor
from hvc.datasets.ringnorm import Ringnorm
from hvc.datasets.seeds import Seeds
from hvc.datasets.semeion import Semeion
from hvc.datasets.soybean import Soybean
from hvc.datasets.spambase import Spambase
from hvc.datasets.spect import Spect
from hvc.datasets.spectf import Spectf
from hvc.datasets.statlog_australian_credit import StatlogAustralianCredit
from hvc.datasets.statlog_german_credit import StatlogGermanCredit
from hvc.datasets.statlog_heart import StatlogHeart
from hvc.datasets.statlog_image import StatlogImage
from hvc.datasets.statlog_landsat import StatlogLandsat
from hvc.datasets.statlog_shuttle import StatlogShuttle
from hvc.datasets.statlog_vehicle import StatlogVehicle
from hvc.datasets.steel_plates import SteelPlates
from hvc.datasets.synthetic_control import SyntheticControl
from hvc.datasets.teaching import Teaching
from hvc.datasets.thyroid import Thyroid
from hvc.datasets.tic_tac_toe import TicTacToe
from hvc.datasets.titanic import Titanic
from hvc.datasets.trains import Trains
from hvc.datasets.twonorm import Twonorm
from hvc.datasets.vertebral_column_2clases import VertebralColumn2Clases
from hvc.datasets.vertebral_column_3clases import VertebralColumn3Clases
from hvc.datasets.wall_following import WallFollowing
from hvc.datasets.waveform import Waveform
from hvc.datasets.waveform_noise import WaveformNoise
from hvc.datasets.wine import Wine
from hvc.datasets.wine_quality_red import WineQualityRed
from hvc.datasets.wine_quality_white import WineQualityWhite
from hvc.datasets.yeast import Yeast
from hvc.datasets.zoo import Zoo

__all__ = [
    "BeijingAirQuality",
    "ISOLET",
    "EuropeanLanguages",
    "UCIHAR",
    "AirfoilSelfNoise",
    "EMGHandGestures",
    "PAMAP",
    "CyclePowerPlant",
    "CollectionDataset",
    "DatasetFourFold",
    "DatasetTrainTest",
    "UCIClassificationBenchmark",
    "Abalone",
    "Adult",
    "AcuteInflammation",
    "AcuteNephritis",
    "Annealing",
    "Arrhythmia",
    "AudiologyStd",
    "BalanceScale",
    "Balloons",
    "Bank",
    "Blood",
    "BreastCancer",
    "BreastCancerWisc",
    "BreastCancerWiscDiag",
    "BreastCancerWiscProg",
    "BreastTissue",
    "Car",
    "Cardiotocography3Clases",
    "Cardiotocography10Clases",
    "ChessKrvk",
    "ChessKrvkp",
    "CongressionalVoting",
    "ConnBenchSonarMinesRocks",
    "ConnBenchVowelDeterding",
    "Connect4",
    "Contrac",
    "CreditApproval",
    "CylinderBands",
    "Dermatology",
    "Echocardiogram",
    "Ecoli",
    "EnergyY1",
    "EnergyY2",
    "Fertility",
    "Flags",
    "Glass",
    "HabermanSurvival",
    "HayesRoth",
    "HeartCleveland",
    "HeartHungarian",
    "HeartSwitzerland",
    "HeartVa",
    "Hepatitis",
    "HillValley",
    "HorseColic",
    "IlpdIndianLiver",
    "ImageSegmentation",
    "Ionosphere",
    "Iris",
    "LedDisplay",
    "Lenses",
    "Letter",
    "Libras",
    "LowResSpect",
    "LungCancer",
    "Lymphography",
    "Magic",
    "Mammographic",
    "Miniboone",
    "MolecBiolPromoter",
    "MolecBiolSplice",
    "Monks1",
    "Monks2",
    "Monks3",
    "Mushroom",
    "Musk1",
    "Musk2",
    "Nursery",
    "OocytesMerlucciusNucleus4d",
    "OocytesMerlucciusStates2f",
    "OocytesTrisopterusNucleus2f",
    "OocytesTrisopterusStates5b",
    "Optical",
    "Ozone",
    "PageBlocks",
    "Parkinsons",
    "Pendigits",
    "Pima",
    "PittsburgBridgesMaterial",
    "PittsburgBridgesRelL",
    "PittsburgBridgesSpan",
    "PittsburgBridgesTOrD",
    "PittsburgBridgesType",
    "Planning",
    "PlantMargin",
    "PlantShape",
    "PlantTexture",
    "PostOperative",
    "PrimaryTumor",
    "Ringnorm",
    "Seeds",
    "Semeion",
    "Soybean",
    "Spambase",
    "Spect",
    "Spectf",
    "StatlogAustralianCredit",
    "StatlogGermanCredit",
    "StatlogHeart",
    "StatlogImage",
    "StatlogLandsat",
    "StatlogShuttle",
    "StatlogVehicle",
    "SteelPlates",
    "SyntheticControl",
    "Teaching",
    "Thyroid",
    "TicTacToe",
    "Titanic",
    "Trains",
    "Twonorm",
    "VertebralColumn2Clases",
    "VertebralColumn3Clases",
    "WallFollowing",
    "Waveform",
    "WaveformNoise",
    "Wine",
    "WineQualityRed",
    "WineQualityWhite",
    "Yeast",
    "Zoo",
]
