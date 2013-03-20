import pangloss
import glob

#===============================
#read in any command line inputs



#===============================
#open the survey parameterfile and read in:




#===============================
#make N calibration light-cones:
# you should only need to do this once, unless you want a new set of lightcones.
CreateNewCalibrationLightcones=True

N=100 # This number should be at least tens of thousands to do 'science'
radius=2 #this is the radius out to which halos are included. Larger than 2 doesn't seem to help the reconstruction much

if CreateNewCalibrationLightones:
    MakeCones(N,calibrationcones,radius=radius,catalogue=cataloguelist,kappa=kappalist,gamma1=gamma1list,gamma2=gamma2list)


#===============================
#Define a few things that are used in the reconstruction:

if DoReconstruction==True:
        #first we need to define some quantities and load in some often used objects in order to speed up the reconstruction.

        #define the halo truncation scale: this is the scale where the halo profile transitions from r^-3 to r^-5. (needed to keep total halo mass finite)
        truncationscale=5 #virial radii

        #define how many realisations of each line cone are wanted. larger takes time, but produces smoother results. Nrealisation~500 seems to work well.
        Nrealisations=100

        #read in the stellar mass to halo mass relation files:
        BT=open("DATA/SHMR/S2H.behroozi","rb")
        BI=open("DATA/SHMR/H2S.behroozi","rb")
        SHMR_S2H=cPickle.load(BT)
        SHMR_H2S=cPickle.load(BI)

        #generate the redshift grid on which calculations are done:
        Grid=pangloss.Grid(zl,zs)

#===============================
#Analyse calibration sightlines according to scheme defined in survey.params
CreateNewCalibration=True
if CreateNewCalibration:
    Conelist=glob.glob(calibrationcones)

    if DoReconstruction==False: #the 'reconstruction' is trivial:
        for i in range(len(Conelist)):
            Cone = Conelist[i]
            #note// this doesn't exist:
            ConeResult=WeightingScheme(Cone,surveyparams)
            
    if DoReconstruction==True:
        for i in range(len(Conelist)):
            Cone = Conelist[i]

            ConeResult=Reconstruct(Cone,zl,zs,Grid,SHMR_H2S,SHMR_S2H,Nrealisation,truncationscale, surveyparams)

            #save ConeResult
            OUTPUT=open("%s/cone%i_%s.result"%(CalibrationResultsDirectory,i,surveyname),"wb")
            cPickle.dump(ConeResult,OUTPUT,2)
            OUTPUT.close()


#===============================
#Turn all the results of the calibration lines of sight into a calibration guide of P(kappa_ext,mu_ext,WEIGHT) where weight is the e.g. kappa_halo
if CreateNewCalibration:
    if DoReconstruction==True:
        MakeReconstructionCalibration(CalibrationResultsDirectory,surveyname)
    if DoReconstruction==False:
        MakeWeightCalibration(CalibrationResultsDirectory,surveyname)

#===============================
#Make 'real' lines of sight to analyse.:

#use Mosters halo mass to stellar mass relation?

#ask for high shear lines of sight only?

#-------------------------------
#Analyse real lines of sight
if DoReconstruction==True:
    Conelist=glob.glob(realcones)

    for i in range(len(Conelist)):
        Cone = Conelist[i]
        ConeResult=Reconstruct(Cone,zl,zs,Grid,SHMR_H2S,SHMR_S2H,Nrealisation,truncationscale, surveyparams)

        OUTPUT=open("%s/cone%i_%s.uncalibratedresult"%(RealResultsDirectory,i,surveyname),"wb")
        cPickle.dump(ConeResult,OUTPUT,2)
        OUTPUT.close()


#-------------------------------
# Calibrate real lines of sight

        Value=numpy.median(ConeResult[3])

        if WeightParameter1==kappa:
            Result=CalibrateResult(CalibrationResultsDirectory,surveyname,Value,width=0.01,magnification=False)
        #width includes the wiggle room in the calibration; there are no lines of sight that are identical, so we have to compromise; we give it a gaussian weighting scheme. Note this will fail if your real line of sight is abnormal and you only have a small calibration dataset.
        elif WeightParameter1==mu:
            Result=CalibrateResult(CalibrationResultsDirectory,surveyname,Value,width=0.01,magnification=True)


        #save ConeResult
        OUTPUT=open("%s/cone%i_%s.calibratedresult"%(RealResultsDirectory,i,surveyname),"wb")
        cPickle.dump(Result,OUTPUT,2)
        OUTPUT.close()
        
        #output contains a 3 column list of samples for the line of sight;
        # kappa, magnification, weight


#===============================
# Use the results to do some science...

#===============================






