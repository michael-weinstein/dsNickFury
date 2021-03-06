#!/usr/bin/env python3
'''
Software License
Commercial reservation
This License governs use of the accompanying Software, and your use of the Software constitutes acceptance of this license.

You may use this Software for any non-commercial purpose, subject to the restrictions in this license. Some purposes which can be non-commercial are teaching, academic research, and personal experimentation. 

You may not use or distribute this Software or any derivative works in any form for any commercial purpose. Examples of commercial purposes would be running business operations, licensing, leasing, or selling the Software, or distributing the Software for use with commercial products. 

You may modify this Software and distribute the modified Software for non-commercial purposes; however, you may not grant rights to the Software or derivative works that are broader than those provided by this License. For example, you may not distribute modifications of the Software under terms that would permit commercial use, or under terms that purport to require the Software or derivative works to be sublicensed to others.

You agree: 
1.	Not remove any copyright or other notices from the Software.
2.	That if you distribute the Software in source or object form, you will include a verbatim copy of this license.
3.	That if you distribute derivative works of the Software in source code form you do so only under a license that includes all of the provisions of this License, and if you distribute derivative works of the Software solely in object form you do so only under a license that complies with this License.
4.	That if you have modified the Software or created derivative works, and distribute such modifications or derivative works, you will cause the modified files to carry prominent notices so that recipients know that they are not receiving the original Software. Such notices must state: (i) that you have changed the Software; and (ii) the date of any changes.
5.	THAT THIS PRODUCT IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS PRODUCT, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.  YOU MUST PASS THIS LIMITATION OF LIABILITY ON WHENEVER YOU DISTRIBUTE THE SOFTWARE OR DERIVATIVE WORKS.

6.	That if you sue anyone over patents that you think may apply to the Software or anyone's use of the Software, your license to the Software ends automatically.
7.	That your rights under the License end automatically if you breach it in any way.
8.	UCLA and the Regents of the University of California reserves all rights not expressly granted to you in this license.

9.	Nothing in this Agreement grants by implication, estoppel, or otherwise any rights to any intellectual property owned by the Regents of the University of California, except as explicitly set forth in this license.
10.	You will hold the Regents of the harmless for all claims, suits, losses, liabilities, damages, costs, fees, and expenses resulting from their respective activities arising from this license.  
11.	You will not use any name, trade name, trademark, name of any campus, or other designation of the Regents of the University of California in advertising, publicity, or other promotional activity, except as permitted herein.
'''

#USEFUL DEFAULT SETTINGS HERE
global pythonInterpreterAbsolutePath
pythonInterpreterAbsolutePath = ""  #Set the absolute path for your python interpreter here.  Depending on your system configuration, you may also be able to use a shortcut, such as python3, but that has a greater chance of errors

global selectionModeTargetLimitPerJob
selectionModeTargetLimitPerJob = 0 #This prevents a user from submitting a job with too many target sites that might overload or degrade performance on the system.  Clobber mode can override this.  Change this value according to your system's capabilities.  Set to 0 or negative value for no limit.

global clusterDefaultSelectionModeParallelJobLimit; global standAloneDefaultSelectionModeParallelJobLimit
clusterDefaultSelectionModeParallelJobLimit = 230  #Limit on how many simultaneous parallel jobs can be going at once on a cluster (set this based on the limit for how many queued items you can have)
standAloneDefaultSelectionModeParallelJobLimit = 32  #Limit on how many simultaneous parallel jobs can be going if run on a single system.  Change according to your machine.

global currentVersion
currentVersion = "1.1"

global versionName
versionName = "...and it happened at Villa Straylight"

global yearWritten
yearWritten = "2015"

def yesAnswer(question):  #asks the question passed in and returns True if the answer is yes, False if the answer is no, and keeps the user in a loop until one of those is given.  Also useful for walking students through basic logical python functions
    answer = False  #initializes the answer variable to false.  Not absolutely necessary, since it should be undefined at this point and test to false, but explicit is always better than implicit
    while not answer:  #enters the loop and stays in it until answer is equal to True
        print (question + ' (Y/N)')  #Asks the question contained in the argument passed into this subroutine
        answer = input('>>') #sets answer equal to some value input by the user
        if str(answer) == 'y' or str(answer) == 'Y':  #checks if the answer is a valid yes answer
            return True  #sends back a value of True because of the yes answer
        elif str(answer) == 'n' or str(answer) == 'N': #checks to see if the answer is a valid form of no
            return False  #sends back a value of False because it was not a yes answer
        else: #if the answer is not a value indicating a yes or no
            print ('Invalid response.')
            answer = False #set ansewr to false so the loop will continue until a satisfactory answer is given

def reportUsage(details):  #this will report usage back to us.  This is required by the people who maintain the Azimuth server.  This will not send back any details of your job except if azimuth was used.
    import urllib.request
    url = "http://pathways.mcdb.ucla.edu/cgi-bin/MW_counter/counter.cgi?counter=" + details
    try:
        req = urllib.request.urlopen(url)
    except:
        pass        

def printStartUp():
    print("Double-stranded Nick Fury -- Watch your Crispr targets with both eyes.")
    print("Version " + currentVersion + " (" + versionName + ")")
    print("By Michael M. Weinstein, Copyright " + yearWritten)
    print("Dan Cohn Laboratory and Collaboratory, University of California, Los Angeles")
        
def printManual():
    import urllib.request
    manualURL = 'https://raw.githubusercontent.com/michael-weinstein/dsNickFury/master/readme.md'
    try:
        rawManual = urllib.request.urlopen(manualURL)
        text = rawManual.read().decode('utf-8')
        print("Manual from " + manualURL)
        print(text)
    except:
        print("Unable to download and display manual.  Please view it in your browser at:\n\n" + manualURL + "\n")
    
def checkPythonInterpreterAbsolutePath(absPath):
    import os
    import subprocess
    if not absPath:
        printManual()
        quit("ABORTED: You must set the absolute path for your python interpreter at the beginning of this script.")
    if not os.path.isfile(absPath):  #if the absolute path is not actually a file, check if we have an alias we can expand upon
        import subprocess
        try:
            absPath = subprocess.check_output(['which',absPath]).decode('utf-8').strip()
        except subprocess.CalledProcessError:
            quit("ABORTED: Python interpreter not found at " + absPath + " and it does not appear to be a valid alias.  Please correct the location.")
    return absPath
pythonInterpreterAbsolutePath = checkPythonInterpreterAbsolutePath(pythonInterpreterAbsolutePath)

#===================================Command line Argument Checking===========================================

