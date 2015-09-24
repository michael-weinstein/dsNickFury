#!/usr/bin/env python3

global currentVersion
currentVersion = "0.1"


#===================================Command line Argument Checking===========================================

class Args(object):
    
    def __init__(self):    
        import argparse #loads the required library for reading the commandline
        parser = argparse.ArgumentParser()
        parser.add_argument ("-m", "--mode", help = "Specify the directory where the input VCFs will be found and the output files will be written.")
        parser.add_argument ("-g", "--genome", help = "Specify the genome for searching or indexing.")
        parser.add_argument ("-d", "--inputdirectory", help = "Specify a directory of fasta files for indexing.")
        parser.add_argument ("-f", "--inputfile", help = "Specify a single input file for splitting")
        parser.add_argument ("--tempDir", help = "Temporary directory name for parallel jobs")
        parser.add_argument ("-p", "--parallelJobs", help = "Max number of parallel jobs at once.")
        parser.add_argument ("-9", "--clobber", help = "Do not ask before overwriting files.", action = 'store_true')
        parser.add_argument ("-w", "--workerID", help = "Worker process ID.  Users should not be setting this value.")
        parser.add_argument ("-s", "--sequence", help = "Sequence of interest.  Format: NNNNNNGUIDERNANNNNNN_PAM")
        parser.add_argument ("-t", "--mismatchTolerance", help = "Maximim number of mismatches permitted for a positive result.")
        parser.add_argument ("--verbose", help = "Run in verbose mode", action = 'store_true')
        parser.add_argument ("--mock" , help = "Print exec commands instead of running them.", action = 'store_true')
        parser.add_argument ("--chromosome")
        parser.add_argument ("--start")
        parser.add_argument ("--length")
        parser.add_argument ("--genomeID")
        args = parser.parse_args()  #puts the arguments into the args object
        
        if not args.mode:
            quit("No run mode was set on the commandline.")
        self.mode = args.mode
        if args.mode == 'worker':
            self.setWorkerArgs(args)
        elif args.mode == 'search':
            self.setSearchArgs(args)
        elif args.mode == 'index':
            self.setIndexArgs(args)
        elif args.mode == 'FASTAWorker':
            self.setFASTAWorkerArgs(args)
        else:
            quit('Invalid mode set on commandline.')

    def setWorkerArgs(self, args):
        pass
    
    def setSearchArgs(self, args):
        pass
    
    def setIndexArgs(self, args):
        import os
        self.mode = "index"
        if not args.sequence:
            quit("No search sequence specified.")
        if "_" in args.sequence:
            self.sequence = args.sequence.upper()
        else:
            quit("Invalid sequence passed. Please include an underscore between the guide and PAM sequences.")
        if not args.inputfile:
            quit("No FASTA specified for searching.")
        if os.path.isfile(args.inputfile):
            self.inputfile = args.inputfile
        else:
            quit("FASTA file: " + args.inputfile + " not found.")
        if not args.genome:
            quit("You must specify the name you want to identify this genome by.")
        self.genome = args.genome
        self.clobber = args.clobber
        self.mock = args.mock
        self.tempDir = args.tempDir
    
    def setFASTAWorkerArgs(self, args):
        import os
        self.mode = "FASTAWorker"
        self.chromosome = args.chromosome
        self.start = args.start
        self.length = args.length
        if "_" in args.sequence:
            self.sequence = args.sequence
        else:
            quit("Invalid sequence passed to worker. Please include an underscore between the guide and PAM sequences.")
        if os.path.isfile(args.inputfile):
            self.inputfile = args.inputfile
        else:
            quit("FASTA file: " + args.inputfile + " not found.")
        self.genome = args.genome
        self.tempDir = args.tempDir
        #if os.path.isdir(args.tempDir):
        #    self.tempDir = args.tempDir
        #else:
        #    quit("Unable to detect temporary directory: " + args.tempDir)

#=================================================Reverse Complement and other sequence manipulation.  Possibly move to its own module later?===========================================Complete==============================

