# mks500-configurator
Configuration script for the MKS 500 Cold Cathode Vacuum Gauge

1. Reads every uncommented command/query from gauge, records as "save"
2. Executes each command with the argument. If the argument is NA, it is skipped. Change NA to value you want programmed. (resp)
3. Reads every command to confirm settings were accepted. (check)

To use:
- Edit the settings file. Change NA to the value you want programmed.
