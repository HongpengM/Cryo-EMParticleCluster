import os
import os.path
import re
import copy
import pickle

# Meaning of each item in read

# loop_
# _rlnVoltage #1 --> voltage
# _rlnDefocusU #2 --> defocusU
# _rlnDefocusV #3 --> defocusV
# _rlnDefocusAngle #4 --> defocusAngel
# _rlnSphericalAberration #5 --> sphericalAbrr
# _rlnDetectorPixelSize #6 --> detectPixelSize
# _rlnCtfFigureOfMerit #7 --> ctfFigOfMerit
# _rlnMagnification #8 --> magnification
# _rlnAmplitudeContrast #9 --> amplitudeContrast
# _rlnImageName #10 --> imageName
# _rlnCoordinateX #11 --> coordX
# _rlnCoordinateY #12 --> coordY
# _rlnNormCorrection #13 --> normCorrection
# _rlnMicrographName #14 --> micrographName
# _rlnGroupNumber #15 --> groupName
# _rlnOriginX #16 --> originX
# _rlnOriginY #17 --> originY
# _rlnAngleRot #18 --> angleRot
# _rlnAngleTilt #19 --> angleTilt
# _rlnAnglePsi #20 --> anglePsi
# _rlnAutopickFigureOfMerit #21 --> autopickFigOfMerit
# _rlnClassNumber #22 --> classNumber
# _rlnLogLikeliContribution #23 --> logLikeliContribution
# _rlnNrOfSignificantSamples #24 --> NrOfSigSample
# _rlnMaxValueProbDistribution #25 --> maxValProbDistr
# _rlnRandomSubset #26 --> randomSubset

# **** An example read
# 300.000000 22133.380859 21392.150391     1.830000     2.000000    10.000000
# 0.312230 41132.000000     0.100000
# 000034@Particles/Micrographs/stack_0021_2x_SumCorr_particles_bin2.mrcs
# 3295.000000  1372.000000     0.414558 Micrographs/stack_0021_2x_SumCorr.mrc
# 19    -4.013087    -0.761087    43.293127    84.846311   160.421794
# 0.488655            1 60084.350428           23     0.083737
# 1

pattern = re.compile(r'(.*?)')
patternRemove = re.compile(r'_|.*_$')
STAR_PATH = './'
# output the extract StarRead list
OUTPUT_PATH = './'
starname = 'run1_data.star'
_keylist = ['voltage', 'defocusU', 'defocusV', 'defocusAngle', 'sphericalAbrr', 'detectPixelSize',
            'ctfFigOfMerit', 'magnification', 'amplitudeContrast', 'imageName', 'coordX', 'coordY',
            'normCorrection', 'micrographName', 'groupNumber', 'originX', 'originY', 'angleRot',
            'angleTilt', 'anglePsi', 'autopickFigOfMerit', 'classNumber', 'logLikeliContribution',
            'NrOfSigSample', 'maxValProbDistr', 'randomSubset']
# input a read and extract to list


def getReadList(read):
    return re.split(r' *', read)


# input a read string or list and return a dictionary
# of which keys are parameter name


def getReadInfo(input):
    if not (type(input) is list):
        input = getReadList(input)
    readInfo = {}
    readInfo['voltage'] = float(input[0])
    readInfo['defocusU'] = float(input[1])
    readInfo['defocusV'] = float(input[2])
    readInfo['defocusAngle'] = float(input[3])
    readInfo['sphericalAbrr'] = float(input[4])
    readInfo['detectPixelSize'] = float(input[5])
    readInfo['ctfFigOfMerit'] = float(input[6])
    readInfo['magnification'] = float(input[7])
    readInfo['amplitudeContrast'] = float(input[8])
    readInfo['imageName'] = str(input[9])
    readInfo['coordX'] = float(input[10])
    readInfo['coordY'] = float(input[11])
    readInfo['normCorrection'] = float(input[12])
    readInfo['micrographName'] = str(input[13])
    readInfo['groupNumber'] = int(input[14])
    readInfo['originX'] = float(input[15])
    readInfo['originY'] = float(input[16])
    readInfo['angleRot'] = float(input[17])
    readInfo['angleTilt'] = float(input[18])
    readInfo['anglePsi'] = float(input[19])
    readInfo['autopickFigOfMerit'] = float(input[20])
    readInfo['classNumber'] = float(input[21])
    readInfo['logLikeliContribution'] = float(input[22])
    readInfo['NrOfSigSample'] = int(input[23])
    readInfo['maxValProbDistr'] = float(input[24])
    readInfo['randomSubset'] = int(input[25])
    return readInfo


class StarRead:
    ''' This Class represent a read in star file, and the parameters can be fecth using feature string'''
    dictInfo = {}
    listInfo = {}

    def __init__(self, input):
        if type(input) is list or str:
            self.dictInfo = getReadInfo(input)
            self.listInfo = [self.dictInfo[k] for k in _keylist]
        elif type(input) is dict:
            self.dictInfo = copy.copy(input)
            self.listInfo = [self.dictInfo[k] for k in _keylist]
        else:
            raise Exception('input value type not allowed')

    def __repr__(self):
        _repr = ''
        for k, v in self.dictInfo.items():
            _repr += str(k) + ':' + str(v) + '\n'
        return _repr

    def getInfo(self):
        return self.dictInfo

    def getList(self):
        return [(k, self.dictInfo[k]) for k in _keylist]

    def getFeatureName(self, feature):
        if type(feature) is int:
            return _keylist[feature]
        else:
            raise Exception(
                'Feature name type error, please check the query again')

    def getFeature(self, feature=None):
        if type(feature) is str and (len(self.dictInfo) != 0):
            return self.dictInfo[feature]
        elif type(feature) is int:
            return self.listInfo[feature]
        else:
            raise Exception(
                'The class has no valid dict or no valid input')


def getStarRead(fn):
    try:
        fh = open(fn + '.pkl', 'rb')
        starReads = pickle.load(fh)
        fh.close()
    except IOError:
        starReads = []
        with open(STAR_PATH + fn, 'r') as fr:
            counter = 0
            rawRead = fr.readline().strip()
            while len(rawRead) > 0 or counter < 10:
                matchRemove = patternRemove.match(rawRead)
                if (not matchRemove) and len(rawRead) > 0:
                    starReads.append(StarRead(rawRead))
                    # print rawRead.split('\t')
                rawRead = fr.readline().strip()
                counter += 1
        fh = open(fn + '.pkl', 'wb')
        pickle.dump(starReads, fh)
        fh.close()
    return starReads


def test():
    print getStarRead(starname)[0]


def main():
    test()

if __name__ == '__main__':
    main()
