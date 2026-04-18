RESPOND TYPE=echo MSG="starting Klipper Hotload tests"
U FILE={EXTRAS}/klipper_hotload_demotest/demotest.py FUN=demotest

U FILE={EXTRAS}/klipper_hotload_demotest/a/demotest.py FUN=funA CHECK=a/funA
U CHECK=a/funA # checking default FILE with absolute path

U FUN=funB CHECK=a/funB # checking default FILE with absolute path
U CHECK=a/funB # checking default FUN

U PATH={EXTRAS}/klipper_hotload_demotest FILE=demotest.py FUN=funA CHECK=/funA # testing PATH
U CHECK=/funA # testing defaults
U FUN=funB CHECK=/funB 

U PATH={EXTRAS}/klipper_hotload_demotest FILE=a/demotest.py FUN=funA CHECK=a/funA # testing relative path component in FILE
U CHECK=a/funA # testing defaults
U FUN=funB CHECK=a/funB 

U FILE=a/b/demotest.py FUN=funA CHECK=a/b/funA # testing relative path component in FILE
U FUN=funB CHECK=a/b/funB