class ReverseComplement(object):  #declares an object class.  We capitalize the first letter (unlike variables that should start with lowercase) to avoid potential collisions with variable names
    
    def __init__(self, sequence, reverse = True, case = 'original'):
        case = case.lower()
        if not case in ['upper','lower','original']:
            raise ValueError('Case option must be set to upper, lower, or original.')
        self.case = case
        if reverse:  #we defined an optional argument "reverse" to be true.  We did this because we assume people will often want the reverse complement.  They have to specify reverse = False if they don't.
            self.inputSeq = sequence[::-1]  #Neat trick in Python to reverse the order of an iterable (string, list, etc).  Indexing goes [inclusive start:non-inclusive end:step].  A step of -1 tells it to start from the end and step backwards 1 element at a time.  This seems to run slightly more efficiently than iterating in reverse.
        else: #if the user wants a non-reverse complement
            self.inputSeq = sequence  #we store the value without reversing.  The self.[name] means that this value will be variable that can be called from anywhere within this instance of the object AND from outside the object by calling [instance].[name].  A variable that is tied to a function like this one is called an attribute. 
        if self.case == 'upper':  #now that case is being handled by the dictionary itself, we just need to change the original sequence if necessary
            self.inputSeq = self.inputSeq.upper()  
        elif self.case == 'lower':
            self.inputSeq == self.inputSeq.lower()
        self.complementTable = self.createComplementTable()  #this is defining an attribute of the object (complementTable) by calling the createComplementTable method.  Of interest, since the table is just returned by the function, a program could call the table for its own use by calling [instance].createComplementTable()
        self.complementLists = self.createComplementLists()  #same as above, but this one gets back all non-degenerate possibilities
        self.checkInput() #always good to validate inputs.  This will handle any invalid letters entered.  It will still raise an exception, but will be more specific in the error reporting.
        self.outputSeqString = self.createOutputString()  #Creates the outputString (the reverse complement).  Because this is called in the __init__ initializer method, we automatically calculate the reverse complement (why this is convenient will be covered in the __str__ overload method)
        self.outputList = False  #this initializes an attribute to False.  Why we want to do this will be covered as part of a later method.
        
        
    def __str__(self):  #this is overloading the existing str(object) method.  Normally, if I tried to print(thisObject), I would either get an exception or a bunch of rubbish back.
        return self.outputSeqString  #Instead, this says that if I try to print the entire object or turn it to a string, what I REALLY want to get back is the outputSeqString I created in the initialization function
        
    def createComplementTable(self):  #Will this work faster is we just define the values by case in our dictionary?
        complementTable =  {"A":"T",
                            "T":"A",
                            "G":"C",
                            "C":"G",
                            "Y":"R",
                            "R":"Y",
                            "S":"S",
                            "W":"W",
                            "K":"M",
                            "M":"K",
                            "B":"V",
                            "D":"H",
                            "H":"D",
                            "V":"B",
                            "N":"N",
                            "a":"t",
                            "t":"a",
                            "g":"c",
                            "c":"g",
                            "y":"r",
                            "r":"y",
                            "s":"s",
                            "w":"w",
                            "k":"m",
                            "m":"k",
                            "b":"v",
                            "d":"h",
                            "h":"d",
                            "v":"b",
                            "n":"n"}
        return complementTable
    
    def createComplementLists(self):  
        complementLists =  {"A":["T"],
                            "T":["A"],
                            "G":["C"],
                            "C":["G"],
                            "Y":["G","A"],
                            "R":["T","C"],
                            "S":["C","G"],
                            "W":["T","A"],
                            "K":["A","C"],
                            "M":["T","G"],
                            "B":["G","C","A"],
                            "D":["T","C","A"],
                            "H":["T","G","A"],
                            "V":["T","G","C"],
                            "N":["T","G","C","A"],
                            "a":["t"],
                            "t":["a"],
                            "g":["c"],
                            "c":["g"],
                            "y":["g","a"],
                            "r":["t","c"],
                            "s":["c","g"],
                            "w":["t","a"],
                            "k":["a","c"],
                            "m":["t","g"],
                            "b":["g","c","a"],
                            "d":["t","c","a"],
                            "h":["t","g","a"],
                            "v":["t","g","c"],
                            "n":["t","g","c","a"]}
        return complementLists
    
    def checkInput(self):  #Input validation
        for letter in self.inputSeq:   #iterate over the input letters
            if letter not in list(self.complementLists.keys()):  #get a list of keys from the complement table, and if a letter is in the input sequence that is not a key in the table
                raise ValueError(letter + " in " + self.inputSeq + " is not a valid DNA base.")  #Raise an exception that explicitly lists what the problem was and where.  Help the user help themselves.
            
    def createOutputString(self):  #This simple function creates our most basic output: a reverse complement string containing any degeneracy that may have been in the original
        output = ""  #intialize an empty string
        for letter in self.inputSeq:  #iterate over our input string (which, if appropriate was reversed in the initializer)
            output += self.complementTable[letter]  #add on the proper complementary base to the growing output string
        return output  #return the output
    
    def permutations(self):  #turn a sequence containing degenerate bases into a list of all possible non-degenerate sequences
        import itertools  #this library contains the code we need to create all possible permutations and probably does so more efficiently than our own code would
        if self.outputList:  #if we already have the value we are trying to create here (and we can tell because it is no longer the False value we initialized it to)
            return self.outputList  #we avoid repeating previous work and just output what we already have stored.  As will be shown in the test code below, the work required for this function can grow exponentially.  We only want to run it if it is requested AND we only ever want to run it the one time.
        letterList = []  #initialize an empty list to store a list of lists, where the outer list will correspond to the letters of the sequence and each inner list will represent all possibilities for that letter
        for letter in self.inputSeq:  #iterate over the input sequence
            letterList.append(self.complementLists[letter])  #add a list of possible bases to a growing list of possible bases at each position
        self.outputList = [''.join(letter) for letter in itertools.product(*letterList)]  #use the itertools module's product function to create the permutations (if this line seems strange to you, try looking up list comprehension in python and positional arguments, commonly called *args)
        return self.outputList #return the (potentially quite large) list
    
