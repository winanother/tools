@echo off

if "%JAVA_HOME%"=="E:\BurpSuite\jdk8" (
    
    setx "JAVA_HOME" "E:\BurpSuite" /M
) else (
    
    setx "JAVA_HOME" "E:\BurpSuite\jdk8" /M
)