class Args(object):
    
    def __init__(self):
        import os
        import argparse #loads the required library for reading the commandline
        parser = argparse.ArgumentParser()
        parser.add_argument("--manual", help = "Print out the user manual and sample command lines.", action = 'store_true')
        parser.add_argument ("-m", "--mode", help = "Specify how the program is to run (what the desired task is)")
        parser.add_argument ("-g", "--genome", help = "Specify the genome for searching or indexing.")
        parser.add_argument ("-d", "--inputDirectory", help = "Specify genome index directory for a worker job.")
        parser.add_argument ("-f", "--inputfile", help = "Specify a single input file for splitting")
        parser.add_argument ("--tempDir", help = "Temporary directory name for parallel jobs")
        parser.add_argument ("-p", "--parallelJobs", help = "Max number of parallel jobs at once. (Or per search if running in selection mode)")
        parser.add_argument ("-9", "--clobber", help = "Do not ask before overwriting files.", action = 'store_true')
        parser.add_argument ("-w", "--workerID", help = "Worker process ID.  Users should not be setting this value.")
        parser.add_argument ("-s", "--sequence", help = "Sequence of interest.  Format: NNNNNNGUIDERNANNNNNN_PAM")
        parser.add_argument ("-t", "--mismatchTolerance", help = "Maximim number of mismatches permitted for a positive result.")
        parser.add_argument ("--verbose", help = "Run in verbose mode", action = 'store_true')
        parser.add_argument ("--mock" , help = "Print exec commands instead of running them.", action = 'store_true')
        parser.add_argument ("--ordered", help = "Do not break up chromosomes for parallel analysis.", action = 'store_true')
        parser.add_argument ("-c", "--chunkSize", help = "Specify the chunk size for parallel genome annotation.")
        parser.add_argument ("--chromosome", help = "Used to specify the chromosome/contig ID.  This should be passed by the machine and not the user.")
        parser.add_argument ("--start", help = "Used to specify the starting byte of the FASTA for indexing.  This should be passed by the machine and not the user.")
        parser.add_argument ("--length", help = "Used to specify the bytelength of the chunk to be indexed by the program.  This should be passed by the machine and not the user.")
        parser.add_argument ("--forceJobIndex", help = "Force the indexing supervisor instance to take a specific job index.  Mostly useful for debugging functions.")
        parser.add_argument ("--outputDirectory", help = "Directory for outputting search results to a hypervisor.  This should generally be passed by the machine and not the user.")
        parser.add_argument ("--noCleanup", help = "Leave behind any temporary files for future inspection.", action = 'store_true')
        parser.add_argument ("--forceGenome", help = "Force the search supervisor to use this genome directory.  Generally this should be passed by the machine and not the user.")
        parser.add_argument ("--species", help = "Tell the indexer which species the genome is from.")
        parser.add_argument ("--targetSequence", help = "Enter a long sequence here to search for and analyze potential targets.")
        parser.add_argument ("--targetFasta", help = "Enter a file name for a FASTA file to search for and analyze potential target sites.")
        parser.add_argument ("--targetList", help = "Enter a list of potential sites to analyze for off-target risk.")
        parser.add_argument ("--noForcedBases", help = "Prevent forcing bases 1 and/or 3 in the guide RNA to match those submitted for Azimuth analysis")
        parser.add_argument ("--skipAzimuth", help = "Do not attempt Azimuth analysis.", action = 'store_true')
        parser.add_argument ("--parallelJobLimit", help = "Set a limit on the number of parallel jobs allowed at once in the queue for highly parallelized tasks (this MUST be set below your scheduler's limit for queued jobs for a single user, and should be set 5-10 percent below it).")
        parser.add_argument ("--genomeDirectory", help = "Specify an alternate directory to search for suitable indexed genomes.")
        parser.add_argument ("--annotationExpansion", help = "Specify how far from the target site to search for an annotated gene/genomic feature (default is 1KB).")
        parser.add_argument ("--azimuthSequence", help = "Specify a sequence for Azimuth analysis.")
        parser.add_argument ("--outputToFile", help = "In selection mode, dump the output to the filename passed as an argument here.")
        parser.add_argument ("--scratchFolder", help = "Specify a directory to use for writing temporary (job) folders.")
        parser.add_argument ("--cluster", help = "Specify that this is running on a cluster system.", action = "store_true")
        parser.add_argument ("--standAlone", "--standalone", help = "Specify that this is running on a single system or server.", action = "store_true")
        args = parser.parse_args()  #puts the arguments into the args object
        
        if args.standAlone and args.cluster: #You really can't be both.
            quit("Aborted: You must specify either --cluster or --standAlone.  You can't be both.")
        if not (args.standAlone or args.cluster or args.manual) and args.mode in ['search', 'index', 'selection']:
            quit("ABORTED: You must specify if this will be running on a stand-alone system or a cluster. (--standAlone or --cluster)")
        else:
            if args.standAlone:
                self.standAlone = True
                self.cluster = False
            if args.cluster:
                self.cluster = True
                self.standAlone = False
        if not args.mode and not args.manual:  #series of case statements for mode to determine which set of inputs to validate.  If no mode was set, it will see if the user is asking for the manual.  
            quit("ABORTED: No run mode was set on the commandline.")
        self.mode = args.mode
        if not args.genomeDirectory:
            self.genomeListDirectory = "genomes/"
        else:
            self.genomeListDirectory = args.genomeDirectory
            if not self.genomeListDirectory[-1] == "/":
                self.genomeListDirectory += "/"
            if not os.path.isdir(self.genomeListDirectory) and not self.mode == 'index':
                quit("ABORTED: User-specified genome: " + self.genomeListDirectory + " not found.")
        if args.mode == 'worker':
            self.setWorkerArgs(args)
        elif args.mode == 'search':
            self.setSearchArgs(args)
        elif args.mode == 'index':
            self.setIndexArgs(args)
        elif args.mode == 'FASTAWorker':
            self.setFASTAWorkerArgs(args)
        elif args.mode == 'selection':
            self.setSelectionArgs(args)
        elif args.manual:
            printManual()
            quit()
        else:
            quit('ABORTED: Invalid/no mode set on commandline.  Please select a mode or run with --manual set for assistance.')
            
    def setSelectionArgs(self, args):  #validating and setting arguments for selection of targets from a user-provided sequence
        import os
        self.sequence = args.sequence
        if not self.sequence:
            quit("ABORTED: You must specify a generic sequence to describe your system (see manual, argument --manual) for more information.")
        if "_" in args.sequence:
            guide, pam = args.sequence.split("_")
            try:
                guide = int(guide)
            except ValueError:
                pass
            else:
                args.sequence = "N"*guide + "_" + pam
            self.sequence = args.sequence.upper()
        else:
            quit("ABORTED: Invalid sequence passed. Please include an underscore between the guide and PAM sequences.")
        if not len(self.sequence) > 15 and not args.clobber:
            quit("ABORTED: This guide+pam combination appears too short, and will likely cause memory and other errors.  Rerun in clobber mode (argument -9) to proceed anyway.")
        self.targetSequence = args.targetSequence
        self.targetFasta = args.targetFasta
        if self.targetFasta and not os.path.isfile(self.targetFasta):
            quit("ABORTED: " + self.targetFasta + " is not a valid file.")
        self.targetList = args.targetList
        if self.targetList and not os.path.isfile(self.targetList):
            quit("ABORTED: " + self.targetList + " is not a valid file.")
        if not args.genome:
            quit("ABORTED: You must set a genome.  See manual (run with --manual) for details.")
        self.genome = args.genome.upper()
        self.verbose = args.verbose
        self.mock = args.mock
        if args.parallelJobs:
            try:
                self.parallelJobs = int(args.parallelJobs)
            except ValueError:
                quit("ABORTED: Parallel jobs argument must be an integer")
        else: self.parallelJobs = 10
        if not args.mismatchTolerance:
            self.mismatchTolerance = 3
        else:
            try:
                self.mismatchTolerance = int(args.mismatchTolerance)
            except ValueError:
                quit("ABORTED: Mismatch tolerance must be an integer.  Please check your command line options and try again.")
        if args.noForcedBases:
            if args.noForcedBases == "1":
                self.noForcedBases = False
                self.noForced1 = True
                self.noForced3 = False
            if args.noForcedBases == "3":
                self.noForcedBases = False
                self.noForced1 = False
                self.noForced3 = True
            else: #if they put in any other argument here, we block forcing either base (this could include 1,3 or all or anything else)
                self.noForcedBases = True
                self.noForced1 = True
                self.noForced3 = True
        else:  #if the argument was left blank or not passed at all, we allow base forcing
            self.noForcedBases = False
            self.noForced1 = False
            self.noForced3 = False
            self.skipAzimuth = args.skipAzimuth
        self.noCleanup = args.noCleanup
        if not args.parallelJobLimit:
            if self.cluster:
                self.maxParallelJobs = clusterDefaultSelectionModeParallelJobLimit  #set this value at the top of the script for your configuration of choice
            if self.standAlone:
                self.maxParallelJobs = standAloneDefaultSelectionModeParallelJobLimit
        else:
            try:
                self.maxParallelJobs = int(args.parallelJobLimit)
            except ValueError:
                quit("ABORTED: Parallel job limit must be an integer.")
        if self.maxParallelJobs < self.parallelJobs:
            self.maxParallelJobs = self.parallelJobs
        self.outputToFile = args.outputToFile
        if self.outputToFile and os.path.isfile(self.outputToFile) and not args.clobber:
            quit("ABORTED: Output file " + self.outputToFile + " already exists.  Run in clobber mode to overwrite.")
        self.clobber = args.clobber
        self.scratchFolder = args.scratchFolder
        if not self.scratchFolder:
            self.scratchFolder = "" #making sure this is cast to a string and not a NoneType (although that will probably add to a string with no trouble)
        else:
            if not self.scratchFolder[-1] == "/":
                self.scratchFolder = self.scratchFolder + "/"  #make sure that the directory name is passed ending with a slash so we can prepend it directly to our tempDir name
            if not os.path.isdir(self.scratchFolder):
                try:
                    os.mkdir(self.scratchFolder)
                except OSError:
                    if not os.path.isdir(self.scratchFolder):  #This could happen because of a data race type condition, if one process creates the directory after this one checks for it, but before it creates it.  This will catch that problem.
                        quit("ABORTED: Unable to create scratch folder.  Check if directory containing this folder already exists.")
            
    def setWorkerArgs(self, args):  #Validating arguments for a search worker.  This should not require too much validation, as users should not be launching worker processes themselves
        self.mode = "worker"
        self.workerID = args.workerID
        self.tempDir = args.tempDir
        self.sequence = args.sequence
        self.mismatchTolerance = int(args.mismatchTolerance)
        self.inputDirectory = args.inputDirectory
        self.verbose = args.verbose
        self.skipAzimuth = True
           
    def setSearchArgs(self, args):  #Validating arguments for launching a search supervisor.  This will require good validations, as users are likely to be launching this on their own.
        import os
        self.mode = "search"
        self.sequence = args.sequence
        if not self.sequence:
            quit("ABORTED: You must specify a sequence to search for.  Remember to place an underscore between the guide and PAM sequences.")
        if not "_" in self.sequence:
            quit("ABORTED: You must include an underscore '_' in your sequence between the guide RNA portion and the PAM sequence.")
        if not len(self.sequence) > 15 and not args.clobber:
            quit("ABORTED: This guide+pam combination appears too short, and will likely cause memory and other errors.  Rerun in clobber mode (argument -9) to proceed anyway.")
        self.sequence = self.sequence.upper()
        if not args.mismatchTolerance:
            self.mismatchTolerance = 3
        else:
            try:
                self.mismatchTolerance = int(args.mismatchTolerance)
            except ValueError:
                quit("ABORTED: Mismatch tolerance must be an integer.  Please check your command line options and try again.")
        self.tempDir = args.tempDir
        self.workerID = args.workerID
        self.inputDirectory = args.inputDirectory
        self.verbose = args.verbose
        self.mock = args.mock
        if not args.forceGenome:
            self.genome = args.genome.upper()  #if a genome is forced by a hypervisor function, this will prevent an error from trying to uppercase a NoneType variable.
        if args.parallelJobs:
            try:
                self.parallelJobs = int(args.parallelJobs)
            except ValueError:
                quit("ABORTED: Parallel jobs argument must be an integer")
        else:
            self.parallelJobs = 20
        self.outputDirectory = args.outputDirectory
        self.noCleanup = args.noCleanup
        self.forceGenome = args.forceGenome
        self.skipAzimuth = True
        self.annotationExpansion = args.annotationExpansion
        if not self.annotationExpansion:
            self.annotationExpansion = 1000
        else:
            try:
                self.annotationExpansion = int(self.annotationExpansion)
            except ValueError:
                quit("ABORTED: Annotation expansion range must be an integer value.")
        self.azimuthSequence = args.azimuthSequence
        if not self.azimuthSequence or self.azimuthSequence == "False":
            self.azimuthSequence = False
        self.scratchFolder = args.scratchFolder
        if not self.scratchFolder:
            self.scratchFolder = "" #making sure this is cast to a string and not a NoneType (although that will probably add to a string with no trouble)
        else:
            if not self.scratchFolder[-1] == "/":
                self.scratchFolder = self.scratchFolder + "/"  #make sure that the directory name is passed ending with a slash so we can prepend it directly to our tempDir name
            if not os.path.isdir(self.scratchFolder):
                try:
                    os.mkdir(self.scratchFolder)
                except OSError:
                    quit("ABORTED: Unable to create scratch folder.  Check if directory containing this folder already exists.")

    def setIndexArgs(self, args):  #Validating arguments for launching an indexing supervisor.  This will also require good validations as users are likely to be launching this on their own.
        import os
        self.mode = "index"
        if not args.sequence:
            quit("ABORTED: No search sequence specified.")
        if "_" in args.sequence:
            guide, pam = args.sequence.split("_")
            try:
                guide = int(guide)
            except ValueError:
                pass
            else:
                args.sequence = "N"*guide + "_" + pam
            self.sequence = args.sequence.upper()
        else:
            quit("ABORTED: Invalid sequence passed. Please include an underscore between the guide and PAM sequences.")
        if not len(self.sequence) > 15 and not args.clobber:
            quit("ABORTED: This guide+pam combination appears too short, and will likely cause memory and other errors.  Rerun in clobber mode (argument -9) to proceed anyway.")
        if not args.inputfile:
            quit("ABORTED: No FASTA specified for searching.")
        if os.path.isfile(args.inputfile):
            self.inputfile = args.inputfile
        else:
            quit("ABORTED: FASTA file: " + args.inputfile + " not found.")
        if not args.genome:
            quit("ABORTED: You must specify the name you want to identify this genome by.")
        self.genome = args.genome.upper()
        self.clobber = args.clobber
        self.mock = args.mock
        self.tempDir = args.tempDir
        self.ordered = args.ordered
        self.workerID = args.workerID
        self.species = args.species.upper()
        if args.chunkSize:
            try:
                args.chunkSize = int(args.chunkSize)
            except ValueError:
                quit("ABORTED: Invalid chunk size passed as argument (must be an integer)")
            self.chunkSize = args.chunkSize
        else:
            self.chunkSize = 20000000
        if self.chunkSize < 100:
            self.chunkSize = 1000000 * self.chunkSize
        if args.forceJobIndex:
            try:
                tester = int(args.forceJobIndex)  #Leave this argument as a string until it is used so that a zero value can be passed for the index and will still evaluate to true.
            except ValueError:
                quit("ABORTED: Forced job index argument must be an integer so that it can be used as an index.  If you don't understand why this is, you probably should not be messing with this argument.")
            self.forceJobIndex = args.forceJobIndex
        else:
            self.forceJobIndex = False
        self.noCleanup = args.noCleanup
        self.skipAzimuth = True
        self.verbose = args.verbose
        if not args.parallelJobLimit:
            if self.cluster:
                self.maxParallelJobs = clusterDefaultSelectionModeParallelJobLimit
            if self.standAlone:
                self.maxParallelJobs = standAloneDefaultSelectionModeParallelJobLimit
        else:
            try:
                self.maxParallelJobs = int(args.parallelJobLimit)
            except ValueError:
                quit("ABORTED: Parallel job limit must be an integer.")
            else:
                if self.maxParallelJobs < 1:
                    quit("ABORTED: Parallel job limit must be greater than 0")
        self.scratchFolder = args.scratchFolder
        if not self.scratchFolder:
            self.scratchFolder = "" #making sure this is cast to a string and not a NoneType (although that will probably add to a string with no trouble)
        else:
            if not self.scratchFolder[-1] == "/":
                self.scratchFolder = self.scratchFolder + "/"  #make sure that the directory name is passed ending with a slash so we can prepend it directly to our tempDir name
            if not os.path.isdir(self.scratchFolder):
                try:
                    os.mkdir(self.scratchFolder)
                except OSError:
                    quit("ABORTED: Unable to create scratch folder.  Check if directory containing this folder already exists.")
    
    def setFASTAWorkerArgs(self, args):  #Validate arguments for launching a FASTA indexing worker.  Users are unlikely to be launching this on their own.
        import os
        self.mode = "FASTAWorker"
        self.chromosome = args.chromosome
        self.start = args.start
        self.length = args.length
        if "_" in args.sequence:
            self.sequence = args.sequence
        else:
            quit("ABORTED: Invalid sequence passed to worker. Please include an underscore between the guide and PAM sequences.")
        if os.path.isfile(args.inputfile):
            self.inputfile = args.inputfile
        else:
            quit("ABORTED: FASTA file: " + args.inputfile + " not found.")
        self.genome = args.genome.upper()
        self.tempDir = args.tempDir
        self.workerID = args.workerID
        self.chunkSize = args.chunkSize
        #if os.path.isdir(args.tempDir):
        #    self.tempDir = args.tempDir
        #else:
        #    quit("ABORTED: Unable to detect temporary directory: " + args.tempDir)
        self.skipAzimuth = True
        self.species = args.species
        self.verbose = args.verbose