class RNAReverseComplement(ReverseComplement):  #declare another class called RNAReverseComplement as an extension of the ReverseComplement base class
    
    def createComplementTable(self):  #Will this work faster is we just define the values by case in our dictionary?
        complementTable =  {"A":"U",
                            "T":"A",
                            "U":"A",
                            "G":"C",
                            "C":"G",
                            "Y":"R",
                            "R":"Y",
                            "S":"S",
                            "W":"W",
                            "K":"M",
                            "M":"K",
                            "B":"V",
                            "D":"H",
                            "H":"D",
                            "V":"B",
                            "N":"N",
                            "a":"u",
                            "t":"a",
                            "u":"a",
                            "g":"c",
                            "c":"g",
                            "y":"r",
                            "r":"y",
                            "s":"s",
                            "w":"w",
                            "k":"m",
                            "m":"k",
                            "b":"v",
                            "d":"h",
                            "h":"d",
                            "v":"b",
                            "n":"n"}
        return complementTable
    
    def createComplementLists(self):  
        complementLists =  {"A":["U"],
                            "T":["A"],
                            "U":["A"],
                            "G":["C"],
                            "C":["G"],
                            "Y":["G","A"],
                            "R":["U","C"],
                            "S":["C","G"],
                            "W":["U","A"],
                            "K":["A","C"],
                            "M":["U","G"],
                            "B":["G","C","A"],
                            "D":["U","C","A"],
                            "H":["U","G","A"],
                            "V":["U","G","C"],
                            "N":["U","G","C","A"],
                            "a":["u"],
                            "t":["a"],
                            "u":["a"],
                            "g":["c"],
                            "c":["g"],
                            "y":["g","a"],
                            "r":["u","c"],
                            "s":["c","g"],
                            "w":["u","a"],
                            "k":["a","c"],
                            "m":["u","g"],
                            "b":["g","c","a"],
                            "d":["u","c","a"],
                            "h":["u","g","a"],
                            "v":["u","g","c"],
                            "n":["u","g","c","a"]}
        return complementLists

