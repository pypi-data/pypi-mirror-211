import numpy as np
from PAMI.faultTolerantFrequentPattern.maximal import abstract as _ab

class maxFTP(_ab._faultTolerantFrequentPatterns):
    """
        FT-Apriori is one of the fundamental algorithm to discover fault tolerant frequent patterns in a transactional database.
        This program employs apriori property (or downward closure property) to  reduce the search space effectively.

        Reference:
        ----------
            Pei, Jian & Tung, Anthony & Han, Jiawei. (2001). Fault-Tolerant Frequent Pattern Mining: Problems and Challenges.


        Attributes:
        ----------
            iFile : str
                Input file name or path of the input file
            oFile : str
                Name of the output file or the path of output file
            minSup: float or int or str
                The user can specify minSup either in count or proportion of database size.
                If the program detects the data type of minSup is integer, then it treats minSup is expressed in count.
                Otherwise, it will be treated as float.
                Example: minSup=10 will be treated as integer, while minSup=10.0 will be treated as float
            sep : str
                This variable is used to distinguish items from one another in a transaction. The default seperator is tab space or \t.
                    However, the users can override their default separator.
            startTime:float
                To record the start time of the mining process
            endTime:float
                To record the completion time of the mining process
            finalPatterns: dict
                Storing the complete set of patterns in a dictionary variable
            memoryUSS : float
                To store the total amount of USS memory consumed by the program
            memoryRSS : float
                To store the total amount of RSS memory consumed by the program
            Database : list
                To store the transactions of a database in list

        Methods:
        -------
            startMine()
                Mining process will start from here
            getPatterns()
                Complete set of patterns will be retrieved with this function
            save(oFile)
                Complete set of frequent patterns will be loaded in to a output file
            getPatternsAsDataFrame()
                Complete set of frequent patterns will be loaded in to a dataframe
            getMemoryUSS()
                Total amount of USS memory consumed by the mining process will be retrieved from this function
            getMemoryRSS()
                Total amount of RSS memory consumed by the mining process will be retrieved from this function
            getRuntime()
                Total amount of runtime taken by the mining process will be retrieved from this function


        Executing the code on terminal:
        -------------------------------

            Format:
            ------
                python3 FTApriori.py <inputFile> <outputFile> <minSup> <itemSup> <minLength> <faultTolerance>

            Examples:
            ---------
                python3 FTApriori.py sampleDB.txt patterns.txt 10.0 3.0 3 1  (minSup will be considered in times of minSup and count of database transactions)

                python3 FTApriori.py sampleDB.txt patterns.txt 10  3 2 1    (minSup will be considered in support count or frequency)


        Sample run of the importing code:
        ---------------------------------

            import PAMI.faultTolerantFrequentPattern.maximal.maxFTP as alg

            obj = alg.maxFTP(iFile, minSup, itemSup, minLength, faultTolerance)

            obj.startMine()

            faultTolerantFrequentPatterns = obj.getPatterns()

            print("Total number of Fault Tolerant Frequent Patterns:", len(faultTolerantFrequentPatterns))

            obj.save(oFile)

            Df = obj.getPatternInDataFrame()

            print("Total Memory in USS:", obj.getMemoryUSS())

            print("Total Memory in RSS", obj.getMemoryRSS())

            print("Total ExecutionTime in seconds:", obj.getRuntime())

        Credits:
        --------
            The complete program was written by P.Likhitha  under the supervision of Professor Rage Uday Kiran.

    """

    _minSup = float()
    _itemSup = float()
    _minLength = int()
    _faultTolerance = int()
    _startTime = float()
    _endTime = float()
    _finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _sep = " "
    _memoryUSS = float()
    _memoryRSS = float()
    _Database = []
    _mapSupport = {}

    def _creatingItemSets(self):
        """
            Storing the complete transactions of the database/input file in a database variable


        """
        self._Database = []
        if isinstance(self._iFile, _ab._pd.DataFrame):
            temp = []
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                temp = self._iFile['Transactions'].tolist()

            for k in temp:
                self._Database.append(set(k))
        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._sep)]
                    temp = [x for x in temp if x]
                    self._Database.append(set(temp))
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line.strip()
                            temp = [i.rstrip() for i in line.split(self._sep)]
                            temp = [x for x in temp if x]
                            self._Database.append(set(temp))
                except IOError:
                    print("File Not Found")
                    quit()

    def _convert(self, value):
        """
        To convert the user specified minSup value

        :param value: user specified minSup value

        :return: converted type
        """
        if type(value) is int:
            value = int(value)
        if type(value) is float:
            value = (len(self._Database) * value)
        if type(value) is str:
            if '.' in value:
                value = float(value)
                value = (len(self._Database) * value)
            else:
                value = int(value)
        return value

    def _oneLengthItems(self):
        self._mapSupport = {}
        self._bits = {}
        for i in self._Database:
            for j in i:
                if j not in self._mapSupport:
                    self._mapSupport[j] = 1
                else:
                    self._mapSupport[j] += 1
        self._mapSupport = {k: v for k, v in self._mapSupport.items() if v >= self._minSup}
        genList = [k for k, v in sorted(self._mapSupport.items(), key=lambda x: x[1], reverse=True)]
        for i in genList:
            for j in self._Database:
                if i in j:
                    if i not in self._bits:
                        self._bits[i] = np.array(1)
                    else:
                        self._bits[i].append(1)
                else:
                    if i not in self._bits:
                        self._bits[i] = np.array(0)
                    else:
                        self._bits[i].append(0)
        print(self._bits)
        return genList

    def _checkMaximal(self, itemset):
        s = [0] * len(self._Database)
        for i in itemset:
            s = list(np.array(s) & np.array(self._bits[i]))
        print(s)



    def startMine(self):
        self._startTime =  _ab._time.time()
        self._creatingItemSets()
        self._minSup = self._convert(self._minSup)
        self._itemSup = self._convert(self._itemSup)
        self._faultTolerance = int(self._faultTolerance)
        sortedList = self._oneLengthItems()
        self._checkMaximal(sortedList)
        self._maxFTP(sortedList)
        self.__endTime = _ab._time.time()
        self.__memoryUSS = float()
        self.__memoryRSS = float()
        process = _ab._psutil.Process(_ab._os.getpid())
        self.__memoryUSS = process.memory_full_info().uss
        self.__memoryRSS = process.memory_info().rss

    def getMemoryUSS(self):
        """Total amount of USS memory consumed by the mining process will be retrieved from this function

        :return: returning USS memory consumed by the mining process

        :rtype: float
        """

        return self.__memoryUSS

    def getMemoryRSS(self):
        """Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process

        :rtype: float
        """

        return self.__memoryRSS

    def getRuntime(self):
        """Calculating the total amount of runtime taken by the mining process


        :return: returning total amount of runtime taken by the mining process

        :rtype: float
        """

        return self._endTime - self._startTime

    def getPatternsAsDataFrame(self):
        """Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe

        :rtype: pd.DataFrame
        """

        dataframe = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a.replace('\t', ' '), b])
            dataframe = _ab._pd.DataFrame(data, columns=['Patterns', 'Support'])
        return dataframe

    def save(self, outFile):
        """Complete set of frequent patterns will be loaded in to a output file

        :param outFile: name of the output file

        :type outFile: file
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            s1 = x.strip() + ":" + str(y)
            writer.write("%s \n" % s1)

    def getPatterns(self):
        """ Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns

        :rtype: dict
        """
        return self._finalPatterns

    def printResults(self):
        print("Total number of Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:", self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 7 or len(_ab._sys.argv) == 8:
        if len(_ab._sys.argv) == 8:
            _ap = maxFTP(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[5], _ab._sys.argv[6], _ab._sys.argv[7])
        if len(_ab._sys.argv) == 7:
            _ap = maxFTP(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], _ab._sys.argv[6], _ab._sys.argv[6])
        _ap.startMine()
        print("Total number of maximal Fault-Tolerant Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        _ap = maxFTP('sample.txt', 3, 2, 1, ' ')
        _ap.startMine()
        print("Total number of maximal Fault-Tolerant Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save('output.txt')
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
        print("Error! The number of input parameters do not match the total number of parameters provided")