#=================================================Sequence target analysis/hypervisor objects=================================================================================================================================

class TargetSite(object):  #This object holds attributes that describe a potential target site found in the user-defined target sequence.  This can be extended as we get better ways to describe potential target sites.  Only needs a cut site sequence to be initialized, all else can be set later.
    
    def __init__(self, cutSeq, longSeq = False):
        self.longSeq = longSeq
        self.cutSeq = cutSeq  #this value should come in with the underscore already added between guide and pam
        self.matches = {}   #This is designed to hold the dictionary of match/mismatch sites that gets passed from the search function
        for i in range(0, args.mismatchTolerance + 1):
            self.matches[i] = []
        self.azimuthScore = -1  #Default value for this is -1 to indicate no score.
        self.score = False
        self.acceptable = True  #This flag gets set to false if the target has more than one perfect match in the genome
        self.mismatchRisk = False  #This is a function of how well-matched the sites are and if they are in or near an annotated gene
        
    def calculateSortValue(self):
        self.sortValue = (self.mismatchRisk, -self.azimuthScore)

class TargetFinder(object):  #This object is analogous to a FASTA indexer, except designed to deal with smaller sequences and can be extended to collect larger windows for analysis in azimuth
    
    def __init__(self, target):
        self.target = target  #This is the target sequence passed in.  Should be supplied by the user either on the command line or in a FASTA file
        self.longSeq = False  #If we can generate a 30bp site to pass to azimuth, this is where it gets stored.  Note that we may have to force it a bit if we try to apply their model to other systems
        self.lastGroup = 0
        self.done = False
        self.cutWindow = len(args.sequence) - 1  #subtract out the underscore
        self.start = 0  #start is inclusive
        self.end = self.cutWindow
        self.guide, self.pam = args.sequence.split("_")
        self.pamList = NondegenerateBases(self.pam).permutations()
        self.pamLength = len(self.pam)
        self.matches = []  #initialize an empty list to hold our match sites (which will be TargetSite class instances)
        self.done = False
        self.forceAzimuthPam = False  #This indicates that we have forced the azimuth model for this system by trimming the fixed bases on the end of the pam
        self.forceGuide1 = False  #This indicates that we have forced the azimuth model by making the 5' base we submit into the 5' base on the guide
        self.forceGuide3 = False  #This indicates we have done the same thing with the second base from the 5' end (base 3 if the guide is indexed to 1)
        
        
    def findMatches(self):  #main running function for this object, actually runs the search, gets azimuth scores if needed, and returns the list of matches
        while not self.done:
            windowSeq = self.target[self.start:self.end]
            revComp = str(ReverseComplement(windowSeq))
            if windowSeq[-self.pamLength:] in self.pamList:
                guide = windowSeq[:-self.pamLength]
                pam = windowSeq[-self.pamLength:]
                if not args.skipAzimuth:
                    longSeq = self.getLongSeq(guide, pam,'+')  #tries to get an extended sequence for azimuth analysis
                self.matches.append(TargetSite(guide + "_" + pam, longSeq))
            if revComp[-self.pamLength:] in self.pamList:
                guide = revComp[:-self.pamLength]
                pam = revComp[-self.pamLength:]
                if not args.skipAzimuth:
                    longSeq = self.getLongSeq(guide, pam,'-')
                self.matches.append(TargetSite(guide + "_" + pam, longSeq))
            self.advance()
        # if not args.skipAzimuth:
        #     self.useAzimuth = True
        # else:
        #     self.useAzimuth = False
        # if self.useAzimuth:
        #     self.azimuthAPIkey = self.getAzimuthAPIkey()
        #     if self.azimuthAPIkey:
        #         self.assignAzimuthScores()
        return self.matches
    
    def advance(self):  #moves the window ahead one character, then checks to see if it has reached the end
        self.start += 1
        self.end += 1
        self.done = self.end > len(self.target)
        
    def getLongSeq(self, guide, pam, strand):  #this method gets an extended sequence for azimuth or other analysis if possible
        pamExtensionLength = 3
        guideExtensionLength = 24 - len(self.guide)
        try:  #we need a try/except block for this because it is possible that the extended sequence will run us off the end of the sequence
            if strand == '+':
                pamEnd = self.end + pamExtensionLength
                guideStart = self.start - guideExtensionLength
                if pamEnd > len(self.target) or guideStart < 0:
                    return False
                pamExtension = self.target[self.end : pamEnd]
                guideExtension = self.target[self.start - guideExtensionLength : self.start]
            if strand == '-':
                pamStart = self.start - pamExtensionLength
                guideEnd = self.end + guideExtensionLength
                if pamStart < 0 or guideEnd > len(self.target):
                    return False
                pamExtension = self.target[self.start - pamExtensionLength : self.start]
                guideExtension = self.target[self.end : self.end + guideExtensionLength]
                pamExtension = str(ReverseComplement(pamExtension))
                guideExtension = str(ReverseComplement(guideExtension))
        except IndexError:  #If we get something near the end of the given sequence where we try to read off the end, we just return False for this value.  Later, this will tell us not try submitting it for analysis.
            return False
        if not len(pam) == 3:  #if we have to force the pam, we will warn the user
            if not self.forceAzimuthPam:
                print("WARNING: Attempting to force conformity of PAM site to the Azimuth model.  Predictions based on forced projections may not be as accurate.")
            self.forceAzimuthPam = True
            pam = pam[:2]
        extendedSeq = guideExtension + guide + pam + pamExtension
        # if not len(guide) == 20 and not args.noForcedBases:
        #     extendedSeq = list(extendedSeq)  #making it a list so that I can change individual characters by their index
        #     if not extendedSeq[4] == guide[0] and not args.noForced1:
        #         extendedSeq[4] = guide[0]
        #         if not self.forceGuide1:
        #             print("Forcing guide base 1 into position 1 for azimuth analysis.  Predictions based on forced projections may not be as accurate.")
        #             self.forceGuide1 = True
        #     if not extendedSeq[6] == guide[2] and not args.noForced3:
        #         extendedSeq[6] = guide[2]
        #         if not self.forceGuide3:
        #             print("Forcing guide base 3 into position 3 for azimuth analysis.  Predictions based on forced projections may not be as accurate.")
        #             self.forceGuide3 = True
        #     extendedSeq = str(extendedSeq)  #return the value back to a string for later submission
        return extendedSeq
    
    def getAzimuth(self, sequence, failedPrevious = False):  #this handles communication with the azure server to get a score.  This can later be replaced if we decide to run a local instance with the source code.
        import urllib.request
        import json
        import time
        import sys #for error catching
        data = {
            "Inputs":{
                "input1":{
                    "ColumnNames":["sequence", "cutsite", "percentpeptide"],
                    "Values":[[sequence, "-1", "-1"]]
                }
            },
                "GlobalParameters": {}
        }
        body = str.encode(json.dumps(data))
        #url = 'https://ussouthcentral.services.azureml.net/workspaces/ee5485c1d9814b8d8c647a89db12d4df/services/c24d128abfaf4832abf1e7ef45db4b54/execute?api-version=2.0&details=true'
        url = 'https://ussouthcentral.services.azureml.net/workspaces/ee5485c1d9814b8d8c647a89db12d4df/services/5c6cbabaef4947b4b7425e934b6f7d6b/execute?api-version=2.0&details=true'  #slower, but only one working for now.  Use for testing
        api_key = self.azimuthAPIkey
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
        req = urllib.request.Request(url, body, headers)
        try:
            response = urllib.request.urlopen(req)
            result = response.read().decode('utf-8')
            result = json.loads(result)
            return float(result['Results']['output2']['value']['Values'][0][0])
        except urllib.error.HTTPError as error:
            if error.code == 401:
                print("Unable to use Azimuth due to a possible invalid API key.  Please check on the status of key: " + self.azimuthAPIkey)
            else:
                print("The Azimuth request failed with status code: " + str(error.code))
                print(error.info())
                print(json.loads(error.read().decode('utf-8')))
            self.useAzimuth = False
            return -1  #Remember that -1 is our placeholder value for a failed attempt or no attempt.
        except urllib.error.URLError:
            if not failedPrevious:
                time.sleep(5) #wait 5 seconds before retry
                return self.getAzimuth(sequence, True)
            else:
                print("Unable to reach/find Azimuth server.  Please confirm you are connected to the internet.")
                self.useAzimuth = False
                return -1
        except:  #Allowing this for now while dealing with many possible exceptions due to experimental server and software
            if not failedPrevious:
                time.sleep(5)
                return self.getAzimuth(sequence, True)  #give it another go, because why not...
            else:
                error = sys.exc_info()
                print("Unexpected error in Azimuth scoring:")
                for item in error:
                    print(item)
                return -1
        
    def getAzimuthAPIkey(self):  #this gets the API key from a file
        import os
        if os.path.isfile("azimuth.apikey"):
            file = open("azimuth.apikey", 'r')
            key = file.read()
            file.close()
            key = key.strip()
            return key
        else:
            print("Unable to run azimuth.  Cannot locate API key.  Please save the key the same directory as this program under filename azimuth.apikey.")
            return False
        
    def assignAzimuthScores(self):  #iterate over all our matches and get an azimuth score if there is a saved extended sequence, otherwise it is left as the default -1 value
        for i in range(0,len(self.matches)):
            if self.matches[i].longSeq and self.useAzimuth:
                self.matches[i].azimuthScore = self.getAzimuth(self.matches[i].longSeq)        
                