class InosineReverseComplement(ReverseComplement):
    
    def createComplementTable(self):  #Will this work faster is we just define the values by case in our dictionary?
        complementTable =  {"A":"T",
                            "T":"A",
                            "G":"C",
                            "C":"G",
                            "Y":"R",
                            "R":"Y",
                            "S":"S",
                            "W":"W",
                            "K":"M",
                            "M":"K",
                            "B":"V",
                            "D":"H",
                            "H":"D",
                            "V":"B",
                            "N":"N",
                            "I":"N",
                            "a":"t",
                            "t":"a",
                            "g":"c",
                            "c":"g",
                            "y":"r",
                            "r":"y",
                            "s":"s",
                            "w":"w",
                            "k":"m",
                            "m":"k",
                            "b":"v",
                            "d":"h",
                            "h":"d",
                            "v":"b",
                            "n":"n",
                            "i":"n"}
        return complementTable
    
    def createComplementLists(self):  
        complementLists =  {"A":["T","I"],
                            "T":["A","I"],
                            "G":["C","I"],
                            "C":["G","I"],
                            "Y":["G","A","I"],
                            "R":["T","C","I"],
                            "S":["C","G","I"],
                            "W":["T","A","I"],
                            "K":["A","C","I"],
                            "M":["T","G","I"],
                            "B":["G","C","A","I"],
                            "D":["T","C","A","I"],
                            "H":["T","G","A","I"],
                            "V":["T","G","C","I"],
                            "N":["T","G","C","A","I"],
                            "I":["A","T","G","C","I"],
                            "a":["t","i"],
                            "t":["a","i"],
                            "g":["c","i"],
                            "c":["g","i"],
                            "y":["g","a","i"],
                            "r":["t","c","i"],
                            "s":["c","g","i"],
                            "w":["t","a","i"],
                            "k":["a","c","i"],
                            "m":["t","g","i"],
                            "b":["g","c","a","i"],
                            "d":["t","c","a","i"],
                            "h":["t","g","a","i"],
                            "v":["t","g","c","i"],
                            "n":["t","g","c","a","i"],
                            "i":["a","t","g","c","i"]}
        return complementLists
       
class NondegenerateBases(ReverseComplement):
    
    def __init__(self, sequence, case = 'original'):
        case = case.lower()
        if not case in ['upper','lower','original']:
            raise ValueError('Case option must be set to upper, lower, or original.')
        self.case = case
        self.inputSeq = sequence  #we store the value without reversing.  The self.[name] means that this value will be variable that can be called from anywhere within this instance of the object AND from outside the object by calling [instance].[name].  A variable that is tied to a function like this one is called an attribute. 
        if self.case == 'upper':  #now that case is being handled by the dictionary itself, we just need to change the original sequence if necessary
            self.inputSeq = self.inputSeq.upper()  
        elif self.case == 'lower':
            self.inputSeq == self.inputSeq.lower()
        self.complementLists = self.createComplementLists()  #same as above, but this one gets back all non-degenerate possibilities
        self.checkInput() #always good to validate inputs.  This will handle any invalid letters entered.  It will still raise an exception, but will be more specific in the error reporting.
        self.outputList = self.permutations()  #this initializes an attribute to False.  Why we want to do this will be covered as part of a later method.
        
    def __str__(self, separator = "\n"):
        return separator.join(self.outputList)
    
    def __iter__(self):
        for i in range(0,len(self.outputList)):
            yield self.outputList[i]
            
    def __getitem__(self, index):
        return self.outputList[index]
    
    def __len__(self):
        return len(self.outputList)
        
    def createComplementLists(self):  
        complementLists =  {"A":["A"],
                            "T":["T"],
                            "G":["G"],
                            "C":["C"],
                            "Y":["C","T"],
                            "R":["A","G"],
                            "S":["G","C"],
                            "W":["A","T"],
                            "K":["T","G"],
                            "M":["A","C"],
                            "B":["C","G","T"],
                            "D":["A","G","T"],
                            "H":["A","C","T"],
                            "V":["A","C","G"],
                            "N":["A","C","G","T"],
                            "a":["a"],
                            "t":["t"],
                            "g":["g"],
                            "c":["c"],
                            "y":["c","t"],
                            "r":["a","g"],
                            "s":["g","c"],
                            "w":["a","t"],
                            "k":["t","g"],
                            "m":["a","c"],
                            "b":["c","g","t"],
                            "d":["a","g","t"],
                            "h":["a","c","t"],
                            "v":["a","c","g"],
                            "n":["a","c","g","t"]}
        return complementLists   

    def permutations(self):  #turn a sequence containing degenerate bases into a list of all possible non-degenerate sequences
        import itertools  #this library contains the code we need to create all possible permutations and probably does so more efficiently than our own code would
        try: #This try/except block is another way of determining if we have already calculated this list out.  I do not know which method is more efficient, but the difference is probably negligible in this context
            if self.outputList:  #if we already have the value we are trying to create here (and we can tell because it is no longer the False value we initialized it to)
                return self.outputList  #we avoid repeating previous work and just output what we already have stored.  As will be shown in the test code below, the work required for this function can grow exponentially.  We only want to run it if it is requested AND we only ever want to run it the one time.
        except (AttributeError, NameError):
            letterList = []  #initialize an empty list to store a list of lists, where the outer list will correspond to the letters of the sequence and each inner list will represent all possibilities for that letter
            for letter in self.inputSeq:  #iterate over the input sequence
                letterList.append(self.complementLists[letter])  #add a list of possible bases to a growing list of possible bases at each position
            self.outputList = [''.join(letter) for letter in itertools.product(*letterList)]  #use the itertools module's product function to create the permutations (if this line seems strange to you, try looking up list comprehension in python and positional arguments, commonly called *args)
            return self.outputList #return the (potentially quite large) list

