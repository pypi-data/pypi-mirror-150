#!/usr/bin/env softIoc
#!/opt/epics/R7/base/bin/darwin-x86/softIoc
## Register all support components

#softIoc_registerRecordDeviceDriver(pdbbase)
dbLoadTemplate("./excas.substitutions","")
dbLoadRecords("./test.db")

#iocInit # for EPICS 3.x