class TargetSelection(object):  #This is the main running object for the target selection job
    
    def __init__(self):
        printStartUp()
        reportUsage("SELECTION")
        self.targetList = []
        self.indexedGenome = self.selectIndexedGenome() #we will pass this to the search supervisor.  This will save each supervisor a few seconds (probably not significant) and will cover for the potential loss of degeneracy when we pass the sequence to searcher agents 
        print("Checking for target sites")
        self.getTargetSequence()
        if not self.targetList:
            self.targetList = TargetFinder(self.target).findMatches()
        if not self.targetList:
            quit('ABORTED: No suitable target sequences found.')
        if selectionModeTargetLimitPerJob > 0 and len(self.targetList) > selectionModeTargetLimitPerJob and not args.clobber:
            quit("ABORTED: Too many targets in sequence.  Try running a shorter target sequence, a more specific Crispr system, or using clobber mode (argument -9) to override this.")
        print("Found " + str(len(self.targetList)) + " potential target sites.")
        self.createTempDir()
        self.createJobList()
        self.runJobList()
        self.gatherResults()
        self.sortResults()
        if not args.outputToFile:
            self.reportResults()
        else:
            self.reportToFile()
        if not args.noCleanup:
            self.cleanup()
        
    def getTargetSequence(self):
        if args.targetSequence:  #if the user just passed the sequence as an argument...
            target = args.targetSequence.strip()
            target = target.upper()
            for letter in target:
                if letter not in ['A','T','G','C']:  #reject any degenerate sequences passed (probably reasonable to expect the user to have a good sequence for their target)
                    quit("ABORTED: Invalid letters in targeted DNA sequence")
            self.target = target
        elif args.targetFasta:  #if the user referred us to a file for the sequence...
            try:
                targetFasta = open(args.targetFasta, 'r')
            except FileNotFoundError:
                quit("ABORTED: Unable to open the specified FASTA file")
            else:
                target = ""
                line = targetFasta.readline()
                while line:
                    if ">" in line:  #fasta standards state that a line starting with > is identifying a contig and will not contain sequence
                        line = targetFasta.readline()  #readline is probably less efficient than slurping the whole file.  If the user wants to run this on a sequence big enough that this becomes a concern, they are going to have bigger problems in their future.
                        continue
                    else:
                        line = line.replace("\n","")
                        line = line.upper()
                        for letter in line:
                            if letter not in ["A","T","G","C"]:
                                targetFasta.close()
                                quit("ABORTED: Invalid letters in the sequence file")
                        target += line
                        line = targetFasta.readline()
            self.target = target
            targetFasta.close()
        elif args.targetList:  #if the user passed a list of targets...
            try:
                targetListFile = open(args.targetList, 'r')
            except FileNotFoundError:
                quit("ABORTED: Unable to open the specified list of target sites")
            targetList = []
            line = targetListFile.readline()
            while line:
                line = line.strip()
                line = line.replace("\n","")
                line = line.upper()
                for letter in line:
                    if letter not in ['A','T','G','C','_']:
                        quit("ABORTED: Invalid character specified in target list item.")
                if not "_" in line:
                    line = line[:-len(self.pam)] + "_" + line[-len(self.pam):]
                targetList.append(TargetSite(line))  #we can't get an extended sequence from here, so longSeq will remain the default False value and the azimuth score will remain -1
                line = targetListFile.readline()
            self.targetList = targetList
            targetListFile.close()
            print("Using targets from target list file.")
        else:
            quit("ABORTED: No target sequence or list of target sites given/nothing for me to do.")
    
    def selectIndexedGenome(self):  #uses the user-passed guide_pam scheme to pick an indexed genome (or say if we don't have one) that is suitable for this run.  Remember that the sequence is stored in reverse
        import os
        if not os.path.isdir(args.genomeListDirectory):
            quit("ABORTED: No indexed genome directory found.  Please run the indexer to create indexed genomes for searching.")
        seqPam, seqGuide = args.sequence[::-1].split("_")
        self.pam = seqPam[::-1]
        self.guide = seqGuide[::-1]
        directoryContents = os.listdir(args.genomeListDirectory)
        for item in directoryContents:
            if not item[0] == "." and item.count(".") == 2 and "_" in item and "NNN" in item:
                itemSeq, itemGenome, species = item.split(".")
                if itemGenome == args.genome:
                    itemPam, itemGuide = itemSeq.split("_")
                    itemPamList = NondegenerateBases(itemPam).permutations()
                    if (seqPam == itemPam or seqPam in itemPam) and len(seqGuide) <= len(itemGuide):
                        return item
        quit("ABORTED: Please create an indexed genome for this search.  No suitable indexed genome was found.")
        
    def createTempDir(self):  #makes a temporary directory for this run.  Completions will clock out here and results will be reported back to it.
        if args.verbose:
            print ("Creating temporary directory")
        import re
        import os
        import datetime
        successful = False
        while not successful:
            currenttime = datetime.datetime.now()
            currenttime = str(currenttime)
            currenttime = re.sub(r'\W','',currenttime)
            self.tempDir = args.scratchFolder + '.shieldHQ' + currenttime
            if os.path.isdir(self.tempDir):
                continue
            try:
                os.mkdir(self.tempDir)
            except OSError:
                continue
            successful = True
        os.mkdir(self.tempDir + "/completed")
        os.mkdir(self.tempDir + "/progress")
        os.mkdir(self.tempDir + "/result")
        if args.verbose:
            print ("Temporary directory created.")
        return True
        
    def createJobList(self):
        self.jobList = {'queued':[], 'running':[], 'complete':[]}
        for targetSite in self.targetList:
            self.jobList['queued'].append(targetSite)
            
    def runJobList(self):
        import os
        import time
        self.submittedJob = 1
        maxSimultaneousJobs = args.maxParallelJobs // args.parallelJobs
        while self.jobList['queued'] or self.jobList['running']:
            try:
                while self.jobList['queued'] and len(self.jobList['running']) < maxSimultaneousJobs:
                    self.createJobBash(self.jobList['queued'][0])
                    self.submitJob(self.jobList['queued'][0])
                    self.jobList['running'].append(self.jobList['queued'][0])
                    del self.jobList['queued'][0]
                while len(self.jobList['running']) >= maxSimultaneousJobs or len(self.jobList['queued']) == 0:
                    newlyCompleted = []
                    for i in range(0, len(self.jobList['running'])):
                        if os.path.isfile(self.tempDir + "/completed/" + self.jobList['running'][i].cutSeq):
                            newlyCompleted.append(i)
                    newlyCompleted.sort(reverse = True)  #we need to reverse this list so that we remove items in reverse index order.  If we did not do this, and we had two items on the list (say 1 and 3), we could potentially remove item 1 first, and then item 3 becomes item 2, with what started off as item 4 now targeted for deletion and a very high probability that at some point we will run off the end of the list (IndexError)
                    if newlyCompleted:
                        for completedIndex in newlyCompleted:
                            self.jobList['complete'].append(self.jobList['running'][completedIndex])
                            del self.jobList['running'][completedIndex]
                    if not self.jobList['running'] and not self.jobList['queued']:
                        break
                    time.sleep(10)
            except KeyboardInterrupt:
                for key in list(self.jobList.keys()):
                    print(key)
                    for item in self.jobList[key]:
                        print("\t" + item.cutSeq)
                    if yesAnswer("Continue with run?"):
                        continue
                    else:
                        quit("ABORTED: By your command.")
                    
    def createJobBash(self, job):  #Creates a bash file to submit for running the job
        self.bash = self.tempDir + "/" + str(job.cutSeq) + ".sh"
        bashFile = open(self.bash, 'w')
        bashFile.write("#! /bin/bash\n")
        scratchFolder = ""
        if args.scratchFolder:
            scratchFolder = " --scratchFolder " + args.scratchFolder
        if args.cluster:
            systemInfo = " --cluster "
        if args.standAlone:
            systemInfo = " --standAlone "
        #bashFile.write("module load python/3.4\n")
        bashFile.write(pythonInterpreterAbsolutePath + " dsNickFury" + currentVersion + ".py --mode search --mismatchTolerance " + str(args.mismatchTolerance) + " --sequence " + job.cutSeq + " --forceGenome " + self.indexedGenome + " --outputDirectory " + self.tempDir + " --parallelJobs " + str(args.parallelJobs) + " --mismatchTolerance " + str(args.mismatchTolerance) + " --genomeDirectory " + args.genomeListDirectory.replace(" ",'\ ') + " --azimuthSequence " + str(job.longSeq) + scratchFolder + systemInfo + "\n")
        bashFile.close()
    
    def submitJob(self, job):  #submits the bash file to the queue scheduler
        shortName = "ShieldHQ" + str(self.submittedJob)
        self.submittedJob += 1
        if args.cluster:
            import os
            command = "qsub -cwd -V -N " + shortName + " -l h_data=2G,time=23:59:00 -e " + os.getcwd() +  "/schedulerOutput/ -o " + os.getcwd() + "/schedulerOutput/ " + self.bash
            if not args.mock:
                import subprocess
                import time
                subprocess.Popen(command, shell = True)
                time.sleep(1)   #Testing this to see if it prevents errors with the job schedulers by slowing job submission a little 
            else:
                print ("MOCK SUBMIT: " + command)
        if args.standAlone:
            command = "bash " + self.bash
            if not args.mock:
               import subprocess
               subprocess.Popen(command, shell = True)
            else:
                print ("MOCK SUBMIT: " + command)
            
            
    def gatherResults(self):  #gathers the results from the worker processes (passed via pickle), checks for unacceptable sites (ones that have perfect matches in multiple genomic locations), and calculates mismatch risk numbers
        import pickle
        for i in range(0,len(self.targetList)):
            totalMismatchRisk = 0
            genesCounted = [] #prevent us from counting multiple hits in the same gene twice or from counting hits due to a nearby pseudogene
            inputFile = open(self.tempDir + "/result/" + self.targetList[i].cutSeq, 'rb')
            result = pickle.load(inputFile)
            inputFile.close()
            self.targetList[i].matches = result['matches']
            self.targetList[i].azimuthScore = result['azimuthScore']
            if len(self.targetList[i].matches[0]) > 1:
                first = self.targetList[i].matches[0][0].gene
                for site in self.targetList[i].matches[0]:
                    if site.gene != first:
                        self.targetList[i].acceptable = False
                        break
            for j in range(0, args.mismatchTolerance + 1):
                for k in range(0, len(self.targetList[i].matches[j])):
                    risk = self.targetList[i].matches[j][k].calculateMismatchRisk()
                    if not (j == 0 and k == 0) or self.targetList[i].matches[j][k].gene in genesCounted:
                        totalMismatchRisk += risk
                    if self.targetList[i].matches[j][k].gene and self.targetList[i].matches[j][k].gene not in genesCounted:
                        genesCounted.append(self.targetList[i].matches[j][k].gene)
            self.targetList[i].mismatchRisk = totalMismatchRisk
                        
    def sortResults(self):  #Sorts in ascending order by mismatch risk first, then by azimuth score (done by sorting on the negative value of the azimuth score).  If no azimuth was given, the result will be shown last
        import operator
        for i in range(0, len(self.targetList)):
            self.targetList[i].calculateSortValue()        
        self.targetList.sort(key = operator.attrgetter('sortValue'))
        
    def reportResults(self):  #Reports results to STDOUT.  At some point, I should probably offer alternatives to output to a file or even some data object format like JSON
        unacceptableHeaderPrinted = False
        for target in self.targetList:
            if target.acceptable:
                print(target.cutSeq + "\tMismatch Risk: " + str(target.mismatchRisk))
                if int(target.azimuthScore) != -1:
                    print(" "*len(target.cutSeq) + "\tAzimuth Score: " + str(target.azimuthScore))
                else:
                    print(" "*len(target.cutSeq) + "\tAzimuth Score: Cannot determine")
                for count in range(0, args.mismatchTolerance + 1):
                    print("\tMismatches: " + str(count))
                    for site in target.matches[count]:
                        print("\t\t" + str(site))
        for target in self.targetList:
            if not target.acceptable:
                if not unacceptableHeaderPrinted:
                    print("******SITES WITH PERFECT MATCHES ELSEWHERE IN THE GENOME******")
                    unacceptableHeaderPrinted = True
                print(target.cutSeq + "\tMismatch Risk: " + str(target.mismatchRisk))
                for count in range(0, args.mismatchTolerance + 1):
                    print("\tMismatches: " + str(count))
                    for site in target.matches[count]:
                        print("\t\t" + str(site))
                        
    def reportToFile(self): #Reports results to a file passed as the appropriate argument
        output = open(args.outputToFile,'w')  #We validated that this is not an existing file (or we are willing to clobber it) in the arg checking above
        for target in self.targetList:
            if target.acceptable:
                output.write(target.cutSeq + "\tMismatch Risk: " + str(target.mismatchRisk) + "\n")
                if int(target.azimuthScore) != -1:
                    output.write(" "*len(target.cutSeq) + "\tAzimuth Score: " + str(target.azimuthScore) + "\n")
                else:
                    output.write(" "*len(target.cutSeq) + "\tAzimuth Score: Cannot determine" + "\n")
                for count in range(0, args.mismatchTolerance + 1):
                    output.write("\tMismatches: " + str(count) + "\n")
                    for site in target.matches[count]:
                        output.write("\t\t" + str(site) + "\n")
        for target in self.targetList:
            if not target.acceptable:
                if not unacceptableHeaderPrinted:
                    output.write("******SITES WITH PERFECT MATCHES ELSEWHERE IN THE GENOME******" + "\n")
                    unacceptableHeaderPrinted = True
                output.write(target.cutSeq + "\tMismatch Risk: " + str(target.mismatchRisk) + "\n")
                for count in range(0, args.mismatchTolerance + 1):
                    output.write("\tMismatches: " + str(count) + "\n")
                    for site in target.matches[count]:
                        output.write("\t\t" + str(site) + "\n")
                        
    def cleanup(self):
        import shutil
        shutil.rmtree(self.tempDir)
                        