#================================================Search Objects to find potential targets in an indexed genome based on guide RNA sequence=======================================================
    
class SearchSupervisor(object):
    
    def __init__(self, args):
        self.jobTemplate = self.blankJob()
    
    
    def createTempDir(self):
        if args.verbose:
            print ("Creating temporary directory")
        import re
        import os
        import datetime
        currenttime = datetime.datetime.now()
        currenttime = str(currenttime)
        currenttime = re.sub(r'\W','',currenttime)
        self.tempDir = '.dsNickFuryMission' + currenttime
        if os.path.isdir(self.tempDir):
            raise FileExistsError('Temporary directory for this job already exists.  Please look into this.  Directory name: ' + self.tempDir)
        os.mkdir(self.tempDir)
        os.mkdir(self.tempDir + "/completed")
        os.mkdir(self.tempDir + "/progress")
        if args.verbose:
            print ("Temporary directory created.")
        return True
                
    def createBlankJob(self):
        self.blankJob = {
            sequence:args.searchSequence,
            referenceFiles:[]
        }
        return True
    
    def createJobList(self):
        if args.verbose:
            print ("Creating a list of jobs.")
        self.jobList = []
        for i in range(0,args.parallelJobs):
            self.jobList[i] = self.blankJob
        indexedReferenceFiles = getRefFiles()
        self.checkInputSequence(indexedReferenceFiles)
        remainder = len(indexedReferenceFiles) % args.parallelJobs
        filesPerJob = len(indexedReferenceFiles) // args.parallelJobs
        assignedFileCount = []
        for i in range(0,args.parallelJobs):
            if i < remainder:  #because it is indexed to zero, if we have a remainder of 1, we only need an extra job for the zeroth index.  If we have remainder of zero, nobody needs an extra job.  If Donald Trump wins, everybody will need two extra jobs.
                assignedFileCount[i] = filesPerJob + 1
            else:
                assignedFileCount[i] = filesPerJob
        counter = 0
        jobID = 0
        for file in indexedReferenceFiles:
            if counter <= assignedFileCount[jobID]:
                self.jobList[i][referenceFiles] += file
                counter += 1
            else:
                jobID += 1
                counter = 0
        return True
    
    def checkInputSequence(self, fileList):
        file = open(self.tempDir + "/" + fileList[0], 'r')
        firstLine = file.readline()
        file.close()
        firstLine.strip()
        firstLine.strip("\n")
        firstLine.strip("\r")
        refArray = firstLine.split("_")
        
        refLength = len(firstLine)
        seqLength = len(self.sequence)
        if seqLength > refLength:
            quit("Search sequence guide RNA is longer than indexed references.")
            
    def assignJobs(self):
        import pickle  #pickle has security issues, know about them before using it
        for i in range(1,len(self.jobList)):  #we index to 1 here because job 0 (which will have an equal or greater number of searches) will be reserved for the supervisor instance
            pickle.dump(job, open(self.tempDir + "/mission" + str(i), "wb"))  #this could also be dumped to a network socket
            self.createJobBash(i)
            self.submitJob(i)
        args.workerID = "0"
        myJob = workerJob(str(0), jobList[0])
        self.matches = myJob.run(returnToSelf = True)  #this will both make this instance work AND function as a bit of a timer
        
    def monitorJobs(self):
        import time
        import os
        allDone = False
        while not allDone:
            for i in range(1,len(self.jobList)):
                if not os.path.isfile(self.tempDir + "/completed/" + str(i)):
                    allDone = False
                    time.sleep(10)
                    break
                else:
                    allDone = True
        return True
    
    def gatherJobs(self):
        import pickle
        for i in range(1,len(self.jobList)):
            gatheredPart = pickle.load(open(self.tempDir + "/result" + str(i), "rb"))
            for j in range(0,args.mismatchTolerance + 1):
                self.matches[j] += gatheredPart[j]
            
    def createJobBash(self, jobID):
        pass
    
    def submitJob(self, jobID):
        pass
    
