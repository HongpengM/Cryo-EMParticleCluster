import os
import os.path
import re
import copy


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
starname = 'run1_data.star'

# input a read and extract to list


def getReadList(read):
    return re.split(r' *', read)


# input a read string or list and return a dictionary
# of which keys are parameter name


def getReadInfo(input):
    if not (type(input) is list):
        input = getReadList(input)
    readInfo = {}
    readInfo['voltage'] = input[0]
    readInfo['defocusU'] = input[1]
    readInfo['defocusV'] = input[2]
    readInfo['defocusAngle'] = input[3]
    readInfo['sphericalAbrr'] = input[4]
    readInfo['detectPixelSize'] = input[5]
    readInfo['ctfFigOfMerit'] = input[6]
    readInfo['magnification'] = input[7]
    readInfo['amplitudeContrast'] = input[8]
    readInfo['imageName'] = input[9]
    readInfo['coordX'] = input[10]
    readInfo['coordY'] = input[11]
    readInfo['normCorrection'] = input[12]
    readInfo['micrographName'] = input[13]
    readInfo['groupNumber'] = input[14]
    readInfo['originX'] = input[15]
    readInfo['originY'] = input[16]
    readInfo['angleRot'] = input[17]
    readInfo['angleTilt'] = input[18]
    readInfo['anglePsi'] = input[19]
    readInfo['autopickFigOfMerit'] = input[20]
    readInfo['classNumber'] = input[21]
    readInfo['logLikeliContribution'] = input[22]
    readInfo['NrOfSigSample'] = input[23]
    readInfo['maxValProbDistr'] = input[24]
    readInfo['randomSubset'] = input[25]
    return readInfo


class StarRead:
    dictInfo = {}

    def __init__(self, input):
        if type(input) is list:
            if len(input) == 26:
                self.dictInfo = getReadInfo(input)
        elif type(input) is dict:
            self.dictInfo = copy.copy(input)
        else:
            raise ValueException('input value type not allowed')

    def __repr__(self):
        _repr = ''
        for k, v in self.dictInfo.items():
            _repr += str(k) + ':' + str(v) + '\n'
        return _repr

    def getInfo(self):
        return self.dictInfo

    def getList(self):
        return [(k, v) for k, v in self.dictInfo.items()]

    def getFeature(self, feature=None):
        if feature and (len(self.dictInfo) != 0):
            return self.dictInfo[feature]
        else:
            raise ValueException('The class has no valid dict or no valid input')


def test():
    with open(STAR_PATH + starname, 'r') as fr:
        for i in xrange(1, 40):
            rawRead = fr.readline().strip()
            matchRemove = patternRemove.match(rawRead)
            if (not matchRemove) and len(rawRead) > 0:
                print 'line-', i, ' ', rawRead
                print StarRead(getReadList(rawRead)).getFeature('voltage')
                print getReadInfo(rawRead)
                # print rawRead.split('\t')


def main():
    test()

if __name__ == '__main__':
    main()