#=================================================Azimuth analysis object==================================================================================================================

class AzimuthAnalysis(object):

    def __init__(self, sequence, failedPrevious = False):  #this handles communication with the azure server to get a score.  This can later be replaced if we decide to run a local instance with the source code.
        import urllib.request
        import json
        import time
        import sys #for error catching
        self.azimuthAPIkey = self.getAzimuthAPIkey()
        if not self.azimuthAPIkey:
            self.score = -1
        else:
            data = {
                "Inputs":{
                    "input1":{
                        "ColumnNames":["sequence", "cutsite", "percentpeptide"],
                        "Values":[[sequence, "-1", "-1"]]
                    }
                },
                    "GlobalParameters": {}
            }
            body = str.encode(json.dumps(data))
            #url = 'https://ussouthcentral.services.azureml.net/workspaces/ee5485c1d9814b8d8c647a89db12d4df/services/c24d128abfaf4832abf1e7ef45db4b54/execute?api-version=2.0&details=true'
            url = 'https://ussouthcentral.services.azureml.net/workspaces/ee5485c1d9814b8d8c647a89db12d4df/services/5c6cbabaef4947b4b7425e934b6f7d6b/execute?api-version=2.0&details=true'  #slower, but only one working for now.  Use for testing
            api_key = self.azimuthAPIkey
            headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
            req = urllib.request.Request(url, body, headers)
            try:
                response = urllib.request.urlopen(req)
                result = response.read().decode('utf-8')
                result = json.loads(result)
                self.score = float(result['Results']['output2']['value']['Values'][0][0])
            except urllib.error.HTTPError as error:
                if error.code == 401:
                    print("Unable to use Azimuth due to a possible invalid API key.  Please check on the status of key: " + self.azimuthAPIkey)
                else:
                    print("The Azimuth request failed with status code: " + str(error.code))
                    print(error.info())
                    print(json.loads(error.read().decode('utf-8')))
                self.useAzimuth = False
                self.score = -1  #Remember that -1 is our placeholder value for a failed attempt or no attempt.
            except urllib.error.URLError:
                if not failedPrevious:
                    time.sleep(5) #wait 5 seconds before retry
                    self.score = AzimuthAnalysis(sequence, True).score
                else:
                    print("Unable to reach/find Azimuth server.  Please confirm you are connected to the internet.")
                    self.useAzimuth = False
                    self.score = -1
            except:  #Allowing this for now while dealing with many possible exceptions due to experimental server and software
                if not failedPrevious:
                    time.sleep(5)
                    self.score = AzimuthAnalysis(sequence, True)  #give it another go, because why not...
                else:
                    error = sys.exc_info()
                    print("Unexpected error in Azimuth scoring:")
                    for item in error:
                        print(item)
                    self.score = -1
        
    def getAzimuthAPIkey(self):  #this gets the API key from a file
        import os
        if os.path.isfile("azimuth.apikey"):
            file = open("azimuth.apikey", 'r')
            key = file.read()
            file.close()
            key = key.strip()
            return key
        else:
            print("Unable to run azimuth.  Cannot locate API key.  Please save the key the same directory as this program under filename azimuth.apikey.")
            return False

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
    
class MatchSite(object):  #Note that this is also used when we unpickle this object from the hypervisor (target selection) function
    def __init__(self, chrom, begin, end, matchSeq, score, strand, colorScheme, mismatches, extendedMatchSeq = ""):
        self.chrom = chrom
        self.begin = begin
        self.end = end
        self.matchSeq = matchSeq
        self.score = score
        self.strand = strand
        self.colorScheme = colorScheme
        self.extendedMatchSeq = extendedMatchSeq
        self.thickStart = ""
        self.thickEnd = ""
        self.azimuth = False
        self.delimiter = "\t"
        try:  #this deals with sorting chromosomes that can be identified by numbers or X, Y, and M and being able to sort by number and then by letter
            sortChr = int(self.chrom)
            sortChr = str(sortChr).zfill(2)
        except ValueError:
            sortChr = self.chrom
        self.sortValue = (sortChr,int(begin))  #This value helps sort by chromosome/location
        self.mismatchRisk = False
        self.mismatches = mismatches
        self.gene = False
        
    def calculateMismatchRisk(self):  #
        if self.mismatchRisk:
            return self.mismatchRisk
        else:
            self.mismatchRisk = args.mismatchTolerance + 2 - self.mismatches
            if self.gene:
                self.mismatchRisk = self.mismatchRisk ** 2
            return self.mismatchRisk
        
    def __str__(self):  #quick way to output the info on the match site
        if not self.gene:
            printGene = "NoGene"
        else:
            printGene = self.gene.split("[")[0].strip() #info on source of gene annotation follows the open bracket.  This just takes the part before it.
        printName = "/".join([printGene, self.matchSeq])
        returnThings = [self.chrom, self.begin, self.end, printName, self.score, self.strand, self.thickStart, self.thickEnd, self.colorScheme]
        return self.delimiter.join(returnThings)