class WorkerJob(object):
    
    def __init__(self, jobID, jobList = False, ):
        if not jobList:
            jobList = getJobList()
        self.sequence = jobList[sequence]
        self.fileList = jobList[referenceFiles]
        self.matches = []
        self.revSeq = self.sequence[::-1]
        self.refPam, self.refGuide = self.revSeq[::-1].split("_")
        self.colorScheme = self.createColorScheme()
        self.checkAllSequences()

    def getJobList(self):
        import pickle
        jobList = pickle.load(open(args.tempDir + "/mission" + args.workerID, "rb"))
        return jobList
        
    def createColorScheme(self):
        colorScheme = []
        if args.mismatchTolerance > 8:
            increments = 8
        elif args.mismatchTolerance == 0:
            return ["0,0,0"]
        else:
            increments = args.mismatchTolerance
            step = 255//increments
        for i in range(0,args.mismatchTolerance):
            if i < 8:
                red = 255 - (step*i)
                green = 0
                blue = 0 + step*i
                colorScheme.append(str(red) + "," + str(green) + "," + str(blue))
            else:
                colorScheme.append(str(red) + ",0," + str(blue))
        return colorScheme
        
    def checkAllSequences(self):
        for file in self.fileList:
            file = open(self.tempDir + "/" + self.fileList[0], 'r')
            line = file.readline()
            while line:
                mismatches = 0
                chrom, begin, end, refSeq, score, strand = line.split("\t")
                pam, guide = refSeq.split("_")
                for i in range(0,len(guide)):
                    if guide[i] != self.refGuide[i]:
                        mismatches += 1
                        if mismatches > args.mismatchTolerance:
                            line = file.readline()
                            break
                    self.matches.append([chrom, begin, end, refSeq[::-1].replace("_",""), str(1000*((len(guide)-mismatches)/len(guide))), strand, "", "", self.colorScheme[mismatches]])

    def reportResult(self):
        output = open(self.tempDir + "/result" + args.workerID, "w")
        for line in self.matches:
            output.write("\t".join(line) + "\n")  #check if this works more efficiently from a pickle
        output.close()
        clockOut = open(self.tempDir + "/completed/" + args.workerID + ".done", "w")
        clockOut.close()
        quit()

#===================================================FASTA indexing objects.  Requires a FASTA and FAI as input and will output a directory containing a list of targets for the system from the genome.=======================