class SearchSupervisor(object):
    
    def __init__(self):
        if not args.forceGenome:
            printStartUp()
            reportUsage("SEARCH") 
            genomeDirectory = self.selectIndexedGenome()
        else:
            genomeDirectory = args.forceGenome
            pam, sequence, self.species = genomeDirectory.split(".")
        self.genomeDirectory = args.genomeListDirectory + genomeDirectory
        self.createTempDir()
        print("Creating job list")
        self.createJobList()
        print("Assigning jobs")
        self.assignJobs()
        print("Calculating Azimuth Score")
        self.azimuthScore = -1
        if args.azimuthSequence:  #Do this after finishing local job, but before monitoring, since we will still be waiting on them
            self.azimuthScore = AzimuthAnalysis(args.azimuthSequence).score
        print("Monitoring")
        self.monitorJobs()
        print("Gathering")
        self.gatherJobs()
        print("Sorting")
        self.sortResults()
        print("Annotating")
        self.annotateResults()
        print("Reporting")
        if not args.outputDirectory:
            self.reportResults()
        else:
            self.reportToDirectory()
        if not args.noCleanup:
            self.cleanup()
  
    def selectIndexedGenome(self):
        import os
        if not os.path.isdir(args.genomeListDirectory):
            quit("ABORTED: No indexed genome directory found.  Please run the indexer to create indexed genomes for searching.")
        seqPam, seqGuide = args.sequence[::-1].split("_")
        directoryContents = os.listdir(args.genomeListDirectory)
        for item in directoryContents:
            if not item[0] == "." and "." in item and "_" in item and "NNN" in item:
                itemSeq, itemGenome, itemSpecies = item.split(".")
                if itemGenome == args.genome:
                    itemPam, itemGuide = itemSeq.split("_")
                    itemPamList = NondegenerateBases(itemPam).permutations()
                    if (seqPam.upper() == itemPam.upper() or seqPam.upper() in itemPamList) and len(seqGuide) <= len(itemGuide):
                        self.species = itemSpecies.strip().lower()
                        return item
        quit("ABORTED: Please create an indexed genome for this search.  No suitable indexed genome was found.")
                
    def createTempDir(self):
        if args.verbose:
            print ("Creating temporary directory")
        import re
        import os
        import datetime
        successful = False
        while not successful:
            currenttime = datetime.datetime.now()
            currenttime = str(currenttime)
            currenttime = re.sub(r'\W','',currenttime)
            self.tempDir = args.scratchFolder + '.dsNickFuryMission' + currenttime
            if os.path.isdir(self.tempDir):
                continue
            try:
                os.mkdir(self.tempDir)
            except OSError:
                continue
            successful = True
        os.mkdir(self.tempDir + "/completed")
        os.mkdir(self.tempDir + "/progress")
        os.mkdir(self.tempDir + "/result")
        if args.verbose:
            print ("Temporary directory created.")
        return True
    
    def getRefFiles(self):
        import os
        dirContents = os.listdir(self.genomeDirectory)
        targets = []
        for item in dirContents:
            if os.path.isfile(self.genomeDirectory + "/" + item) and "c" in item:
                targets.append(item)
        return targets
    
    def createJobList(self):
        if args.verbose:
            print ("Creating a list of jobs.")
        self.jobList = []
        for i in range(0,args.parallelJobs):
            self.jobList.append([])
        indexedReferenceFiles = self.getRefFiles()
        remainder = len(indexedReferenceFiles) % args.parallelJobs
        filesPerJob = len(indexedReferenceFiles) // args.parallelJobs
        assignedFileCount = []
        for i in range(0,args.parallelJobs):
            if i < remainder:  #because it is indexed to zero, if we have a remainder of 1, we only need an extra job for the zeroth index.  If we have remainder of zero, nobody needs an extra job.  If Donald Trump wins, everybody will need two extra jobs.
                assignedFileCount.append(filesPerJob + 1)
            else:
                assignedFileCount.append(filesPerJob)
        counter = 0
        jobID = 0
        for file in indexedReferenceFiles:
            if counter <= assignedFileCount[jobID]:
                self.jobList[jobID].append(file)
                counter += 1
            else:
                jobID += 1
                counter = 0
                self.jobList[jobID].append(file)
                counter += 1
        return True
    
    def assignJobs(self):
        import pickle  #pickle has security issues, know about them before using it
        for i in range(1,len(self.jobList)):  #we index to 1 here because job 0 (which will have an equal or greater number of searches) will be reserved for the supervisor instance
            outputFile = open(self.tempDir + "/mission" + str(i), "wb")
            pickle.dump(self.jobList[i], outputFile)  #this could also be dumped to a network socket
            outputFile.close()
            self.createJobBash(i)
            self.submitJob(i)
        print("Submitted all jobs.  Beginning worker job on this node.")
        args.workerID = "0"
        args.inputDirectory = self.genomeDirectory
        myJob = WorkerJob(self.jobList[0])
        self.matches = myJob.reportResult()  #this will both make this instance work AND function as a bit of a timer
        print("Worker job on this node complete.")
        
    def createJobBash(self,jobID):
        self.bash = self.tempDir + "/" + str(jobID) + ".sh"
        bashFile = open(self.bash, 'w')
        bashFile.write("#! /bin/bash\n")
        #bashFile.write("module load python/3.4\n")
        bashFile.write(pythonInterpreterAbsolutePath + " dsNickFury" + currentVersion + ".py --mode worker --workerID " + str(jobID) + " --mismatchTolerance " + str(args.mismatchTolerance) + " --sequence " + args.sequence + " --inputDirectory " + self.genomeDirectory + " --tempDir " + self.tempDir + " --genomeDirectory " + args.genomeListDirectory.replace(" ",'\ ') + "\n")
        bashFile.close()
    
    def submitJob(self, jobID):
        shortName = "NickFury" + str(jobID)
        if args.cluster:
            import time
            import os
            command = "qsub -cwd -V -N " + shortName + " -l h_data=2G,time=0:59:00 -e " + os.getcwd() +  "/schedulerOutput/ -o " + os.getcwd() + "/schedulerOutput/ " + self.bash
            if not args.mock:
                import os
                time.sleep(10)
                os.system(command)
            else:
                print ("MOCK SUBMIT: " + command)
        if args.standAlone:
            command = "bash " + self.bash
            if not args.mock:
                import subprocess
                subprocess.Popen(command, shell = True)
            else:
                print ("MOCK SUBMIT: " + command)
            
            
    def monitorJobs(self):
        import time
        import os
        allDone = False
        if args.parallelJobs == 1:
            return True
        while not allDone:
            for i in range(1,len(self.jobList)):
                if args.verbose:
                    print("Checking for " + str(i))
                if not os.path.isfile(self.tempDir + "/completed/" + str(i) + ".done"):
                    if args.verbose:
                        print("it was not found")
                    allDone = False
                    time.sleep(10)
                    break
                else:
                    if args.verbose:
                        print("it was found")
                    allDone = True
        return True
    
    def gatherJobs(self):
        import pickle
        for i in range(1,len(self.jobList)):
            inputFile = open(self.tempDir + "/result/" + str(i), "rb")
            gatheredPart = pickle.load(inputFile)
            inputFile.close()
            for j in range(0,args.mismatchTolerance + 1):
                self.matches[j] += gatheredPart[j]
                
    def sortResults(self):
        import operator
        if args.verbose:
            print("Starting to sort.")
        for i in range(0,args.mismatchTolerance + 1):
            if args.verbose:
                print("Sorting group " + str(i))
            self.matches[i].sort(key = operator.attrgetter('sortValue'))
    
    def getAnnotation(self, site, expand = 0, failedPrevious = False):
        import urllib.request
        import time
        import json
        begin = int(site.begin) - expand
        end = int(site.end) + expand
        urlBase = 'http://rest.ensembl.org/overlap/region/' + self.species + '/'
        urlLocus = str(site.chrom) + ":" + str(begin) + "-" + str(end)
        urlArguments = "?feature=gene;content-type=application/json"
        fullURL = urlBase + urlLocus + urlArguments
        try:
            ensembl = urllib.request.urlopen(fullURL)
            ensembl = ensembl.read().decode('utf-8')
            ensembl = json.loads(ensembl)
        except urllib.error.HTTPError as error:
            if not failedPrevious:
                time.sleep(5)
                return self.getAnnotation(site, expand, True)
            else:
                print("The ensembl annotation request failed with status code: " + str(error.code))
                print(error.info())
                print(error.read().decode('utf-8'))
                return "Unable to get annotation.  Error code: " + str(error.code) + " FullURL = " + fullURL
        except urllib.error.URLError:
            if not failedPrevious:
                time.sleep(5)
                return self.getAnnotation(site, expand, True)
            else:
                print("Unable to reach/find ensembl server.  Please confirm you are connected to the internet.")
                return "Unable to contact ensembl. (URL/network error)"
        except http.client.HTTPException as error:
            if not failedPrevious:
                time.sleep(5)
                return self.getAnnotation(site, expand, True)
            else:
                print("Got bad status line trying to pull up " + fullURL)
                print("Response: " + error.read().decode('utf-8'))
                return "Unable to get annotation due to BadStatusCode error.  Matching " + args.sequence
        gene = False
        for item in ensembl:
            if item['description']:  #check if a gene is listed for the site, if not, check the next one.  If we get to the end and find no gene, then we return no gene.  Sometimes ensembl returns a result with no gene listed, followed by a second annotation listing the gene.
                gene = item['description']
        return gene

    def annotateResults(self):
        for key in list(self.matches.keys()):
            for i in range(0,len(self.matches[key])):
                self.matches[key][i].gene = self.getAnnotation(self.matches[key][i])
        for key in list(self.matches.keys()):
            for i in range(0,len(self.matches[key])):
                if not self.matches[key][i].gene:
                    self.matches[key][i].gene = self.getAnnotation(self.matches[key][i], args.annotationExpansion // 10)
        for key in list(self.matches.keys()):
            for i in range(0,len(self.matches[key])):
                if not self.matches[key][i].gene:
                    self.matches[key][i].gene = self.getAnnotation(self.matches[key][i], args.annotationExpansion)
            
    def reportResults(self):
        for i in range(0,args.mismatchTolerance + 1):
            print("Mismatches: " + str(i))
            for line in self.matches[i]:
                print("\t" + str(line))

    def reportToDirectory(self):
        import pickle
        print("Starting reporter function.")
        print("Reporting to directory.")
        outputData = {}
        outputData['sequence'] = args.sequence
        outputData['matches'] = self.matches
        outputData['azimuthScore'] = self.azimuthScore
        print(self.matches)
        print(args.sequence)
        print("Starting pickle")
        outputFile = open(args.outputDirectory + "/result/" + args.sequence, 'wb')
        pickle.dump(outputData, outputFile)
        outputFile.close()
        print("Pickle done.")
        clockOut = open(args.outputDirectory + "/completed/" + args.sequence, 'w')
        clockOut.close()
        print("Clocked out.")
                
    def cleanup(self):
        import shutil
        shutil.rmtree(self.tempDir)
                

    
class WorkerJob(object):
    
    def __init__(self, fileList = False):
        if not fileList:
            self.fileList = self.getJobList()
        else:
            self.fileList = fileList
        self.matchTable = self.createMatchTable()
        self.pam, self.guide = args.sequence[::-1].split("_")
        self.colorScheme = self.createColorScheme()
        print("Matching")
        self.checkAllSequences()
        print("Worker job reporting results")
        self.reportResult()

    def createMatchTable(self):
        matchTable = {}
        for i in range(0,args.mismatchTolerance+1):
            matchTable[i] = []
        return matchTable
        
    def getJobList(self):
        import pickle
        inputFile = open(args.tempDir + "/mission" + args.workerID, "rb")
        jobList = pickle.load(inputFile)
        inputFile.close()
        return jobList
        
    def createColorScheme(self):
        colorScheme = []
        if args.mismatchTolerance > 7:
            increments = 8
        elif args.mismatchTolerance == 0:
            return ["0,0,0"]
        else:
            increments = args.mismatchTolerance
            step = 255//increments
        for i in range(0,increments + 1):
            if i < 8:
                red = 255 - (step*i)
                green = 0
                blue = 0 + step*i
                colorScheme.append(str(red) + "," + str(green) + "," + str(blue))
            else:
                colorScheme.append(str(red) + ",0," + str(blue))
        return colorScheme
        
    def checkAllSequences(self):
        progress = 0
        for fileName in self.fileList:
            file = open(args.inputDirectory + "/" + fileName, 'r')
            wholeFile = file.read()
            file.close()
            wholeFile = wholeFile.split("\n")
            for line in wholeFile:
                if line:
                    mismatches = 0
                    chrom, begin, end, refSeq, score, strand = line.split("\t")
                    pam, guide = refSeq.split("_")
                    for i in range(0,len(self.guide)):
                        try:
                            if guide[i] != self.guide[i]:
                                mismatches += 1
                                if mismatches > args.mismatchTolerance:
                                    break
                        except IndexError:
                            quit("ABORTED: Encountered an error reading " + fileName + " where we got an error comparing input sequence " + self.guide + " to " + guide + ".  This could be due to a corrupted, shortened sequence in the data file, or a bug in the program.")
                        if i == len(self.guide) - 1:
                            matchGuide = guide[:len(guide)]
                            matchGuide = matchGuide[::-1]
                            matchSeq = matchGuide + pam[::-1]
                            matchSeqExtended = matchSeq
                            guideDiff = len(guide) - len(self.guide) #accounting for a longer guide sequence in the stored reference
                            if guideDiff != 0:
                                matchSeq = matchSeq[guideDiff:]
                                if strand == "+":
                                    begin = str(int(begin) + guideDiff)
                                if strand == "-":
                                    end = str(int(end) - guideDiff)
                            self.matchTable[mismatches].append(MatchSite(chrom, begin, end, matchSeq, str(1000*((len(guide)-mismatches)/len(guide))), strand, self.colorScheme[mismatches], mismatches))
                            if args.verbose:
                                print("\nFound Match")
                    progress += 1
                    if progress % 10000 == 0 and (args.verbose or args.workerID == "0"):
                        print("Processed " + str(progress) + " lines", end = "\r")
        print("\n")
                    
    def reportResult(self):
        if args.workerID == "0":
            return self.matchTable
        else:
            import pickle
            self.tempDir = args.tempDir
            outputFile = open(self.tempDir + "/result/" + args.workerID, "wb")
            pickle.dump(self.matchTable, outputFile)
            outputFile.close()
            # output = open(self.tempDir + "/result" + args.workerID, "w")
            # for line in self.matches:
            #     output.write("\t".join(line) + "\n")  #check if this works more efficiently from a pickle
            # output.close()
            clockOut = open(self.tempDir + "/completed/" + args.workerID + ".done", "w")
            clockOut.close()

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
        self.endpoint = self.length + ((self.lineBytes-self.lineBases)*(self.length // self.lineBases)) + self.start

class ParallelIndexJob(object):
    
    def __init__(self, contig, start, end, workerID):
        self.contig = contig
        self.start = start
        self.end = end
        self.workerID = workerID
        self.jobName =  str(contig) + "." + str(workerID)
        self.chunkStartBase = 0
        
    def __str__(self):
        return str(self.contig) + "." + str(self.workerID)

class FASTASupervisor(object):
    
    def __init__(self):
        import os
        printStartUp()
        reportUsage("INDEX")
        if not self.isAnEnsemblSpecies(args.species):  #make sure that the species they entered is one that is annotated, or make them set an option to ignore this
            if not args.clobber:
                quit("ABORTED: " + args.species.upper() + " is not a valid ensembl species.  Please check your naming of this species.  If this is known not to be an ensembl species, rerun with clobber mode on (argument '-9') to ignore this issue.")
        redundantGenome = self.suitableIndexedGenomeExists()
        if redundantGenome:
            if not args.clobber:
                seq, genome, species = redundantGenome.split(".")
                print("Suitable indexed genome already exists.  Indexed genome info:")
                print("Sequence " + seq[::-1])
                print("  Genome " + genome)
                quit("ABORTED: Suitable genome exists.  Please delete existing one (or run in clobber mode, not recommended).")
        self.countFileName = args.genomeListDirectory + "genomeData/" + args.sequence[::-1].upper() + "." + args.genome.upper() + "." + args.species.upper()
        if os.path.isfile(self.countFileName + ".gather"): #checking for an existing gather file and deleting it if it exists
            os.remove(self.countFileName + ".gather")
        if os.path.isfile(self.countFileName):  #and removing an existing countfile as well
            os.remove(self.countFileName)
        if redundantGenome:
            import shutil
            shutil.rmtree(args.genomeListDirectory + redundantGenome)
        self.getFiles(args.inputfile)
        self.createTempDir()
        self.createOutputDir()
        if args.ordered:
            self.faiJobs()
        else:
            self.createParallelJobs()
            if args.cluster:
                while len(self.parallelJobs) > args.maxParallelJobs:
                    print("WARNING: Current chunk size generated too many parallel jobs.  Increasing chunk size by 50% and trying again.")
                    args.chunkSize = args.chunkSize * 1.5
                    self.createParallelJobs()
                self.assignParallelJobs()
                self.monitorJobs()
            if args.standAlone:
                self.runJobQueue()
            self.gatherCounts()
            if not args.noCleanup:
                self.cleanup()
    
    def suitableIndexedGenomeExists(self):
        import os
        if not os.path.isdir(args.genomeListDirectory):
            return False
        seqPam, seqGuide = args.sequence[::-1].split("_")
        directoryContents = os.listdir(args.genomeListDirectory)
        for item in directoryContents:
            if not item[0] == "." and "." in item and "_" in item and "NNN" in item:
                try:
                    itemSeq, itemGenome, itemSpecies = item.split(".")
                    if itemGenome == args.genome:
                        if args.species.upper() != itemSpecies:  #If someone is trying to index a genome as being from a different species than an already annotated genome of the same name, warn them and require them to set the clobber option to do it.  They really should not be doing that.
                            if not args.clobber:
                                quit("ABORTED: Warning: This exact genome has already been indexed as species " + itemSpecies + " it should not also be indexed as " + args.species.upper() + ".  If you wish to actually have this situation (not recommended), please set the clobber option in arguments (argument '-9').")
                        itemPam, itemGuide = itemSeq.split("_")
                        if seqPam == itemPam and len(seqGuide) <= len(itemGuide):
                            return item
                except ValueError:
                    continue
        return False
    
    def isAnEnsemblSpecies(self, species):
        import urllib.request
        url = 'http://rest.ensembl.org/overlap/region/' + species.lower() + '/1:1000000-1000001?feature=gene'
        try:
            ensembl = urllib.request.urlopen(url)
            ensembl = ensembl.read().decode('utf-8')
            if "Can not find internal name for species" in ensembl:
                return False
        except urllib.error.HTTPError as error:
            message = error.read().decode('utf-8')
            if "Can not find internal name for species" in message:
                return False
            else:
                return True
        except urllib.error.URLError:
            print("Unable to reach/find ensembl server.  Please confirm you are connected to the internet.")
            return True
        return True
    
    def getFiles(self, fastaName):
        try:
            self.fasta = open(fastaName)
            firstLine = self.fasta.readline()
            if not ">" in firstLine:
                quit("ABORTED: " + fastaName + " does not appear to be a properly formatted FASTA file.  Please check to be sure that it follows FASTA standards.")
            self.fasta.close()
        except FileNotFoundError:
            quit("ABORTED: " + fastaName + " was not found.  This file was passed as the reference genome.")
        try:
            self.fai = open(fastaName + ".fai",'r')
        except FileNotFoundError:
            try:
                self.fai = open(fastaName[:-4] + ".fai", 'r')
            except FileNotFoundError:
                quit("ABORTED: No FASTA index (.fai) file could be found for " + fastaName + " please run a FASTA indexer and try again.")
    
    def createOutputDir(self):
        import os
        if not os.path.isdir(args.genomeListDirectory):
            os.mkdir(args.genomeListDirectory)
        if not os.path.isdir(args.genomeListDirectory + "genomeData"):
            os.mkdir(args.genomeListDirectory + "genomeData")
        outputDirectory = args.genomeListDirectory + args.sequence[::-1] + "." + args.genome + "." + args.species
        if os.path.isdir(outputDirectory) and not args.clobber:
            quit("ABORTED: This genome/system combination has already been indexed.")
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
        
    def createParallelJobs(self):
        contigData = []
        rawLine = self.fai.readline()
        while rawLine:
            line = FASTAIndexLine(rawLine)
            contigData.append(line)
            rawLine = self.fai.readline()
        self.contigList = []
        for line in contigData:
            self.contigList.append(str(line.contig))        
        parallelJobs = []
        windowLength = len(args.sequence) - 1  #the minus 1 accounts for the underscore separating the guide and pam
        for line in contigData:
            chunkSize = args.chunkSize
            chunkNumber = 0
            contigFinished = False
            contigStartByte = line.start
            contigEndByte = line.endpoint
            while not contigFinished:
                contig = line.contig
                start = contigStartByte + (chunkSize * chunkNumber)
                end = chunkSize + start
                if end >= contigEndByte:
                    contigFinished = True
                    readLength = contigEndByte - start
                    chunkNumber += 1
                else:
                    readLength = chunkSize + windowLength -1  #this will read windowLength - 1 bytes into the next chunk.  This means that the last window of this chunk will be one byte before the first windw of the next one
                    chunkNumber += 1
                parallelJobs.append(ParallelIndexJob(contig, start, readLength, chunkNumber))
        self.parallelJobs = parallelJobs
        
    def assignParallelJobs(self):    
        if not args.forceJobIndex:
            self.myJobIndex = len(self.parallelJobs) // 2  #making this instance take the job in the middle so that it less likely to be running through a string of pure "N"s
        else:
            self.myJobIndex = int(args.forceJobIndex)
        for i in range(0,len(self.parallelJobs)):
            if i != self.myJobIndex:
                self.createJobBash(self.parallelJobs[i],self.parallelJobs[i].workerID)
                self.submitJob(self.parallelJobs[i],self.parallelJobs[i].workerID)
        myJob = self.parallelJobs[self.myJobIndex]
        args.chromosome = myJob.contig
        args.start = str(myJob.start)
        args.length = str(myJob.end)
        args.workerID = str(myJob.workerID)
        self.myRun = FASTAreader()
        print("Completed this job. Checking/monitoring other parallel jobs.")
        
    def runJobQueue(self):
        import os
        import time
        jobList = {'queued':[],'running':[],'complete':[]}
        maxSimultaneousJobs = args.maxParallelJobs #no further calculation is needed here, since FASTAworkers don't launch subprocesses like search managers do
        print("Allowing only " + str(maxSimultaneousJobs) + " running jobs at once.")
        jobList['queued'] = self.parallelJobs
        while jobList['queued'] or jobList['running']:
            try:
                while jobList['queued'] and len(jobList['running']) < maxSimultaneousJobs:
                    self.createJobBash(jobList['queued'][0],jobList['queued'][0].workerID)
                    self.submitJob(jobList['queued'][0],jobList['queued'][0].workerID)
                    jobList['running'].append(jobList['queued'][0])
                    del jobList['queued'][0]
                while len(jobList['running']) >= maxSimultaneousJobs or len(jobList['queued']) == 0:
                    newlyCompleted = []
                    for i in range(0, len(jobList['running'])):
                        if args.ordered:
                            touchFileName = jobList['running'].contig
                        else:
                            touchFileName = jobList['running'][i].contig + "." + str(jobList['running'][i].workerID)
                        if os.path.isfile(self.tempDir + "/completed/" + touchFileName):
                            newlyCompleted.append(i)
                    newlyCompleted.sort(reverse = True)
                    if newlyCompleted:
                        for completedIndex in newlyCompleted:
                            jobList['complete'].append(jobList['running'][completedIndex])
                            del jobList['running'][completedIndex]
                    if not jobList['running'] and not jobList['queued']:
                        break
                    time.sleep(10)
            except KeyboardInterrupt:
                for key in list(jobList.keys()):
                    print(key)
                    for item in jobList[key]:
                        print("\t" + item.jobName)
                    if yesAnswer("Continue with run?"):
                        continue
                    else:
                        quit("ABORTED: By your command.")
        
    def calculateRAM(contigSize):
        pass  #skipping this method, as it seems like everything can run with 2G or less
    
    def createTempDir(self):
        import re
        import os
        import datetime
        successful = False
        while not successful:
            currenttime = datetime.datetime.now()
            currenttime = str(currenttime)
            currenttime = re.sub(r'\W','',currenttime)
            self.tempDir = args.scratchFolder + '.indexJob' + currenttime
            args.tempDir = self.tempDir
            if os.path.isdir(self.tempDir):
                continue
            try:
                os.mkdir(self.tempDir)
            except OSError:
                continue
            successful = True
        os.mkdir(self.tempDir + "/completed")
        os.mkdir(self.tempDir + "/progress")
        return True
    
    def createJobBash(self, job, workerID = False):
        import os
        self.bash = self.tempDir + "/" + job.contig + "." + str(workerID) + ".sh"
        bashFile = open(self.bash, 'w')
        bashFile.write("#! /bin/bash\n")
        #bashFile.write("module load python/3.4\n")
        if not workerID:
            bashFile.write(pythonInterpreterAbsolutePath + " dsNickFury" + currentVersion + ".py --mode FASTAWorker --chromosome " + job.contig + " --start " + str(job.start) + " --length " + str(job.end) + " --sequence " + args.sequence + " --inputfile " + os.path.abspath(args.inputfile) + " --genome " + args.genome + " --tempDir " + args.tempDir + " --species " + args.species + " --genomeDirectory " + args.genomeListDirectory + "\n")
        else:
            bashFile.write(pythonInterpreterAbsolutePath + " dsNickFury" + currentVersion + ".py --mode FASTAWorker --workerID " + str(workerID) + " --chromosome " + job.contig + " --start " + str(job.start) + " --length " + str(job.end) + " --sequence " + args.sequence + " --inputfile " + os.path.abspath(args.inputfile) + " --genome " + args.genome + " --tempDir " + args.tempDir + " --chunkSize " + str(args.chunkSize) + " --species " + args.species + " --genomeDirectory " + args.genomeListDirectory.replace(" ",'\ ') + "\n")
        bashFile.close()
    
    def submitJob(self, job, workerID = False):
        if args.cluster:
            import os
            if not workerID:
                shortName = "NickFury" + job.contig
            else:
                shortName = "NF." + job.contig + "." + str(workerID)    
            command = "qsub -cwd -V -N " + shortName + " -l h_data=2G,time=0:59:99 -e " + os.getcwd() +  "/schedulerOutput/ -o " + os.getcwd() + "/schedulerOutput/ " + self.bash
            if not args.mock:
                import os
                os.system(command)
            else:
                print ("MOCK SUBMIT: " + command)
        if args.standAlone:
            if not workerID:
                shortName = "NickFury" + job.contig
            else:
                shortName = "NF." + job.contig + "." + str(workerID)
            print("Submitting " + shortName)
            command = "bash " + self.bash
            if not args.mock:
                import subprocess
                subprocess.Popen(command, shell = True)
            else:
                print ("MOCK SUBMIT: " + command)
    
    def monitorJobs(self):
        import time
        import os
        allDone = False
        while not allDone:
            completedItems = os.listdir(self.tempDir + "/completed")
            #completedItems.append(str(args.chromosome + "." + str(args.workerID)))  #adding this instance's job to the completed job list
            for job in self.parallelJobs:
                checkJob = job.jobName
                #print("Checking " + checkJob)
                if not checkJob in completedItems:
                    #print("It was not found.")
                    allDone = False
                    time.sleep(60)
                    break
                else:
                    #print("It was found.")
                    allDone = True
        #print("Found all files.")
        print("All parallel jobs completed.  Finishing up.")
        return True
    
    def monitorJobsOld(self):
        import time
        import os
        allDone = False
        if len(self.parallelJobs) == 1:
            return True
        unfinished = self.parallelJobs
        toDelete = []
        checkCount = 0
        print("Starting Monitor")
        print("Unfinished: " + str(unfinished))
        while unfinished:
            print("Performing check: " + str(checkCount), end = "\r")
            checkCount += 1
            for i in range(0,len(unfinished)):
                if os.path.isfile(self.tempDir + "/completed/" + str(unfinished[i].contig) + "." + str(unfinished[i].workerID)):
                    print("Found " + str(i))
                    toDelete.append(i)
            if toDelete:
                print("To Delete: " + str(toDelete))
                print("Unfinished: " + str(unfinished))
            for index in toDelete[::-1]:  #run through this in reverse order so we don't run off the end of the array due to previously deleted items
                del unfinished[index]
            if toDelete:
                print("After: " + str(unfinished))
            toDelete = []
            if unfinished:
                time.sleep(1)
        return True
    
    def gatherCounts(self):
        import re
        counts = {}
        alreadyCounted = {}
        for contig in self.contigList:
            counts[contig] = 0
            alreadyCounted[contig] = []
        gatherFile = open(self.countFileName +  ".gather", 'r')
        rawData = gatherFile.read()
        gatherFile.close()
        data = rawData.split("\n")
        for datum in data:
            if datum:
                contig, workerID, hitCount = datum.split("\t")
                if workerID in alreadyCounted[contig]:
                    continue #protection against unintentional double counting if the job was previously stopped and restarted
                else:
                    counts[contig] += int(hitCount)
                    alreadyCounted[contig].append(workerID)
        output = open(self.countFileName, 'w')
        for contig in self.contigList:
            output.write(contig + "\t" + str(counts[contig]) + "\n")
        output.close()
        
    def cleanup(self):
        import os
        import shutil
        os.remove(self.countFileName + ".gather")
        shutil.rmtree(self.tempDir)

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
        if self.start // 10000 > self.lastGroup and (args.verbose or not args.workerID):
            print("Tested " + str((self.start // 10000)*10000), end = "\r")
            self.lastGroup = self.start // 10000
        self.sequence = self.chromosome[self.start:self.end]
        if ">" in self.sequence:
            raise RuntimeError("Ran off end of chromosome.  > in sequence: " + self.sequence)
        if self.sequence[-1] == "N":
            self.nInLastPositionJump()
            return False
        if "N" in self.sequence:
            return False
        if self.sequence[-self.pamLength:].upper() in self.pamList:
            guide = self.sequence[:-self.pamLength]
            pam = self.sequence[-self.pamLength:]
            self.forwardMatch = guide + "_" + pam
        else:
            self.forwardMatch = False
        revComp = str(ReverseComplement(self.sequence))
        if revComp[-self.pamLength:].upper() in self.pamList:
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
        characterCountCheck = inputFile.readline()
        while ">" in characterCountCheck:
            characterCountCheck = inputFile.readline()
        inputFile.close()
        lineBytes = len(characterCountCheck)
        lineBases = len(characterCountCheck.strip())
        lineDifference = lineBytes - lineBases
        #print("Line diff: " + str(lineDifference))
        if args.workerID:
            chunkStartByte = int(args.chunkSize) * (int(args.workerID) - 1)
            chunkStart = chunkStartByte - (lineDifference * (chunkStartByte // lineBytes))
            #print("ChunkStartByte: " + str(chunkStartByte))
            #print("ChunkStart: " + str(chunkStart))
        else:
            chunkStart = 0
        self.outputDirectory = args.genomeListDirectory + args.sequence[::-1] + "." + args.genome + "." + args.species
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
        inputFile = open(args.inputfile, 'r')
        window = FASTAWindow(inputFile, args.start, args.length, windowsize, pamList)
        if not args.workerID:
            outputFileName = self.outputDirectory + "/" + fileChromosome + "c" + str(hitCount // 10000).zfill(9)
        else:
            outputFileName = self.outputDirectory + "/" + fileChromosome + "c" + str(args.workerID).zfill(3) + str(hitCount // 10000).zfill(9)
        outputFile = False  #minor change so we don't open an output file until we have an output to write
        while window.getNextMatch():
            if window.forwardMatch:
                if not outputFile:
                    outputFile = open(outputFileName, 'w')
                outputFile.write("\t".join([args.chromosome, str(window.start + chunkStart + 1), str(window.end + chunkStart + 1 + 1), window.forwardMatch[::-1], '', "+\n"]))  # The plus 1 in the position is because chromosome data is indexed to 0 while chromosome positions are indexed to 1.  The second +1 for the end location is to account for the BED file standard end base not being inclusive (like python indexing).
                hitCount += 1
                if hitCount % 100000 == 0:  #increasing the filesize by 10x to see if the decreased I/O from the drive saves some searching time.  Files should still be only about 4MB.
                    outputFile.close()
                    if not args.workerID:
                        outputFileName = self.outputDirectory + "/" + fileChromosome + "c" + str(hitCount // 10000).zfill(9)
                    else:
                        outputFileName = self.outputDirectory + "/" + fileChromosome + "c" + str(args.workerID).zfill(3) + str(hitCount // 10000).zfill(9)
                    outputFile = open(outputFileName, 'w')
            if window.reverseMatch:
                if not outputFile:
                    outputFile = open(outputFileName, 'w')
                outputFile.write("\t".join([args.chromosome, str(window.start + chunkStart + 1), str(window.end + chunkStart + 1 + 1), window.reverseMatch[::-1], '', "-\n"]))
                hitCount += 1
                if hitCount % 100000 == 0:
                    outputFile.close()
                    if not args.workerID:
                        outputFileName = self.outputDirectory + "/" + fileChromosome + "c" + str(hitCount // 10000).zfill(9)
                    else:
                        outputFileName = self.outputDirectory + "/" + fileChromosome + "c" + str(args.workerID).zfill(3) + str(hitCount // 10000).zfill(9)
                    outputFile = open(outputFileName, 'w')
        if outputFile:
            outputFile.close()
        if not args.workerID:
            touchFile = open(args.tempDir + "/completed/" + args.chromosome, 'w')  #This is the clockout
            touchFile.close()
            countFileName = args.genomeListDirectory + "genomeData/" + args.sequence[::-1] + "." + args.genome + "." + args.species.upper() + ".gather"
            countFile = open(countFileName, 'a')
            countFile.write(args.chromosome + "\t" + str(hitCount) + "\n")
            countFile.close()
        else:
            self.countFileName = args.genomeListDirectory + "genomeData/" + args.sequence[::-1] + "." + args.genome + "." + args.species.upper() + ".gather"
            countFile = open(self.countFileName, 'a')
            countFile.write(args.chromosome + "\t" + args.workerID + "\t" + str(hitCount) + "\n")
            countFile.close()
            touchFile = open(args.tempDir + "/completed/" + args.chromosome + "." + str(args.workerID), 'w')
            touchFile.close()
            
#=====================================================Execution code===========================================================================

def main():
    import datetime
    import os
    if not os.path.isdir("schedulerOutput"):  #Used for writing scheduler output of subprocesses to a single folder, otherwise this folder can start getting messy.  Only needed for cluster operation, not single server.
       os.mkdir("schedulerOutput")
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
    elif args.mode == 'selection':
        run = TargetSelection()
    runTime = datetime.datetime.now() - startTime
    print (args.mode.upper() + " run completed in " + (str(runTime)))
main()
    