class FASTAIndexLine(object):
    
    def __init__(self, line):
    # read from start to length + (length // 50) + start
        import re
        line = line.split("\t")
        line[0] = re.sub(r'chr','',line[0])
        self.contig = line[0]
        self.length = int(line[1])
        self.start = int(line[2])
        self.lineBases = int(line[3])
        self.lineBytes = int(line[4])
        self.end = self.length + ((self.lineBytes-self.lineBases)*(self.length // self.lineBases)) #this accounts for the fact that length is counted in bases and not bytes, and missed all the newline bytes that terminate each line

class FASTASupervisor(object):
    
    def __init__(self):
        self.getFiles(args.inputfile)
        self.createTempDir()
        self.createOutputDir()
        self.faiJobs()
    
    def getFiles(self, fastaName):
        try:
            self.fasta = open(fastaName)
            firstLine = self.fasta.readline()
            if not ">" in firstLine:
                quit(fastaName + " does not appear to be a properly formatted FASTA file.  Please check to be sure that it follows FASTA standards.")
            self.fasta.close()
        except FileNotFoundError:
            quit(fastaName + " was not found.  This file was passed as the reference genome.")
        try:
            self.fai = open(fastaName + ".fai",'r')
        except FileNotFoundError:
            try:
                self.fai = open(fastaName[:-4] + ".fai", 'r')
            except FileNotFoundError:
                quit("No FASTA index (.fai) file could be found for " + fastaName + " please run a FASTA indexer and try again.")
    
    def createOutputDir(self):
        import os
        outputDirectory = args.sequence[::-1] + "." + args.genome
        if os.path.isdir(outputDirectory) and not args.clobber:
            quit("This genome/system combination has already been indexed.")
        if not os.path.isdir(outputDirectory):
            os.mkdir(outputDirectory)
    
    def faiJobs(self):
        contigJobs = []
        rawLine = self.fai.readline()
        while rawLine:
            line = FASTAIndexLine(rawLine)
            contigJobs.append(line)
            rawLine = self.fai.readline()
        for job in contigJobs[1:]:
            self.createJobBash(job)
            self.submitJob(job)
        myJob = contigJobs[0]
        args.chromosome = myJob.contig
        args.start = str(myJob.start)
        args.length = str(myJob.end)
        myRun = FASTAreader()
        print("Completed this job.  Parallel jobs may still be running.")
    
    def calculateRAM(contigSize):
        pass  #skipping this method, as it seems like everything can run with 2G or less
    
    def createTempDir(self):
        import re
        import os
        import datetime
        currenttime = datetime.datetime.now()
        currenttime = str(currenttime)
        currenttime = re.sub(r'\W','',currenttime)
        self.tempDir = '.indexJob' + currenttime
        args.tempDir = self.tempDir
        if os.path.isdir(self.tempDir):
            raise FileExistsError('Temporary directory for this job already exists.  Please look into this.  Directory name: ' + self.tempDir)
        os.mkdir(self.tempDir)
        os.mkdir(self.tempDir + "/completed")
        os.mkdir(self.tempDir + "/progress")
        return True
    
    def createJobBash(self,job):
        import os
        self.bash = self.tempDir + "/" + job.contig + ".sh"
        bashFile = open(self.bash, 'w')
        bashFile.write("#! /bin/bash\n")
        bashFile.write("module load python/3.4\n")
        bashFile.write("python3 dsNickFury" + currentVersion + ".py --mode FASTAWorker --chromosome " + job.contig + " --start " + str(job.start) + " --length " + str(job.end) + " --sequence " + args.sequence + " --inputfile " + os.path.abspath(args.inputfile) + " --genome " + args.genome + " --tempDir " + args.tempDir + "\n")
        bashFile.close()
    
    def submitJob(self, job):
        shortName = "NickFury" + job.contig
        command = "qsub -cwd -V -N " + shortName + " -l h_data=2G,time=8:00:00 " + self.bash
        if not args.mock:
            import os
            os.system(command)
        else:
            print ("MOCK SUBMIT: " + command)
            

class FASTAWindow(object):
    
    def __init__(self, inputFile, contigStart, contigLength, windowsize, pamList):
        self.lastGroup = 0
        self.done = False
        self.windowsize = windowsize
        self.start = 0  #start is inclusive
        self.end = self.windowsize #end is not inclusive (keeping with BED standards)
        self.pamList = pamList
        self.pamLength = len(pamList[0])
        inputFile.seek(int(contigStart))
        # lastgroup = 0
        # self.chromosome = ""
        # contigLength = int(contigLength)
        # rawline = inputFile.readline()
        # print("Reading in contig")
        # while len(self.chromosome) < contigLength and rawline and ">" not in rawline: #processing in file peacemeal because trying to process the whole buffer at once causes a memory exception
        #     if len(self.chromosome) // 1000000 > lastgroup:
        #         print(".", end = "")
        #         lastgroup = len(self.chromosome) // 1000000
        #     rawline = rawline.replace("\n","")
        #     rawline = rawline.upper()
        #     self.chromosome += rawline
        #     rawline = inputFile.readline()
        # print("Done")
        self.chromosome = inputFile.read(int(contigLength))
        self.chromosome = self.chromosome.replace("\n","")
        self.chromosome = self.chromosome.upper()
        self.chromosomeLength = len(self.chromosome)
        
    def match(self):
        self.forwardMatch = False
        self.reverseMatch = False
        if self.start // 10000 > self.lastGroup:
            print("Tested " + str((self.start // 10000)*10000), end = "\r")
            self.lastGroup = self.start // 10000
        self.sequence = self.chromosome[self.start:self.end]
        if self.sequence[-1] == "N":
            self.nInLastPositionJump()
            return False
        if "N" in self.sequence:
            return False
        if self.sequence[-self.pamLength:] in self.pamList:
            guide = self.sequence[:-self.pamLength]
            pam = self.sequence[-self.pamLength:]
            self.forwardMatch = guide + "_" + pam
        else:
            self.forwardMatch = False
        revComp = str(ReverseComplement(self.sequence))
        if revComp[-self.pamLength:] in self.pamList:
            guide = revComp[:-self.pamLength]
            pam = revComp[-self.pamLength:]
            self.reverseMatch = guide + "_" + pam
        else:
            self.reverseMatch = False
        return (self.forwardMatch or self.reverseMatch)
    
    def nInLastPositionJump(self):
        self.start += self.windowsize - 1
        self.end += self.windowsize - 1
            
    def advance(self):
        self.start += 1
        self.end += 1
        self.done = self.end > self.chromosomeLength
        
    def getNextMatch(self):
        self.first = True
        while not self.match() and not self.done or self.first:
            self.first = False
            self.advance()
        return (not self.done)
        
    
class FASTAreader(object):
    
    def __init__(self):
        hitCount = 0
        inputFile = open(args.inputfile, 'r')
        self.outputDirectory = args.sequence[::-1] + "." + args.genome
        try:
            chromosome = int(args.chromosome)
            chromosome = str(chromosome).zfill(2)
        except ValueError:
            chromosome = args.chromosome
        if chromosome == "M":
            fileChromosome = "zM"
        else:
            fileChromosome = chromosome
        windowsize = len(args.sequence) - 1
        guide, pam = args.sequence.split("_")
        degeneratePam = False
        for character in pam:
            if character not in ["A","T","G","C"]:
                degeneratePam = True
        if not degeneratePam:
            pamList = [pam]
        else:
            pamList = list(NondegenerateBases(pam))
        window = FASTAWindow(inputFile, args.start, args.length, windowsize, pamList)
        outputFileName = self.outputDirectory + "/" + fileChromosome + "c" + str(hitCount // 10000).zfill(9)
        outputFile = open(outputFileName, 'w')
        while window.getNextMatch():
            if window.forwardMatch:
                outputFile.write("\t".join([args.chromosome, str(window.start), str(window.end), window.forwardMatch[::-1], "", "+\n"]))
                hitCount += 1
                if hitCount % 10000 == 0:
                    outputFile.close()
                    outputFileName = self.outputDirectory + "/" + fileChromosome + "c" + str(hitCount // 10000).zfill(9)
                    outputFile = open(outputFileName, 'w')
            if window.reverseMatch:
                outputFile.write("\t".join([args.chromosome, str(window.start), str(window.end), window.reverseMatch[::-1], "", "-\n"]))
                hitCount += 1
                if hitCount % 10000 == 0:
                    outputFile.close()
                    outputFileName = self.outputDirectory + "/" + fileChromosome + "c" + str(hitCount // 10000).zfill(9)
                    outputFile = open(outputFileName, 'w')
        outputFile.close()
        touchFile = open(args.tempDir + "/completed/" + args.chromosome, 'w')
        touchFile.close()
        countFileName = self.outputDirectory +".counts"
        countFile = open(countFileName, 'a')
        countFile.write(args.chromosome + "\t" + str(hitCount) + "\n")
        countFile.close()

#=====================================================Execution code===========================================================================

def main():
    import datetime
    startTime = datetime.datetime.now()
    arguments = Args()
    global args
    args = arguments
    del arguments
    if args.mode == 'index':
        run = FASTASupervisor()
    elif args.mode == 'FASTAWorker':
        run = FASTAreader()
    elif args.mode == 'search':
        run = SearchSupervisor()
    elif args.mode == 'worker':
        run = WorkerJob()
    runTime = datetime.datetime.now() - startTime
    print ("Run completed in " + (str(runTime)))
    
main()
    
